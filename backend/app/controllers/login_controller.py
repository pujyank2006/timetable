from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.config import Config

user_bp = Blueprint("users", __name__)

@user_bp.post("/login")
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        password = data.get('password')
        
        if not password:
            return jsonify({"message": "Password is required"}), 400
        
        if password != Config.ADMIN_PASSWORD:
            return jsonify({"message": "Invalid password"}), 401
        
        access_token = create_access_token(identity="admin")
        
        return jsonify({
            "": "Login successful",
            "user": "admin",
            "token": access_token
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 500
