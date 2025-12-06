from flask import Blueprint, jsonify, request
from app.services.teacher_service import fetch_teachers
from app.services.teacher_service import generate_token_for_teacher
from app.services.teacher_service import send_email

teacher_bp = Blueprint("teachers", __name__)

@teacher_bp.get("/teachers")
def get_teachers():
    return jsonify({
        "success": True,
        "data": fetch_teachers()
    })

@teacher_bp.post("/teachers/generate-link")
def create_and_send__link():
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
        send_email(teacher_email, token)
    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

    return jsonify({
        "message": "Link sent successfully",
        "TOKEN": token
    }), 200