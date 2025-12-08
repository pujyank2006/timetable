from flask import Blueprint, jsonify, request
import subprocess
import os
import sys

from app.algorithm.time_table_input_transform_service import transform_input

generation_bp = Blueprint("generation", __name__)

@generation_bp.post("/time-table")
def generate_time_table():
    if transform_input():
        result = subprocess.run(
            [sys.executable, "-m", "app.algorithm.scheduler_main"],
            capture_output=True,
            text=True
        )
        return jsonify({
            "message": "Time table generated"
        })
    else:
        return jsonify({"message": "Failed to transform input"}), 500