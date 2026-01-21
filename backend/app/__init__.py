from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Config
from app.controllers.class_controller import class_bp
from app.controllers.teacher_controller import teacher_bp
from app.controllers.availability_controller import availability_bp
from app.controllers.login_controller import user_bp
from app.controllers.logout_controller import logout_bp
from app.controllers.getTimeTable_controller import getTimeTable_bp
from app.algorithm.time_table_generation_controller import generation_bp
from app.controllers.assignment_controller import assign_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Allow CORS from the frontend, include Authorization header and OPTIONS method
    CORS(
        app,
        resources={r"/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000", "https://timetable-one-alpha.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }}
    )
    
    # Initialize JWT
    jwt = JWTManager(app)

    @app.route("/")
    def home():
        return "Hello from Flask on Vercel!"

    # Route for users/login or logout
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(logout_bp, url_prefix="/user")

    # Route for classes
    app.register_blueprint(class_bp, url_prefix="/api")

    # Route for teachers
    app.register_blueprint(teacher_bp, url_prefix="/api")

    # Route for availability
    app.register_blueprint(availability_bp, url_prefix="/availability")

    # Route for time table generation
    app.register_blueprint(generation_bp, url_prefix="/generate")
    
    # Route for getting time table
    app.register_blueprint(getTimeTable_bp, url_prefix="/get")

    # Route for inputting
    app.register_blueprint(assign_bp, url_prefix="/input")
    return app
