import json
from flask import request, jsonify

def transform_input():
    try:
        data = request.json
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    output = []

    # Student Groups
    output.append('studentgroups')
    for sg in data['studentgroups']:
        line = [sg['group']]
        for s, c in sg['subjects'].items():
            line.append(s)
            line.append(str(c))
        output.append(" ".join(line))
    output.append("end")

    # Teacher
    output.append("teachers")
    for t in data['teachers']:
        output.append(f"{t['name']} {t['subject']}")
    output.append("end")

    # Unavailability
    output.append("teacherunavailability")
    for ua in data["teacherunavailability"]:
        output.append(f"{ua['name']} " + " ".join(str(s) for s in ua["slots"]))
    output.append("end")

    try: 
        INPUT_FILE_PATH = "input.txt"
        with open(INPUT_FILE_PATH, "w") as f:
            f.write("\n".join(output))
        return True
    except Exception as e:
        return False