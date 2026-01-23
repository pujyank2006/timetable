from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        
        if not check_password_hash(Config.ADMIN_PASSWORD, password):
            return jsonify({"message": "Invalid password"}), 401
        
        access_token = create_access_token(identity="admin")
        response = make_response(jsonify({
            "message": "Login successful",
            "user": "admin"
        }))

        response.set_cookie(
            "access_token_cookie",
            value=access_token,
            max_age=7 * 24 * 60 * 60,
            httponly=True,
            secure=True,
            samesite="None", 
            path="/"
        )

        return response, 200
        
    except Exception as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 500

@user_bp.get("/me")
@jwt_required()
def me():
    try:
        identity = get_jwt_identity()
        return jsonify({
            "user": identity
        })
    except Exception as e:
        return jsonify({"message": f"Failed to get user info: {str(e)}"}), 500