from flask import Flask, render_template, request, redirect, url_for
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
doc_code = 0 #for when we need to update appliances

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
@app.route("/newApp/<update>")
def new_app(update): #0 by default
    return render_template("newApp.html", update=update)

@app.route("/removeApp")
def delete_app():
    return render_template("deleteApp.html", results = None)

@app.route("/newApp/make", methods=["POST"])
def add_app():
    """
    Route for POST requests to new appliances page.
    Accepts form submission data and checks if the appliance exists.
    If it does, asks if user wants to update data. If not, creates 
    a new appliance with given data.
    """

    bname = request.form["bname"]
    floor = int(request.form["floor"])
    appName = request.form["appName"]
    code = int(request.form["code"])

    found: int = appliance_collection.count_documents({
        #ignore code for now, just focus on name and appliance
        "building":bname, 
        "floor":floor,
        "applianceName" : appName
    })

    codeUse: int = appliance_collection.count_documents({
        "code": code
    })

    if found != 0:
        #not sure of a 'cleaner' way to do this
        global doc_code
        doc_code = (appliance_collection.find_one({
            "building":bname, 
            "floor":floor,
            "applianceName" : appName
        }).get("code"))
        return redirect(url_for("new_app", update = 1,docCode = doc_code, blname = str(bname), floor=floor, appName=appName))
        #appliance exists, ask if they want to update code?
    elif codeUse != 0:
        return redirect(url_for("new_app", update = 2))
    else:
        #check code is not in use
        doc = {
            "code":code,
            "building":bname,
            "floor":floor,
            "applianceName" : appName
        }
        appliance_collection.insert_one(doc)
        return redirect(url_for("new_app", update =3)) #successfully added

#@app.route("/newApp/update/", methods=["POST"])
@app.route("/newApp/update", methods=["POST"])
def update_app():
    #make it so that a doc_code == 0 throws an error message?
    bname = request.form["bname"]
    floor = int(request.form["floor"])
    appName = request.form["appName"]
    code = int(request.form["code"])

    found: int = appliance_collection.count_documents({
        #ignore code for now, just focus on name and appliance
        "code":{
            "$ne": doc_code
        },
        "building":bname, 
        "floor":floor,
        "applianceName" : appName
    })
    
    #can maybe simplify?
    if(code != doc_code):
        codeUse: int = appliance_collection.count_documents({
            "code": code
        })
    else:
        codeUse = 0

    if found!= 0:
        return redirect(url_for("new_app", update = 4,doc_code=doc_code, blname = str(bname), floor=floor, appName=appName))
    elif codeUse != 0:
        return redirect(url_for("new_app", update = 5,doc_code=doc_code, blname = str(bname), floor=floor, appName=appName))
    else:
        appliance_collection.update_one(
            {"code":doc_code},
            {
                "$set": {
                    "code" : code,
                    "building":bname,
                    "floor":floor,
                    "applianceName" : appName
                }
            }
        )
        return redirect(url_for("new_app", update =3))

@app.route("/removeApp/find/<use>", methods=["POST"])
def get_app(use): #can potentially also be used for making requests?
    if(use == 'code'):
        code = request.form["code"]
        result=appliance_collection.find_one({
            "code":code
        })
    else:
        result = appliance_collection.find_one({
            "building": request.form["bname"],
            "floor": request.form["floor"],
            "applianceName":request.form["appName"]
        })
    
    return redirect(url_for('delete_app', results=result))

@app.route("/removeApp/remove/<code>", methods=["POST"])
def remove_appliance(code):
    appliance_collection.delete_one({
        "code": code
    })
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run( host="127.0.0.1", port=3000)