from dotenv import load_dotenv
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
import os
from pymongo.mongo_client import MongoClient

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_uri = os.getenv("DB_URI")
port = os.getenv("FLASK_PORT")

# Create a new client and connect to the server
client = MongoClient(db_uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)