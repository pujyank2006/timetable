from flask import Blueprint, jsonify, request
from app.services.teacher_service import fetch_teachers
from app.services.teacher_service import generate_token_for_teacher
from app.services.teacher_service import send_email
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

teacher_bp = Blueprint("teachers", __name__)

@teacher_bp.get("/teachers")
@jwt_required()
def get_teachers():
    current_user = get_jwt_identity()
    if not current_user:
        return jsnoify({
            "message": "No user"
        })
    return jsonify({
        "success": True,
        "data": fetch_teachers()
    })

@teacher_bp.post("/teachers/generate-link")
@jwt_required()
def create_and_send__link():
    current_user = get_jwt_identity()
    if not current_user:
        return jsnoify({
            "message": "No user"
        })
    data = request.json
    teacher_id = data.get("teacher_id")

    if not teacher_id:
        return jsonify({"error": "Missing required field: teacher_id"}), 400
    
    token = generate_token_for_teacher(teacher_id)
    teacher_email = next(
        (teacher['email'] for teacher in fetch_teachers() if teacher['id'] == teacher_id),
        None
    )

    if not teacher_email:
        return jsonify({"error": f"Teacher with ID {teacher_id} not found or email is missing."}), 404
    
    try:
        send_email(teacher_email, token, teacher_id)
    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

    return jsonify({
        "message": "Link sent successfully",
        "TOKEN": token
    }), 200