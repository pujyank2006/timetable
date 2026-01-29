from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.availability_update_service import (
    update_availability_after_timetable,
    get_teacher_availability_status
)

availability_update_bp = Blueprint("availability_update", __name__)

@availability_update_bp.post("/availability/update-after-timetable")
@jwt_required()
def update_availability():
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"message": "No user"}), 401
        
        result = update_availability_after_timetable()
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating availability: {str(e)}"
        }), 500

@availability_update_bp.get("/availability/status")
@jwt_required()
def get_availability_status():
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"message": "No user"}), 401
        
        result = get_teacher_availability_status()
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching availability status: {str(e)}"
        }), 500