from flask import Flask, render_template, request
from pymongo import MongoClient, server_api
import re
app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

reports = ["Vending machine", "Water fountain", "Door hinge"]
fakeCodes = [{'code': 1234, 'building':"CIWW", 'floor':2, 'applianceName':'Water Fountain'}]

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
    return render_template("list.html", reports=reports)

@app.route("/request", methods=["GET", "POST"])
def makeRequest(code=None):
    entry = None
    if(request.method == 'POST'):
        # If code is not empty and is 4 numbers
        if(code := request.form.get('code')) != '' and re.match(r'^[0-9]{4}$', code):
            code = int(code)
            # If code exists, retrieve data as entry and display it 
            # NOTE: This will be replaced by an actual request to our database for the appliance info
            entry = next((entry for entry in fakeCodes if entry["code"] == code), None)
        else:
            entry = None
            # Probably display something like code not found

    return render_template("request.html", applianceInfo=entry)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)