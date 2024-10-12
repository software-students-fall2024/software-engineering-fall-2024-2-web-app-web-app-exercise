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
uri = "mongodb+srv://thisapp:<db_password>@thisapp.pgts3.mongodb.net/?retryWrites=true&w=majority&appName=thisapp"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)