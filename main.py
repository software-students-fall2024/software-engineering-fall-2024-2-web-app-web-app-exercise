from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from pymongo import MongoClient, server_api
app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os, re, string, random

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

# Set up MongoDB database connection
mongo_host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DBNAME")

client = MongoClient(mongo_host, server_api=server_api.ServerApi('1'))
db = client[db_name]
requests_collection = db.requests
#collections for the buildings?
#could potentially be used for auto generating codes
building_collection = db.bldgs
appliance_collection = db.appliances

# Request logging
# @app.before_request
# def log_request_info():
#     print("Request Method:", request.method)
#     print("Request URL:", request.url)
#     print("Request Headers:", request.headers)
#     print("Request Data:", request.get_data())
requestTest = [{"code":"1234","fullName":"Stephen","email":"srs@nyu.edu","subject":"test","description":"Descript","date":"2024-10-13"}]
applianceTest = {"code":"1234","building":"Bobst","floor":"4","applianceName":"Toilet"}
doc_code = 0 #for when we need to update appliances

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
def list():
    return render_template("list.html")


@app.route("/request", methods=["GET", "POST"])
def make_request():
    error = request.args.get('error')  # Get error from query parameters

    entry = None
    if(error):
        return render_template("request.html", error=True)
    if(request.method == 'GET'):
        ticket=None
        # If code is not empty and is 5 numbers
        if ((code := request.args.get('code')) and re.match(r'^[0-9]{4,5}$', code)):
            code = int(code)
            # If code exists, retrieve data as entry and display it 
            entry = appliance_collection.find_one({'code': code})
        
            # If code was not found in database send error
            if(not entry):
                return render_template("request.html", error=True, errInfo="Code not found", applianceInfo=None, ticket=None)
            
        # If there is no code given, check for support ticket
        if(not request.args.get('code')):
            # Render ticket if it exists in args and in database
            ticket = request.args.get('ticket')
            # If ticket does not exist in database, do not display successful request screen
            if(ticket and requests_collection.count_documents({'ticket':ticket}) == 0):
                ticket=None
        return render_template("request.html",ticket=ticket, applianceInfo=entry)
    
    if(request.method == 'POST'):
        entry = None
        # Retrieve post data and sanitize
        code = request.form.get('code')
        fullName = escape(request.form.get('fullName'))
        email = escape(request.form.get('email'))
        subject = escape(request.form.get('subject'))
        description = escape(request.form.get('description'))
        # If code and email match
        if(re.match(r'^[0-9]{4,5}$', code) and re.match(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', email)):
            code = int(code)
            date = datetime.today().strftime('%Y-%m-%d')

            # Generate a random unique ticket
            ticket = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            i = 0
            while(requests_collection.count_documents({'ticket':ticket}) != 0):
                ticket = ''.join(random.choices(string.ascii_uppercase) + string.digits, k=8)
                i+=1
                if(i > 10):
                    break

            result = requests_collection.insert_one({
                'code': code, 
                'status':'pending', 
                'ticket':ticket, 
                'fullName': fullName, 
                'email': email, 
                'subject': subject, 
                'description': description, 
                'date': date
            })

            if(result.inserted_id):
                return redirect(url_for("make_request", ticket=ticket))

        # Redirect with error if validation fails
        return redirect(url_for("make_request", error=True))
    

    return render_template("request.html", ticket=ticket, applianceInfo=entry)

@app.route("/track", methods=["GET"])
def trackRequest(code=None):
    # If code is not empty and is 4 numbers
    if ((code := request.args.get('code')) != '' and code is not None and re.match(r'^[0-9]{4,5}$', code)):
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
    app.run(host="127.0.0.1", port=3000)