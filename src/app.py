import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, g, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from flask_login import LoginManager
from pprint import pprint 


def get_db():
    if 'db' not in g:
        load_dotenv()
        username = os.getenv('MONGO_USERNAME')
        password = os.getenv('MONGO_PASSWORD')
        db_name = os.getenv('MONGO_DBNAME')

        uri = f"mongodb+srv://{username}:{password}@cluster0.lrz8n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        client = MongoClient(uri, server_api=ServerApi('1'))
        g.db = client[db_name]  
    return g.db

login_manager = LoginManager()
def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    login_manager.init_app(app)
    register_blueprint(app)
    with app.app_context():
        get_db()
    return app
def register_blueprint(app):
    from src.routes import routes
    app.register_blueprint(routes)