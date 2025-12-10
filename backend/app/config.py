import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- JWT Configuration ---
    
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise ValueError("Missing JWT_SECRET_KEY environment variable!")
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # Token stored in cookies
    JWT_TOKEN_LOCATION = ["cookies"]

    # Cookie settings
    JWT_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"   # HTTPS only in prod
    JWT_COOKIE_SAMESITE = "None"                                # Required for cross-domain cookies
    
    # Disable for simplicity (enable later for security)
    JWT_COOKIE_CSRF_PROTECT = False
    
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

    # --- App Configuration ---
    
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    if not ADMIN_PASSWORD:
        raise ValueError("Missing ADMIN_PASSWORD environment variable!")
    
    SLOTS_PER_DAY = int(os.getenv("SLOTS_PER_DAY", "7"))
    DAYS_PER_WEEK = int(os.getenv("DAYS_PER_WEEK", "5"))
    MAX_UNAVAILABLE_FRACTION = float(os.getenv("MAX_UNAVAILABLE_FRACTION", "0.95"))