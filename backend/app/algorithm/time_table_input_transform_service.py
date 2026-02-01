import json
import os
from flask import request, jsonify
from pydantic import ValidationError

def is_lab_teacher(teacher_name, teachers_data):
    """Check if a teacher is a lab teacher based on their subject"""
    for teacher in teachers_data:
        if teacher.get('name') == teacher_name:
            subject = teacher.get('subject', '')
            if isinstance(subject, list):
                return any(s.lower().endswith('_lab') for s in subject)
            return subject.lower().endswith('_lab')
    return False

def combine_lab_availability(teacherunavailability_data, teachers_data):
    """Combine availability of all lab teachers into a single 'Labs' entry"""
    lab_slots = set()
    non_lab_availability = []
    
    for ua in teacherunavailability_data:
        teacher_name = ua['name']
        if is_lab_teacher(teacher_name, teachers_data):
            # Collect slots for combined availability
            lab_slots.update(ua["slots"])
        else:
            # Non-lab teacher, keep as is
            non_lab_availability.append(ua)
    
    # Start with non-lab teachers
    combined_availability = non_lab_availability.copy()
    
    # Add combined "Labs" entry if there are lab teachers
    if lab_slots:
        combined_availability.append({
            'name': 'Labs',
            'slots': sorted(list(lab_slots))
        })
    
    return combined_availability

def transform_input(input_data=None):
    try:
        if input_data is None:
            data = request.json
        else:
            data = input_data
        
        if not data:
            print("Error: No data provided")
            return False
            
        # Validate required fields
        required_fields = ['studentgroups', 'teacherunavailability', 'teachers']
        for field in required_fields:
            if field not in data:
                print(f"Error: Missing required field '{field}'")
                return False
                
    except Exception as e:
        print(f"Error getting input data: {e}")
        return False
    
    print(f"Transforming input data: {data}")  # For debugging purposes
    output = []

    # Student Groups
    output.append('studentgroups')
    if 'studentgroups' in data:
        for sg in data['studentgroups']:
            line = [sg['group']]
            for s, c in sg['subjects'].items():
                line.append(s)
                line.append(str(c))
            output.append(" ".join(line))
    output.append("end")

    # Teachers
    output.append("teachers")
    if 'teachers' in data:
        for t in data.get("teachers", []):
            subject = t["subject"]
            if isinstance(subject, list):
                subject = ", ".join(subject)
            output.append(f"{t['name']} {subject}")
    output.append("end")

    # Unavailability - use combined lab availability
    output.append("teacherunavailability")
    if 'teacherunavailability' in data and 'teachers' in data:
        # Get combined availability for labs
        combined_availability = combine_lab_availability(
            data["teacherunavailability"], 
            data["teachers"]
        )
        
        # Write non-lab teachers and combined labs availability
        for ua in combined_availability:
            output.append(f"{ua['name']} " + " ".join(str(s) for s in ua["slots"]))
    output.append("end")

    try:
        INPUT_FILE_PATH = "input.txt"
        with open(INPUT_FILE_PATH, "w") as f:
            f.write("\n".join(output))
        print(f"Successfully wrote input file to {INPUT_FILE_PATH}")
        return True
    except Exception as e:
        print(f"Error writing input file: {e}")
        return False