import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from quiz_app import create_app
    app = create_app()
except Exception as e:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return f"Error loading full app"
    
    @app.route('/api/health')
    def health():
        return {"status": "ok", "full_app": False}