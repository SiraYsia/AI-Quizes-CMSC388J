from flask import Flask

app = Flask(__name__)

@app.route('/')
def test_home():
    return "Test route is working!"

@app.route('/test')
def test():
    return {"message": "Test API endpoint is working"}