from flask import Blueprint, jsonify, request
import logging

from app.algorithm.time_table_input_transform_service import transform_input
from app.algorithm.scheduler_main import SchedulerMain
from app.algorithm.input_data import InputData

# Set up logging
logger = logging.getLogger(__name__)

generation_bp = Blueprint("generation", __name__)

@generation_bp.post("/time-table")
def generate_time_table():
    try:
        if not transform_input():
            return jsonify({"message": "Failed to transform input"}), 500
        
        # Run the scheduler directly within Flask context (not as subprocess)
        try:
            config_data = InputData("/tmp/input.txt")
            scheduler = SchedulerMain(config_data)
            
            # Get the final solution and save it
            if SchedulerMain.final_son is not None:
                SchedulerMain.final_son.print_time_table()
                return jsonify({"message": "Time table generated successfully"}), 200
            else:
                logger.warning("Scheduler completed but no valid solution found")
                return jsonify({"message": "No valid timetable solution found"}), 400
                
        except Exception as e:
            logger.error(f"Error running scheduler: {str(e)}", exc_info=True)
            return jsonify({"message": f"Scheduler error: {str(e)}"}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in generate_time_table: {str(e)}", exc_info=True)
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500