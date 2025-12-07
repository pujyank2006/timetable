from flask import request, jsonify
from pydantic import ValidationError
from bson import ObjectId

from app.utils.db import availability_collection
from app.schema.availability_schema import Availability

def post_availability_service():
    try:
        data = Availability(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    # 1. Extract teacher_id and prepare data
    teacher_id = data.teacher_id
    availability_data = data.dict()

    # 2. Mark as submitted
    availability_data['submitted'] = True

    existing = availability_collection.find_one({"teacher_id": teacher_id})

    if existing:
        # 3. Update existing document
        update_result = availability_collection.update_one(
            {"teacher_id": teacher_id},
            {"$set": availability_data} 
        )
        
        updated_doc = availability_collection.find_one({"teacher_id": teacher_id})
        
        updated_doc['_id'] = str(updated_doc['_id'])
        
        return jsonify({ "message": "Updated the availability" }), 200

    insert_result = availability_collection.insert_one(availability_data)
    
    inserted_id = str(insert_result.inserted_id)
    
    availability_data['_id'] = inserted_id
    
    return jsonify({ "message": "Inserted the availability" }), 201