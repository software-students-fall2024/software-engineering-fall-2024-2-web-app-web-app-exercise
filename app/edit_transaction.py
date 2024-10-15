import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

database_url = os.getenv('DATABASE_ENDPOINT')

client = pymongo.MongoClient(database_url)

db = client["sample_supplies"]
collection = db["sales"]

def edit_transaction(email, purchase_method):
    query = {"customer.email": email}
    update_query = {"$set": {"purchaseMethod": purchase_method}}
    collection.update_one(query, update_query)
    
edit_transaction("ohaguwu@nufub.gi", "In store")