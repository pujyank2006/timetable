from typing import Dict, List, Any
from app.utils.db import availability_collection, teachers_collection, time_table_collection, input_data_collection

def update_availability_after_timetable():
    try:
        # Get all timetables
        timetables = list(time_table_collection.find({}, {"_id": 0}))
        
        if not timetables:
            return {"success": False, "message": "No timetables found"}
        
        # Get input data to understand teacher-subject mappings
        input_data = list(input_data_collection.find({}, {"_id": 0}))
        
        if not input_data:
            return {"success": False, "message": "No input data found"}
        
        # Create teacher-subject mapping from input data
        teacher_subject_mapping = _create_teacher_subject_mapping(input_data)
        
        # Get all teachers for mapping
        teachers = list(teachers_collection.find({}, {"_id": 0}))
        teacher_id_to_name = {teacher["id"]: teacher["name"] for teacher in teachers}
        
        updated_teachers = []
        
        # Process each timetable entry
        for timetable in timetables:
            class_id = timetable.get("class_id")
            ttable = timetable.get("ttable", {})
            
            # Process each subject and its slot positions
            for subject, slot_positions in ttable.items():
                # Find which teacher teaches this subject for this class
                teacher_info = _find_teacher_for_subject_in_input_data(
                    class_id, subject, input_data, teacher_subject_mapping
                )
                
                if teacher_info:
                    teacher_id = teacher_info["id"]
                    teacher_name = teacher_info["name"]
                    
                    # Update availability for this teacher
                    success = _update_teacher_availability(teacher_id, slot_positions)
                    
                    if success:
                        updated_teachers.append(teacher_name)
        
        return {
            "success": True,
            "message": f"Updated availability for {len(set(updated_teachers))} teachers",
            "updated_teachers": list(set(updated_teachers))
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error updating availability: {str(e)}"}

def _create_teacher_subject_mapping(input_data: List[Dict]) -> Dict[str, List[str]]:
    teacher_subjects = {}
    
    for data in input_data:
        teachers = data.get("teachers", [])
        for teacher in teachers:
            teacher_name = teacher.get("name", "")
            subjects = teacher.get("subject", [])
            
            if teacher_name and subjects:
                if teacher_name not in teacher_subjects:
                    teacher_subjects[teacher_name] = []
                teacher_subjects[teacher_name].extend(subjects)
    
    # Remove duplicates
    for teacher_name in teacher_subjects:
        teacher_subjects[teacher_name] = list(set(teacher_subjects[teacher_name]))
    
    return teacher_subjects

def _find_teacher_for_subject_in_input_data(
    class_id: str, 
    subject: str, 
    input_data: List[Dict], 
    teacher_subject_mapping: Dict[str, List[str]]
) -> Dict:
    # First, try to find teacher for this specific class
    for data in input_data:
        if data.get("class_name") == class_id:
            teachers = data.get("teachers", [])
            for teacher in teachers:
                subjects = teacher.get("subject", [])
                if subject in subjects:
                    return {
                        "id": teacher.get("id"),
                        "name": teacher.get("name"),
                        "email": teacher.get("email")
                    }
    
    # If not found for specific class, find any teacher who teaches this subject
    for teacher_name, subjects in teacher_subject_mapping.items():
        if subject in subjects:
            # Find teacher details from teachers collection
            teacher = teachers_collection.find_one({"name": teacher_name})
            if teacher:
                return {
                    "id": teacher.get("id"),
                    "name": teacher.get("name"),
                    "email": teacher.get("email")
                }
    
    return None

def _find_teacher_for_subject(class_id: str, subject: str, teachers: List[Dict]) -> Dict:
    for teacher in teachers:
        if "subjects" in teacher and subject in teacher["subjects"]:
            return teacher
    return None

def _update_teacher_availability(teacher_id: str, occupied_slots: List[int]) -> bool:
    try:
        # Get current availability for this teacher
        current_availability = availability_collection.find_one({"teacher_id": teacher_id})
        
        if not current_availability:
            # Create new availability entry if it doesn't exist
            new_availability = {
                "teacher_id": teacher_id,
                "slots": occupied_slots,
                "submitted": True
            }
            availability_collection.insert_one(new_availability)
            return True
        
        # Get existing unavailable slots
        existing_slots = set(current_availability.get("slots", []))
        
        # Add new occupied slots to the unavailable slots
        updated_slots = list(existing_slots.union(set(occupied_slots)))
        
        # Update the availability document
        availability_collection.update_one(
            {"teacher_id": teacher_id},
            {"$set": {"slots": updated_slots, "submitted": True}}
            # If only timetable slots have to be considered
            # {"$set": {"slots": occupied_slots, "submitted": True}}
        )
        
        return True
        
    except Exception as e:
        print(f"Error updating availability for teacher {teacher_id}: {str(e)}")
        return False

def get_teacher_availability_status():
    try:
        # Get all availability records
        availability_records = list(availability_collection.find({}, {"_id": 0}))
        
        # Get teacher information
        teachers = list(teachers_collection.find({}, {"_id": 0}))
        teacher_info = {teacher["id"]: teacher for teacher in teachers}
        
        # Combine availability with teacher info
        result = []
        for record in availability_records:
            teacher_id = record.get("teacher_id")
            teacher_data = teacher_info.get(teacher_id)
            
            if teacher_data:
                result.append({
                    "teacher_id": teacher_id,
                    "teacher_name": teacher_data.get("name", "Unknown"),
                    "teacher_email": teacher_data.get("email", ""),
                    "unavailable_slots": record.get("slots", []),
                    "submitted": record.get("submitted", False),
                    "total_unavailable": len(record.get("slots", []))
                })
        
        return {
            "success": True,
            "data": result,
            "total_teachers": len(result)
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error fetching availability status: {str(e)}"}