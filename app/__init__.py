# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from flask_migrate import Migrate
from . import db

migrate = Migrate()
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()  # Initialize Bcrypt for other app components

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    

    return app
