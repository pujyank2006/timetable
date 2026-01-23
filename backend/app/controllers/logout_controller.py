from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies

logout_bp = Blueprint("logout", __name__)

@logout_bp.post("/logout")
@jwt_required()
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    unset_jwt_cookies(response)
    return response