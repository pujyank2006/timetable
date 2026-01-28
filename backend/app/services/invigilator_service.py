from datetime import datetime, timedelta
from typing import List, Dict
from app.utils.db import teachers_collection, availability_collection, invigilator_collection

def is_teacher_available(teacher_name: str, date: str, exam_time_start: str, exam_time_end: str) -> bool:
    # teacher = teachers_collection.find_one({"name": teacher_name})
    # return teacher is not None

    # Accept any teacher
    return True


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

