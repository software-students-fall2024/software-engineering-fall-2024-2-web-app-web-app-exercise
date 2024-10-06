from flask import Flask, render_template
from flask.app import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

connstr = os.getenv("DB_URI")

if connstr is None:
    raise Exception("Database URI could not be loaded. Check .env file.")

db = MongoClient(connstr)

@app.route("/")
def index():
    return render_template('index.html')
