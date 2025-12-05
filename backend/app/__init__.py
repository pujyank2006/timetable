from flask import Flask
from app.controllers.subject_controller import subject_bp
from app.controllers.teacher_controller import teacher_bp
from app.controllers.availability_controller import availability_bp

def create_app():
    app = Flask(__name__)

    # Route for subjects
    app.register_blueprint(subject_bp, url_prefix="/api")

    # Route for teachers
    app.register_blueprint(teacher_bp, url_prefix="/api")

    # Route for availability
    app.register_blueprint(availability_bp, url_prefix="/availability")

    return app
