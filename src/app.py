import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv
import flask
from src.database_initialisation import *
import flask_login
from flask_login import LoginManager
from dotenv import dotenv_values

config = dotenv_values(".env")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['db']
database_add(db, "pedals", "src/data/pedal_data.json")
database_add(db, "users", "src/data/user_data.json")
login_manager = LoginManager()
def create_app():
    app = Flask(__name__)
    app.secret_key = config['SECRET_KEY']
    login_manager.init_app(app)
    register_blueprint(app)
    return app

def register_blueprint(app):
    from src.routes import routes
    app.register_blueprint(routes)