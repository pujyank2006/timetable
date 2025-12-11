from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services.availability_service import post_availability_service
from app.utils.db import availability_collection

availability_bp = Blueprint("availability", __name__)

@availability_bp.post("/submit")
@jwt_required()
def post_availability():
    current_user = get_jwt_identity()
    if not current_user:
        return jsnoify({
            "message": "No user"
        })
    return post_availability_service()

@availability_bp.get("/all")
@jwt_required()
def get_all_availability():
    current_user = get_jwt_identity()
    if not current_user:
        return jsnoify({
            "message": "No user"
        })
    records = list(availability_collection.find())
    for r in records:
        r["_id"] = str(r["_id"]) 

    return jsonify(records), 200

@availability_bp.delete("/reset")
@jwt_required()
def reset_availability():
    try:
        current_user = get_jwt_identity()
        print(f"DEBUG: User '{current_user}' resetting availability")
        
        result = availability_collection.delete_many({})
        
        return jsonify({
            "message": "Availability data reset successfully",
            "deleted_count": result.deleted_count
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
