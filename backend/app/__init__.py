from flask import Flask
from app.controllers.subject_controller import subject_bp
from app.controllers.teacher_controller import teacher_bp
from app.controllers.availability_controller import availability_bp
from app.algorithm.time_table_generation_controller import generation_bp

def create_app():
    app = Flask(__name__)

    # Route for subjects
    app.register_blueprint(subject_bp, url_prefix="/api")

    # Route for teachers
    app.register_blueprint(teacher_bp, url_prefix="/api")

    # Route for availability
    app.register_blueprint(availability_bp, url_prefix="/availability")

    # Route for time table generation
    app.register_blueprint(generation_bp, url_prefix="/generate")
    return app
