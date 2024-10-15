from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient, server_api
import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# load environment variables from .env vile
load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

# set up mongodb database connection
mongo_host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DBNAME")

client = MongoClient(mongo_host, server_api=server_api.ServerApi('1'))

db = client[db_name]
requests_collection = db.requests
#collections for the appliances?
building_collection = db.bldgs
appliance_collection = db.appliances

reports = ["Vending machine", "Water fountain", "Door hinge"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    return render_template("list.html", reports=reports)

@app.route("/request")
@app.route("/request/<requestID>")
def makeRequest(requestID=None):
    return render_template("request.html", requestID=requestID)

@app.route("/newApp")
def add_app():
    """
    Route for POST requests to new appliances page.
    Accepts form submission data and checks if the appliance exists.
    If it does, asks if user wants to update data. If not, creates 
    a new appliance with given data.
    """

    bname = request.form["bname"]
    floor = request.form["floor"]
    appName = request.form["appName"]
    code = request.form["code"]

    found: int = db.appliances.find({
        #ignore code for now, just focus on name and appliance
        "building":bname, 
        "floor":floor,
        "applianceName" : appName
    }).count()

    if found == 0:
        #check code is not in use
        doc = {
            "code":code,
            "building":bname,
            "floor":floor,
            "applianceName" : appName
        }
        db.appliances.insert_one(doc)
        return redirect(url_for("index"))

    else:
        return redirect(url_for("index"))
        #appliance exists, ask if they want to update code?


if __name__ == "__main__":
    app.run( host="127.0.0.1", port=3000)