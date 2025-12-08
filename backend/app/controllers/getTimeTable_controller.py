from flask import Blueprint, jsonify
from app.utils.db import time_table_collection

getTimeTable_bp = Blueprint("getTimeTable", __name__)

@getTimeTable_bp.get("/time-tables")
def get_timetables():
    timetables = list(time_table_collection.find({}, {"_id": 0})) 
    return jsonify({"data": timetables})