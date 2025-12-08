from flask import Blueprint, jsonify, make_response

logout_bp = Blueprint("logout", __name__)

@logout_bp.post("/logout")
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    # Overwrite the cookie with an empty value and immediate expiry
    response.set_cookie("access_token_cookie", "", expires=0)
    return response