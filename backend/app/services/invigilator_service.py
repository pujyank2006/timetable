from datetime import datetime, timedelta
from typing import List, Dict
from app.utils.db import teachers_collection, availability_collection, invigilator_collection

def calculate_slot_number(date: str, time_start: str, hours_per_day: int = 7, days_per_week: int = 5) -> int:
    try:
        day_of_week = datetime.strptime(date, "%Y-%m-%d").weekday()  # 0=Monday, 6=Sunday
        
        # Only consider weekdays (Monday-Friday)
        if day_of_week >= days_per_week:
            return -1  # Weekend, not a valid teaching slot
        
        hour = int(time_start.split(":")[0])
        
        # Assuming teaching starts at 9 AM (hour 9) and goes for hours_per_day
        # Adjust hour to be relative to start of teaching day
        teaching_hour = hour - 9  # 9 AM = 0, 10 AM = 1, etc.
        
        if teaching_hour < 0 or teaching_hour >= hours_per_day:
            return -1  # Outside teaching hours
        
        slot_number = day_of_week * hours_per_day + teaching_hour
        return slot_number
        
    except Exception as e:
        print(f"Error calculating slot number for {date} {time_start}: {e}")
        return -1

def is_teacher_available(teacher_name: str, date: str, exam_time_start: str, exam_time_end: str) -> bool:
    """
    Check if a teacher is available for invigilation based on their availability data.
    Teachers not in the database are considered available all the time.
    """
    try:
        # Find teacher by name
        teacher = teachers_collection.find_one({"name": teacher_name})
        if not teacher:
            # Teacher not found in DB, consider them available all the time
            print(f"Teacher '{teacher_name}' not found in database, considering available all the time")
            return True
        
        teacher_id = teacher.get("id")
        if not teacher_id:
            print(f"Teacher '{teacher_name}' has no ID in database, considering available all the time")
            return True
        
        # Get teacher's availability data
        availability = availability_collection.find_one({"teacher_id": teacher_id})
        if not availability:
            # No availability data submitted, consider them available all the time
            print(f"No availability data found for teacher '{teacher_name}', considering available all the time")
            return True
        
        unavailable_slots = availability.get("slots", [])
        
        # Calculate slot number for the exam time
        slot_number = calculate_slot_number(date, exam_time_start)
        
        if slot_number == -1:
            print(f"Invalid date/time slot for {date} {exam_time_start}")
            return False
        
        # Check if this slot is in unavailable slots
        is_available = slot_number not in unavailable_slots
        print(f"Teacher '{teacher_name}' availability for slot {slot_number} ({date} {exam_time_start}): {'Available' if is_available else 'Unavailable'}")
        
        return is_available
        
    except Exception as e:
        print(f"Error checking availability for {teacher_name}: {e}")
        # In case of error, consider teacher available
        return True


def assign_invigilators_simple(
    exam_date_from: str,
    exam_date_to: str,
    teacher_names: List[str],
    teachers_per_day: int,
    exam_time_start: str,
    exam_time_end: str
) -> Dict[str, Any]:

    result = {
        "assignments": [],
        "summary": {},
        "logs": [],
        "teacher_summary": {},
        "success": False,
        "detailed_explanation": []  # New field for frontend display
    }

    def add_log(message: str, level: str = "info"):
        log_entry = {
            "message": message,
            "level": level,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        result["logs"].append(log_entry)
        # Also add to detailed explanation for frontend
        result["detailed_explanation"].append({
            "type": level,
            "content": message,
            "timestamp": log_entry["timestamp"]
        })

    # Input validation
    try:
        start_date = datetime.strptime(exam_date_from, "%Y-%m-%d")
        end_date = datetime.strptime(exam_date_to, "%Y-%m-%d")
        
        if start_date > end_date:
            add_log("Error: Start date cannot be after end date", "error")
            result["summary"]["error"] = "Start date cannot be after end date"
            return result
            
        if teachers_per_day <= 0:
            add_log("Error: Teachers per day must be greater than 0", "error")
            result["summary"]["error"] = "Teachers per day must be greater than 0"
            return result
            
        if not teacher_names:
            add_log("Error: Teacher names list cannot be empty", "error")
            result["summary"]["error"] = "Teacher names list cannot be empty"
            return result
            
    except ValueError as e:
        add_log(f"Error parsing dates: {e}", "error")
        result["summary"]["error"] = f"Error parsing dates: {e}"
        return result
    
    current_date = start_date
    assignments = []
    teacher_index = 0
    
    # Validate and categorize teacher list
    valid_teachers = []
    external_teachers = []
    
    for teacher_name in teacher_names:
        teacher = teachers_collection.find_one({"name": teacher_name})
        if teacher:
            valid_teachers.append(teacher_name)
            add_log(f"✓ Found '{teacher_name}' in database", "success")
        else:
            external_teachers.append(teacher_name)
            add_log(f"ℹ '{teacher_name}' not in database, will be considered available all the time", "info")
    
    # Combine both lists - all teachers can be used for assignment
    all_teachers = valid_teachers + external_teachers
    
    if not all_teachers:
        add_log("Error: No teachers provided", "error")
        result["summary"]["error"] = "No teachers provided"
        return result
    
    # Teacher summary
    result["teacher_summary"] = {
        "database_teachers": len(valid_teachers),
        "external_teachers": len(external_teachers),
        "total_available": len(all_teachers),
        "database_teacher_names": valid_teachers,
        "external_teacher_names": external_teachers
    }
    
    # Add warnings and info to detailed explanation
    if len(external_teachers) > 0:
        add_log(f"Teacher Summary: {len(valid_teachers)} DB teachers, {len(external_teachers)} external teachers, {len(all_teachers)} total", "info")
    
    # Check if we have enough teachers for the requirement
    if len(all_teachers) < teachers_per_day:
        add_log(f"Warning: Only {len(all_teachers)} teachers available, but {teachers_per_day} required per day", "warning")
    
    # Assignment details for frontend
    assignment_details = f"""Assignment Details:
  Date Range: {exam_date_from} to {exam_date_to} ({(end_date - start_date).days + 1} days)
  Teachers Required Per Day: {teachers_per_day}
  Available Teachers: {len(all_teachers)}
  Exam Time: {exam_time_start} - {exam_time_end}
  Using {len(valid_teachers)} valid teachers out of {len(teacher_names)} requested"""
    
    add_log(assignment_details, "info")
    
    # For each day in range
    day_count = 0
    processed_days = []
    skipped_days = []
    
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        day_count += 1
        
        # Skip weekends (Saturday=5, Sunday=6)
        if current_date.weekday() >= 5:
            add_log(f"Skipping weekend: {date_str}", "info")
            skipped_days.append({
                "date": date_str,
                "day_of_week": current_date.strftime("%A"),
                "reason": "Weekend"
            })
            current_date += timedelta(days=1)
            continue
        
        add_log(f"Processing Day {day_count}: {date_str}", "info")
        
        # Get next N teachers (round-robin)
        day_teachers = []
        attempts = 0
        max_attempts = len(all_teachers) * 3  # Allow more attempts for better coverage
        day_attempts = []
        
        while len(day_teachers) < teachers_per_day and attempts < max_attempts:
            teacher_idx = (teacher_index + attempts) % len(all_teachers)
            teacher_name = all_teachers[teacher_idx]
            
            # Check availability
            if is_teacher_available(teacher_name, date_str, exam_time_start, exam_time_end):
                if teacher_name not in day_teachers:  # Avoid duplicates
                    day_teachers.append(teacher_name)
                    add_log(f"  ✓ Assigned {teacher_name} for {date_str}", "success")
                    day_attempts.append({
                        "teacher": teacher_name,
                        "status": "assigned",
                        "reason": "Available"
                    })
                else:
                    day_attempts.append({
                        "teacher": teacher_name,
                        "status": "skipped",
                        "reason": "Duplicate assignment"
                    })
            else:
                add_log(f"  ✗ Teacher {teacher_name} not available for {date_str}", "warning")
                day_attempts.append({
                    "teacher": teacher_name,
                    "status": "unavailable",
                    "reason": "Not available in this slot"
                })
            
            attempts += 1
        
        # Add assignment for this day
        if day_teachers:
            assignment = {
                "date": date_str,
                "day_of_week": current_date.strftime("%A"),
                "teachers": day_teachers,
                "required": teachers_per_day,
                "assigned": len(day_teachers),
                "exam_time": f"{exam_time_start} - {exam_time_end}",
                "status": "success" if len(day_teachers) == teachers_per_day else "partial",
                "attempts": day_attempts
            }
            assignments.append(assignment)
            processed_days.append(assignment)
            
            status = "✓ Fully Staffed" if len(day_teachers) == teachers_per_day else f"⚠ Under Staffed ({len(day_teachers)}/{teachers_per_day})"
            add_log(f"  {status} - Successfully assigned {len(day_teachers)} teachers for {date_str}", "success" if len(day_teachers) == teachers_per_day else "warning")
        else:
            add_log(f"  ❌ Critical: Could not assign any teachers for {date_str}", "error")
            failed_assignment = {
                "date": date_str,
                "day_of_week": current_date.strftime("%A"),
                "teachers": [],
                "required": teachers_per_day,
                "assigned": 0,
                "exam_time": f"{exam_time_start} - {exam_time_end}",
                "status": "failed",
                "attempts": day_attempts
            }
            assignments.append(failed_assignment)
            processed_days.append(failed_assignment)
        
        # Move to next day
        current_date += timedelta(days=1)
        teacher_index = (teacher_index + teachers_per_day) % len(all_teachers)
    
    # Summary
    successful_days = sum(1 for a in assignments if a.get("assigned", 0) > 0)
    total_required = len(assignments) * teachers_per_day
    total_assigned = sum(a.get("assigned", 0) for a in assignments)
    coverage_rate = (total_assigned/total_required*100) if total_required > 0 else 0
    
    result["summary"] = {
        "total_days_processed": len(assignments),
        "successful_days": successful_days,
        "total_teachers_required": total_required,
        "total_teachers_assigned": total_assigned,
        "coverage_rate": round(coverage_rate, 1),
        "exam_period": {
            "start_date": exam_date_from,
            "end_date": exam_date_to,
            "total_days": (end_date - start_date).days + 1,
            "weekdays": len(assignments),
            "weekends": len(skipped_days)
        },
        "requirements": {
            "teachers_per_day": teachers_per_day,
            "exam_time": f"{exam_time_start} - {exam_time_end}"
        }
    }
    
    # Add final summary to detailed explanation
    final_summary = f"""=== Assignment Summary ===
  Total Days Processed: {len(assignments)}
  Successful Days: {successful_days}
  Total Teachers Required: {total_required}
  Total Teachers Assigned: {total_assigned}
  Coverage Rate: {coverage_rate:.1f}%
  Total assignments created: {len(assignments)}"""
    
    add_log(final_summary, "info")
    
    result["assignments"] = assignments
    result["processed_days"] = processed_days
    result["skipped_days"] = skipped_days
    result["success"] = True
    
    # For backward compatibility, also return just the assignments list
    # This allows the existing controller to work while providing rich data
    result["assignments_list"] = assignments  # For backward compatibility
    
    return result

def save_invigilator_assignment(assignment_data: Dict):
    result = invigilator_collection.insert_one(assignment_data)
    return str(result.inserted_id)

def get_invigilator_assignments():
    return list(invigilator_collection.find({}, {"_id": 0}))
