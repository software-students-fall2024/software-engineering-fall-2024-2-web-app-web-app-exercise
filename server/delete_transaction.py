import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

database_url = os.getenv('DATABASE_ENDPOINT')

client = pymongo.MongoClient(database_url)

db = client["sample_supplies"]
collection = db["sales"]

def delete_transaction(email):
    collection.delete_one({"customer.email": email})
