from flask import Flask
from config import Config
from flask_login import LoginManager

# __name__ is the package name (app)
flask_app_instance = Flask(__name__)
flask_app_instance.config.from_object(Config)

login_manager = LoginManager(flask_app_instance)




from app import routes
