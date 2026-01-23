from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.services.invigilator_service import assign_invigilators_simple, save_invigilator_assignment, get_invigilator_assignments

invig_bp = Blueprint("invigilators", __name__)

@invig_bp.post("/assign")
@jwt_required()
def assign_invigilators():
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ["exam_date_from", "exam_date_to", "teacher_names", "teachers_per_day", "exam_time_start", "exam_time_end"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        
        # Parse and run assignment
        assignments = assign_invigilators_simple(
            exam_date_from=data["exam_date_from"],
            exam_date_to=data["exam_date_to"],
            teacher_names=data["teacher_names"],
            teachers_per_day=data["teachers_per_day"],
            exam_time_start=data["exam_time_start"],
            exam_time_end=data["exam_time_end"]
        )
        
        # Save to database
        assignment_doc = {
            "exam_date_from": data["exam_date_from"],
            "exam_date_to": data["exam_date_to"],
            "teachers_per_day": data["teachers_per_day"],
            "exam_time_start": data["exam_time_start"],
            "exam_time_end": data["exam_time_end"],
            "assignments": assignments,
            "created_at": datetime.now().isoformat()
        }
        
        assignment_id = save_invigilator_assignment(assignment_doc)
        
        return jsonify({
            "success": True,
            "assignment_id": assignment_id,
            "assignments": assignments
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@invig_bp.get("/assignments")
@jwt_required()
def get_assignments():
    """Get all invigilator assignments"""
    try:
        assignments = get_invigilator_assignments()
        return jsonify({
            "success": True,
            "count": len(assignments),
            "assignments": assignments
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
