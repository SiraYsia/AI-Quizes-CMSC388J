from flask import Flask, request
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app

def handler(request):
    return app(request)