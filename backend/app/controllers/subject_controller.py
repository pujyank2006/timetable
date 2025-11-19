from flask import Blueprint, jsonify
from app.services.subject_service import fetch_subjects

subject_bp = Blueprint("subjects", __name__)

@subject_bp.get("/subjects")
def get_subjects():
    return jsonify({
        "success": True,
        "data": fetch_subjects()
    })
