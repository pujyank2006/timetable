import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
