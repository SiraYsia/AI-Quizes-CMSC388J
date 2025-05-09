import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_ENABLED = True
    
    MONGO_URI = os.environ.get('MONGO_URI')

    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    @classmethod
    def validate_config(cls):
        missing_vars = []
        
        if not cls.SECRET_KEY:
            missing_vars.append('SECRET_KEY')
        
        if not cls.MONGO_URI:
            missing_vars.append('MONGO_URI')
            
        if not cls.GEMINI_API_KEY:
            missing_vars.append('GEMINI_API_KEY')
            
        if missing_vars:
            print(f"WARNING: The following environment variables are missing: {', '.join(missing_vars)}")
            print("Please check your .env file")