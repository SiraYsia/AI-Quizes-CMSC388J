from flask import Blueprint, render_template
from . import main

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='AI QUIZES')
