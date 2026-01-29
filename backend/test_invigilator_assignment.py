#!/usr/bin/env python3
"""
Test script to verify the invigilator assignment functionality with availability checking.
"""

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.invigilator_service import (
    assign_invigilators_simple,
    is_teacher_available,
    calculate_slot_number
)

def test_slot_calculation():
    """Test the slot calculation function."""
    print("=== Testing Slot Calculation ===\n")
    
    # Test cases
    test_cases = [
        ("2024-01-15", "09:00"),  # Monday 9 AM -> slot 0
        ("2024-01-15", "10:00"),  # Monday 10 AM -> slot 1
        ("2024-01-16", "09:00"),  # Tuesday 9 AM -> slot 7
        ("2024-01-20", "09:00"),  # Saturday -> invalid (-1)
        ("2024-01-15", "08:00"),  # Before teaching hours -> invalid (-1)
        ("2024-01-15", "16:00"),  # After teaching hours -> invalid (-1)
    ]
    
    for date, time in test_cases:
        slot = calculate_slot_number(date, time)
        print(f"Date: {date}, Time: {time} -> Slot: {slot}")
    
    print()

def test_teacher_availability():
    """Test teacher availability checking."""
    print("=== Testing Teacher Availability ===\n")
    
    # Test cases with different teachers and times
    test_cases = [
        ("Pujyank", "2024-01-15", "09:00"),  # Database teacher
        ("Ekshwith", "2024-01-15", "10:00"),  # Database teacher
        ("NonExistentTeacher", "2024-01-15", "09:00"),  # External teacher
        ("ExternalInvigilator", "2024-01-15", "14:00"),  # Another external teacher
    ]
    
    for teacher_name, date, time in test_cases:
        available = is_teacher_available(teacher_name, date, time, "11:00")
        print(f"Teacher: {teacher_name}, Date: {date}, Time: {time} -> Available: {available}")
    
    print()

def test_invigilator_assignment():
    """Test the full invigilator assignment process with different scenarios."""
    print("=== Testing Invigilator Assignment ===\n")
    
    # Test Case 1: Basic assignment
    print("--- Test Case 1: Basic Assignment ---")
    teacher_names = ["Pujyank", "Ekshwith", "Bhavani", "Ambarish"]
    exam_date_from = "2024-01-15"
    exam_date_to = "2024-01-17"
    teachers_per_day = 2
    exam_time_start = "09:00"
    exam_time_end = "11:00"
    
    assignments = assign_invigilators_simple(
        exam_date_from=exam_date_from,
        exam_date_to=exam_date_to,
        teacher_names=teacher_names,
        teachers_per_day=teachers_per_day,
        exam_time_start=exam_time_start,
        exam_time_end=exam_time_end
    )
    
    print(f"Generated {len(assignments)} assignments:")
    for assignment in assignments:
        status = "✓" if assignment.get("assigned", 0) >= assignment.get("required", 0) else "❌"
        print(f"  {status} {assignment['date']} ({assignment.get('day_of_week', 'N/A')}): "
              f"{assignment.get('assigned', 0)}/{assignment.get('required', 0)} teachers")
        if assignment.get('teachers'):
            print(f"      Teachers: {', '.join(assignment['teachers'])}")
    print()
    
    # Test Case 2: Higher teacher requirement
    print("--- Test Case 2: Higher Teacher Requirement ---")
    teachers_per_day = 3
    
    assignments2 = assign_invigilators_simple(
        exam_date_from="2024-01-15",
        exam_date_to="2024-01-16",
        teacher_names=teacher_names,
        teachers_per_day=teachers_per_day,
        exam_time_start="10:00",
        exam_time_end="12:00"
    )
    
    print(f"Generated {len(assignments2)} assignments with {teachers_per_day} teachers per day:")
    for assignment in assignments2:
        status = "✓" if assignment.get("assigned", 0) >= assignment.get("required", 0) else "❌"
        print(f"  {status} {assignment['date']}: {assignment.get('assigned', 0)}/{assignment.get('required', 0)} teachers")
    print()
    
    # Test Case 3: Extended date range (including weekend)
    print("--- Test Case 3: Extended Date Range (Including Weekend) ---")
    assignments3 = assign_invigilators_simple(
        exam_date_from="2024-01-15",
        exam_date_to="2024-01-21",  # Includes weekend
        teacher_names=["Pujyank", "Ekshwith"],
        teachers_per_day=1,
        exam_time_start="09:00",
        exam_time_end="11:00"
    )
    
    print(f"Generated {len(assignments3)} assignments for extended week:")
    for assignment in assignments3:
        status = "✓" if assignment.get("assigned", 0) >= assignment.get("required", 0) else "❌"
        print(f"  {status} {assignment['date']} ({assignment.get('day_of_week', 'N/A')}): "
              f"{assignment.get('assigned', 0)}/{assignment.get('required', 0)} teachers")
    print()
    
    # Test Case 4: Invalid input validation
    print("--- Test Case 4: Input Validation ---")
    
    # Invalid date range
    print("Testing invalid date range (start > end):")
    invalid_assignments = assign_invigilators_simple(
        exam_date_from="2024-01-20",
        exam_date_to="2024-01-15",  # Invalid: end before start
        teacher_names=["Pujyank"],
        teachers_per_day=1,
        exam_time_start="09:00",
        exam_time_end="11:00"
    )
    print(f"Result: {len(invalid_assignments)} assignments (should be 0)")
    
    # Invalid teachers per day
    print("\nTesting invalid teachers per day (0):")
    invalid_assignments2 = assign_invigilators_simple(
        exam_date_from="2024-01-15",
        exam_date_to="2024-01-16",
        teacher_names=["Pujyank"],
        teachers_per_day=0,  # Invalid
        exam_time_start="09:00",
        exam_time_end="11:00"
    )
    print(f"Result: {len(invalid_assignments2)} assignments (should be 0)")
    
    # Empty teacher list
    print("\nTesting empty teacher list:")
    invalid_assignments3 = assign_invigilators_simple(
        exam_date_from="2024-01-15",
        exam_date_to="2024-01-16",
        teacher_names=[],  # Invalid
        teachers_per_day=1,
        exam_time_start="09:00",
        exam_time_end="11:00"
    )
    print(f"Result: {len(invalid_assignments3)} assignments (should be 0)")
    print()
    
    # Test Case 5: External Teachers (not in DB)
    print("--- Test Case 5: External Teachers (Not in Database) ---")
    mixed_teachers = ["Pujyank", "ExternalInvigilator1", "Ekshwith", "ExternalInvigilator2"]
    assignments5 = assign_invigilators_simple(
        exam_date_from="2024-01-15",
        exam_date_to="2024-01-17",
        teacher_names=mixed_teachers,
        teachers_per_day=2,
        exam_time_start="09:00",
        exam_time_end="11:00"
    )
    
    print(f"Generated {len(assignments5)} assignments with mixed teacher types:")
    for assignment in assignments5:
        status = "✓" if assignment.get("assigned", 0) >= assignment.get("required", 0) else "❌"
        print(f"  {status} {assignment['date']}: {assignment.get('assigned', 0)}/{assignment.get('required', 0)} teachers")
        if assignment.get('teachers'):
            print(f"      Teachers: {', '.join(assignment['teachers'])}")
    print()
    
    # Test Case 6: Only External Teachers
    print("--- Test Case 6: Only External Teachers ---")
    external_only = ["ExternalInvigilator1", "ExternalInvigilator2", "ExternalInvigilator3"]
    assignments6 = assign_invigilators_simple(
        exam_date_from="2024-01-15",
        exam_date_to="2024-01-16",
        teacher_names=external_only,
        teachers_per_day=2,
        exam_time_start="10:00",
        exam_time_end="12:00"
    )
    
    print(f"Generated {len(assignments6)} assignments with external teachers only:")
    for assignment in assignments6:
        status = "✓" if assignment.get("assigned", 0) >= assignment.get("required", 0) else "❌"
        print(f"  {status} {assignment['date']}: {assignment.get('assigned', 0)}/{assignment.get('required', 0)} teachers")
        if assignment.get('teachers'):
            print(f"      Teachers: {', '.join(assignment['teachers'])}")

if __name__ == "__main__":
    test_slot_calculation()
    test_teacher_availability()
    test_invigilator_assignment()
    print("=== Test Complete ===")