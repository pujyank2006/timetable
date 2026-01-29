import json
import os
from flask import request, jsonify
from pydantic import ValidationError

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
        required_fields = ['studentgroups', 'teacherunavailability']
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

    # Unavailability
    output.append("teacherunavailability")
    if 'teacherunavailability' in data:
        for ua in data["teacherunavailability"]:
            output.append(f"{ua['name']} " + " ".join(str(s) for s in ua["slots"]))
    output.append("end")

    try:
        INPUT_FILE_PATH = "/tmp/input.txt"
        with open(INPUT_FILE_PATH, "w") as f:
            f.write("\n".join(output))
        print(f"Successfully wrote input file to {INPUT_FILE_PATH}")
        return True
    except Exception as e:
        print(f"Error writing input file: {e}")
        return False