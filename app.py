import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash


load_dotenv()

app = Flask(__name__)

# index means home
@app.route("/")
def index():
    return ""


# app.run(host="0.0.0.0", port=80)