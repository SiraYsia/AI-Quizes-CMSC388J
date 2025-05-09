from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World from AI Quiz Generator! Basic app is working."

@app.route('/api/health')
def health():
    return {"status": "ok"}