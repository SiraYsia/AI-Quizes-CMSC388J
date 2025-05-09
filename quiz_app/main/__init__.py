from flask import Blueprint

main = Blueprint('main', __name__)

from quiz_app.main import routes