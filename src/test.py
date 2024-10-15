import pymongo
from bson.objectid import ObjectId
import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://CodeBuns:CodeBuns@studybuns.ursnd.mongodb.net/?retryWrites=true&w=majority&appName=StudyBuns"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
