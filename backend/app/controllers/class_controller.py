from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.class_service import fetch_classes

class_bp = Blueprint("classes", __name__)

@class_bp.get("/classes")
@jwt_required()
def get_classes():
    current_user = get_jwt_identity()
    if not current_user:
        return jsnoify({
            "message": "No user"
        })
    
    return jsonify({
        "success": True,
        "data": fetch_classes()
    })
