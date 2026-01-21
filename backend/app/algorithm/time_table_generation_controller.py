from flask import Blueprint, jsonify, request
import os
import sys

from app.algorithm.time_table_input_transform_service import transform_input
from app.algorithm.input_data import InputData
from app.algorithm.scheduler_main import SchedulerMain

generation_bp = Blueprint("generation", __name__)

@generation_bp.post("/time-table")
def generate_time_table():
    try:
        # Transform input data and write to file
        if not transform_input():
            return jsonify({"message": "Failed to transform input"}), 400
        
        # Get the input file path (should be in current directory or specified location)
        input_file_path = os.path.join(os.getcwd(), "input.txt")
        
        # Check if input file exists
        if not os.path.exists(input_file_path):
            return jsonify({"message": "Input file not created"}), 400
        
        try:
            # Initialize config and run scheduler directly (no subprocess)
            config_data = InputData(input_file_path)
            
            if config_data.nostudentgroup == 0:
                return jsonify({
                    "message": "No student groups found in input data"
                }), 400
            
            # Run the scheduler algorithm
            scheduler = SchedulerMain(config_data)
            
            return jsonify({
                "message": "Time table generated successfully",
                "status": "success"
            }), 201
            
        except Exception as e:
            return jsonify({
                "message": f"Error during scheduling: {str(e)}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "message": f"Error: {str(e)}"
        }), 500