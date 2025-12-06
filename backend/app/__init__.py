from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.controllers.subject_controller import subject_bp
from app.controllers.teacher_controller import teacher_bp
from app.controllers.availability_controller import availability_bp
from app.controllers.login_controller import user_bp
from app.algorithm.time_table_generation_controller import generation_bp

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    # Load configuration
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
    
    # Initialize JWT
    jwt = JWTManager(app)

    # Route for users/login
    app.register_blueprint(user_bp, url_prefix="/users")

    # Route for subjects
    app.register_blueprint(subject_bp, url_prefix="/api")

    # Route for teachers
    app.register_blueprint(teacher_bp, url_prefix="/api")

    # Route for availability
    app.register_blueprint(availability_bp, url_prefix="/availability")

    # Route for time table generation
    app.register_blueprint(generation_bp, url_prefix="/generate")
    
    return app
