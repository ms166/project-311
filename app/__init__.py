from flask import Flask
from config import Config

# __name__ is the package name (app)
flask_app_instance = Flask(__name__)
flask_app_instance.config.from_object(Config)
from app import routes
