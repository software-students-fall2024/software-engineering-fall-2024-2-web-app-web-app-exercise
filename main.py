from flask import Flask, render_template
from pymongo import MongoClient, server_api
import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

# Set up MongoDB database connection
mongo_host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DBNAME")

client = MongoClient(mongo_host, server_api=server_api.ServerApi('1'))

db = client[db_name]
requests_collection = db.requests

reports = ["Vending machine", "Water fountain", "Door hinge"]

# Regular user homepage
@app.route("/")
def index():
    return render_template("index.html", is_admin=False)

# Admin homepage - show all requests
@app.route("/admin")
def admin_home():
    return render_template("index.html", reports=reports, is_admin=True)

# List all reports (separate view)
@app.route("/list")
def list_reports():
    return render_template("list.html", reports=reports)

# Request details page
@app.route("/request")
@app.route("/request/<requestID>")
def make_request(requestID=None):
    return render_template("request.html", requestID=requestID)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)
