from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
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
        
        if not check_password_hash(Config.ADMIN_PASSWORD, password):
            return jsonify({"message": "Invalid password"}), 401
        
        # 1. Create the token
        access_token = create_access_token(identity="admin")
        
        # 2. Create a response object (but don't return it yet)
        # notice we DO NOT send the 'token' in this JSON body anymore
        # Also include the token in the JSON response so a same-origin frontend
        # can store a client-side cookie or local state. (We keep the HttpOnly
        # cookie as well for the API domain.)
        response = make_response(jsonify({
            "message": "Login successful",
            "user": "admin"
        }))

        # 3. Set the token in a secure cookie
        # This cookie cannot be accessed by client-side JavaScript (HttpOnly)
        response.set_cookie(
            "access_token_cookie",  # Default name expected by Flask-JWT-Extended
            value=access_token_cookie,
            max_age=7 * 24 * 60 * 60, # 7 days (should match your token expiry)
            httponly=True,  # CRITICAL: Prevents XSS attacks (JS cannot read this)
            secure=True,   # Set to True if using HTTPS (Production), False for Localhost
            samesite="None", # CRITICAL: Prevents CSRF (Cookie only sent on nav)
            path="/"        # Available across the whole app
        )

        return response, 200
        
    except Exception as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 500