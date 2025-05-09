import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from quiz_app import create_app
    app = create_app()
except Exception as e:
    from flask import Flask, render_template_string
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        error_details = traceback.format_exc()
        error_html = f"""
        <h1>Error loading the full application</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow: auto;">
        {error_details}
        </pre>
        <h2>Debug Information:</h2>
        <ul>
            <li>Python Path: {sys.path}</li>
            <li>Current Working Directory: {os.getcwd()}</li>
            <li>Files in directory: {os.listdir('.')}</li>
            <li>Files in parent directory: {os.listdir('..')}</li>
        </ul>
        """
        return render_template_string(error_html)
    
    @app.route('/api/health')
    def health():
        return {"status": "partial", "error": str(e)}