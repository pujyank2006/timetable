from flask import Blueprint, jsonify
import subprocess
import os
import sys

from app.algorithm.time_table_input_transform_service import transform_input

generation_bp = Blueprint("generation", __name__)

@generation_bp.get("/time-table")
def generate_time_table():
    if transform_input():
        result = subprocess.run(
            [sys.executable, "-m", "app.algorithm.scheduler_main"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
        return jsonify({
            "message": "Time table generated",
            "stdout": result.stdout,
            "stderr": result.stderr
        })
    else:
        return jsonify({"message": "Failed to transform input"}), 500