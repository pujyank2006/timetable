from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

logout_bp = Blueprint("logout", __name__)

@logout_bp.post("/logout")
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    if not current_user:
        return jsnoify({
            "message": "No user"
        })
    response = make_response(jsonify({"message": "Logout successful"}))
    # Overwrite the cookie with an empty value and immediate expiry
    response.set_cookie("access_token_cookie", "", expires=0)
    return response