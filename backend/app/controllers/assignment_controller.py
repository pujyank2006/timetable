from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.db import classes_collection
from app.utils.db import teachers_collection
from app.utils.db import input_data_collection

assign_bp = Blueprint("assignments", __name__)

@assign_bp.post("/assign")
@jwt_required()
def post_assignments():
    data = request.get_json()

    class_name = data.get("class_name")
    teachers = data.get("teachers", [])

    if not class_name or not teachers:
        return jsonify({"error": "class_name and teachers are required"}), 400
    
    # Add class into class collection
    classes_collection.update_one(
        {
            "name": class_name
        },
        { "$setOnInsert": {"name": class_name} },
        upsert = True
    )

    # Add teachers
    for t in teachers:
        teachers_collection.update_one(
            {"id": t["id"]},
            {
                "$setOnInsert": {
                    "name": t["name"],
                    "email": t["email"],
                    "phone": t["mobileno"],    
                },
                "$addToSet": {
                    "subjects": { "$each": t["subject"] }
                }
            },
            upsert = True
        )
    
    # Adding assignments
    input_data_collection.insert_one({
        "class_name": class_name,
        "teachers": teachers
    })

    return jsonify({
        "message": "Class and teachers saved successfully"
    }), 201

@assign_bp.get("/input-data")
@jwt_required()
def get_input_data():
    try:
        input_data = list(input_data_collection.find({}, {"_id": 0}))
        
        # Get unique class names
        class_names = list(set([item.get("class_name") for item in input_data if item.get("class_name")]))
        
        return jsonify({
            "success": True,
            "data": input_data,
            "classes": sorted(class_names)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500