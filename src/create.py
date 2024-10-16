import pymongo
from bson.objectid import ObjectId
import datetime

from flask import Flask, render_template, request, redirect, abort, url_for, make_response
uri = "mongodb+srv://CodeBuns:CodeBuns@studybuns.ursnd.mongodb.net/?retryWrites=true&w=majority&appName=StudyBuns"

connection = pymongo.MongoClient(uri)

# select a specific database on the server
db = connection["CodeBuns"]
app = Flask(__name__)

doc = {
    "name": "Foo Barstein",
    "email": "fb1258@nyu.edu",
    "message": "We loved with a love that was more than love.\n -Edgar Allen Poe",
    "created_at": datetime.datetime.utcnow() # the date time now
}
