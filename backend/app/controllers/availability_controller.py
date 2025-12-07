from flask import Blueprint, jsonify, current_app
from app.services.availability_service import post_availability_service
from app.utils.db import availability_collection

availability_bp = Blueprint("availability", __name__)

@availability_bp.post("/submit")
def post_availability():
    return post_availability_service()

@availability_bp.get("/all")
def get_all_availability():
    records = list(availability_collection.find())
    for r in records:
        r["_id"] = str(r["_id"]) 

    return jsonify(records), 200