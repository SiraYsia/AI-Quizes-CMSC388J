from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from quiz_app.config import Config

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Add Jinja2 filters
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if s:
            return s.replace('\n', '<br>')
        return s

    
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    from quiz_app.main import main
    from quiz_app.auth import auth
    from quiz_app.quiz import quiz
    from quiz_app.user import user
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(quiz)
    app.register_blueprint(user)
    
    return app