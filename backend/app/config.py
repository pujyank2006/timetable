import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- JWT Configuration ---
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key') # Fallback for safety
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # 1. Tell Flask-JWT to read tokens from cookies
    JWT_TOKEN_LOCATION = ["cookies"]
    
    # 2. Cookie Security Settings
    # True = Cookies only sent over HTTPS (Production)
    # False = Cookies sent over HTTP (Localhost)
    # We check if FLASK_ENV is 'production' to auto-set this, or default to False
    JWT_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    
    # 3. CSRF Protection
    # For high security, this should be True, but it requires extra frontend setup (CSRF headers).
    # Setting to False simplifies the implementation for now.
    JWT_COOKIE_CSRF_PROTECT = False 
    
    # 4. Name of the cookie containing the access token
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

    # --- App Configuration ---
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    
    # Defaults for timetable slots (used for availability validation)
    SLOTS_PER_DAY = int(os.getenv('SLOTS_PER_DAY', '7'))
    DAYS_PER_WEEK = int(os.getenv('DAYS_PER_WEEK', '5'))
    
    # Fraction (0-1] of total slots a teacher may mark unavailable.
    MAX_UNAVAILABLE_FRACTION = float(os.getenv('MAX_UNAVAILABLE_FRACTION', '0.95'))