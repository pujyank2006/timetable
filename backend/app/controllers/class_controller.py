from flask import Blueprint, jsonify
from app.services.class_service import fetch_classes

class_bp = Blueprint("classes", __name__)

@class_bp.get("/classes")
def get_classes():
    return jsonify({
        "success": True,
        "data": fetch_classes()
    })
