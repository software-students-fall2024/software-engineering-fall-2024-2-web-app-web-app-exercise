from flask import Flask, render_template, request
from pymongo import MongoClient, server_api
import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import re

# load environment variables from .env vile
load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

# set up mongodb database connection
mongo_host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DBNAME")

client = MongoClient(mongo_host, server_api=server_api.ServerApi('1'))

db = client[db_name]
requests_collection = db.requests
#collections for the buildings?
#could potentially be used for auto generating codes
building_collection = db.bldgs
appliance_collection = db.appliances

reports = ["Vending machine", "Water fountain", "Door hinge"]
requestTest = [{"code":"1234","fullName":"Stephen","email":"srs@nyu.edu","subject":"test","description":"Descript","date":"2024-10-13"}]
applianceTest = {"code":"1234","building":"Bobst","floor":"4","applianceName":"Toilet"}

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

@app.route("/track", methods=["GET"])
def trackRequest(code=None):
    # If code is not empty and is 4 numbers
    if ((code := request.args.get('code')) != '' and code is not None and re.match(r'^[0-9]{4}$', code)):
        code = int(code)
        # If code exists, retrieve data as entry and display it 
        # requestEntry = requests_collection.find({'code':code}); // broken bc can't connect to atlas
        requestEntry = requestTest
        # applianceEntry = appliances_collection.find({'code':code});
        applianceEntry = applianceTest
        # print(entry.fullName);
    else:
        requestEntry = None
        applianceEntry = None
    return render_template("track.html", requestInfo=requestEntry, applianceInfo=applianceEntry)

if __name__ == "__main__":
    app.run( host="127.0.0.1", port=3000)