from flask import Blueprint, jsonify
from app.utils.db import time_table_collection
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

getTimeTable_bp = Blueprint("getTimeTable", __name__)

@getTimeTable_bp.get("/time-tables")
@jwt_required()
def get_timetables():
    current_user = get_jwt_identity()
    if not current_user:
        return jsnoify({
            "message": "No user"
        })
    
    timetables = list(time_table_collection.find({}, {"_id": 0})) 
    return jsonify({"data": timetables})