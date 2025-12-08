from flask import request, jsonify
from pydantic import ValidationError
from bson import ObjectId

from app.utils.db import availability_collection
from app.schema.availability_schema import Availability
from app.config import Config

def post_availability_service():
    try:
        data = Availability(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    # 1. Extract teacher_id and prepare data
    teacher_id = data.teacher_id
    availability_data = data.dict()

    # Validate slots: prevent marking all slots unavailable or exceeding allowed fraction
    try:
        slots_list = list(dict.fromkeys([int(s) for s in availability_data.get('slots', [])]))
    except Exception:
        return jsonify({"error": "Slots must be a list of integers"}), 400

    total_slots = int(Config.SLOTS_PER_DAY) * int(Config.DAYS_PER_WEEK)
    max_fraction = float(Config.MAX_UNAVAILABLE_FRACTION)
    max_allowed = int(total_slots * max_fraction)

    if len(slots_list) >= total_slots:
        return jsonify({"error": "Invalid submission: you cannot mark every slot as unavailable."}), 400

    if len(slots_list) > max_allowed:
        return jsonify({
            "error": "Too many unavailable slots requested.",
            "details": f"You may mark at most {max_allowed} out of {total_slots} slots unavailable ({int(max_fraction*100)}%)."
        }), 400

    # Normalise slots back into the payload
    availability_data['slots'] = slots_list

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