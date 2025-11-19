from flask import Flask
from app.controllers.subject_controller import subject_bp
from app.controllers.teacher_controller import teacher_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints (route groups)
    app.register_blueprint(subject_bp, url_prefix="/api")
    app.register_blueprint(teacher_bp, url_prefix="/api")

    return app
