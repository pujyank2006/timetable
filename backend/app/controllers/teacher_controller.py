from flask import Blueprint, jsonify
from app.services.teacher_service import fetch_teachers
from app.services.teacher_service import generate_token_for_teacher

teacher_bp = Blueprint("teachers", __name__)

@teacher_bp.get("/teachers")
def get_teachers():
    return jsonify({
        "success": True,
        "data": fetch_teachers()
    })

@teacher_bp.post("/teachers/generate-link/<teacher_id>")
def create_link(teacher_id):
    token = generate_token_for_teacher(teacher_id)
    link = f"https://yourfrontend.com/availability?token={token}"
    
    return jsonify({
        "success": True,
        "link": link
})