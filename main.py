from flask import Flask, render_template, request
from markupsafe import escape
from pymongo import MongoClient, server_api
app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import re

# set up mongodb database connection
mongo_host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DBNAME")

client = MongoClient(mongo_host, server_api=server_api.ServerApi('1'))
db = client[db_name]
requests_collection = db.requests
appliance_collection = db.appliances

# Request logging
# @app.before_request
# def log_request_info():
#     print("Request Method:", request.method)
#     print("Request URL:", request.url)
#     print("Request Headers:", request.headers)
#     print("Request Data:", request.get_data())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    return render_template("list.html")

@app.route("/request", methods=["GET", "POST"])
def makeRequest(code=None):
    entry = None
    if(request.method == 'GET'):
        # If code is not empty and is 4 numbers
        if ((code := request.args.get('code')) != '' and code is not None and re.match(r'^[0-9]{4}$', code)):
            code = int(code)
            # If code exists, retrieve data as entry and display it 
            entry = appliance_collection.find_one({'code': code})
        else:
            entry = None
    if(request.method == 'POST'):
        entry = None
        # Retrieve post data and sanitize
        code = request.form.get('code')
        fullName = escape(request.form.get('fullName'))
        email = escape(request.form.get('email'))
        subject = escape(request.form.get('subject'))
        description = escape(request.form.get('description'))
        if(re.match(r'^[0-9]{4}$', code) and
            re.match(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', email)
        ):
            code = int(code)
            date = datetime.today().strftime('%Y-%m-%d')

            result = requests_collection.insert_one({'code': code, 'fullName': fullName, 'email': email, 'subject': subject, 'description': description, 'date': date})
            if(result.inserted_id):
                return render_template("request.html", success=True, applianceInfo=None)

    return render_template("request.html", applianceInfo=entry)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)