from datetime import datetime, timedelta
from typing import List, Dict
from bson import ObjectId
from app.utils.db import teachers_collection, availability_collection, invigilator_collection
from app.config import Config

def is_teacher_available(teacher_name: str, date: str, exam_time_start: str, exam_time_end: str) -> bool:
    # Check if teacher exists
    teacher = teachers_collection.find_one({"name": teacher_name})
    if not teacher:
        return False
    
    teacher_id = str(teacher.get("_id"))
    
    # Get teacher's availability record
    availability = availability_collection.find_one({"teacher_id": teacher_id})
    if not availability:
        # No availability record means teacher is available for all slots
        return True
    
    unavailable_slots = availability.get("slots", [])
    
    # Calculate which slot the exam falls into
    # Parse date and time
    try:
        exam_date = datetime.strptime(date, "%Y-%m-%d")
        exam_start = datetime.strptime(exam_time_start, "%H:%M")
        exam_end = datetime.strptime(exam_time_end, "%H:%M")
    except ValueError:
        return False
    
    # Get day of week (0 = Monday, 4 = Friday for 5-day week)
    day_of_week = exam_date.weekday()
    
    # Check if day is within working days (assuming 5-day week: Mon-Fri)
    if day_of_week >= int(Config.DAYS_PER_WEEK):
        return False
    
    # Calculate slot number based on time
    # Assuming slots are distributed throughout the day
    slots_per_day = int(Config.SLOTS_PER_DAY)
    
    # Calculate exam slot (this is a simplified approach)
    # You may need to adjust based on your slot definition
    exam_hour = exam_start.hour
    slot_number = day_of_week * slots_per_day + (exam_hour // (24 // slots_per_day))
    
    # Check if this slot is in unavailable slots
    return slot_number not in unavailable_slots


def assign_invigilators_simple(
    exam_date_from: str,
    exam_date_to: str,
    teacher_names: List[str],
    teachers_per_day: int,
    exam_time_start: str,
    exam_time_end: str
) -> List[Dict]:

    # Generate date range
    start_date = datetime.strptime(exam_date_from, "%Y-%m-%d")
    end_date = datetime.strptime(exam_date_to, "%Y-%m-%d")
    current_date = start_date
    
    assignments = []
    teacher_index = 0
    
    # For each day in range
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Get next N teachers (round-robin)
        day_teachers = []
        for i in range(teachers_per_day):
            teacher_idx = (teacher_index + i) % len(teacher_names)
            teacher_name = teacher_names[teacher_idx]
            
            # Check availability (skip if not available)
            if is_teacher_available(teacher_name, date_str, exam_time_start, exam_time_end):
                day_teachers.append(teacher_name)
            else:
                # If not available, find next available teacher
                for j in range(len(teacher_names)):
                    alt_idx = (teacher_idx + j) % len(teacher_names)
                    alt_teacher = teacher_names[alt_idx]
                    if is_teacher_available(alt_teacher, date_str, exam_time_start, exam_time_end):
                        day_teachers.append(alt_teacher)
                        break
            
            if len(day_teachers) == teachers_per_day:
                break
        
        # Add assignment for this day
        if day_teachers:
            assignments.append({
                "date": date_str,
                "teachers": day_teachers
            })
        
        # Move to next day
        current_date += timedelta(days=1)
        teacher_index = (teacher_index + teachers_per_day) % len(teacher_names)
    
    return assignments


def save_invigilator_assignment(assignment_data: Dict):
    result = invigilator_collection.insert_one(assignment_data)
    return str(result.inserted_id)


def get_invigilator_assignments():
    return list(invigilator_collection.find({}, {"_id": 0}))

