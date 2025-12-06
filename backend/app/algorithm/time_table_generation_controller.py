from flask import Blueprint, jsonify
import subprocess
import os
from app.algorithm.time_table_input_transform_service import transform_input

generation_bp = Blueprint("generation", __name__)

@generation_bp.get("/time-table")
def generate_time_table():
    if transform_input():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        SCRIPT_PATH = os.path.abspath(
            os.path.join(BASE_DIR, "..", "algorithm", "scheduler_main.py")
        )

        result = subprocess.run(
            ["python", SCRIPT_PATH],
            capture_output = True,
            text = True
        )

        return jsonify({
            "message": "Time table generated",
            "stdout": result.stdout,
            "stderr": result.stderr
        })
    else:
        return jsonify({"message": "Failed to transform input"}), 500