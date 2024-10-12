from flask import Flask, render_template
from pymongo import MongoClient, server_api
from dotenv import load_dotenv
import os

# load environment variables from .env vile
load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

# set up mongodb database connection
mongo_host = os.getenv("MONGO_HOSt")
db_name = os.getenv("MONGO_DBNAME")

client = MongoClient(mongo_host, server_api=server_api.ServerApi('1'))

db = client[db_name]
requests_collection = db.requests

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


if __name__ == "__main__":
    app.run( host="127.0.0.1", port=3000)