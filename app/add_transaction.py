import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

database_url = os.getenv('DATABASE_ENDPOINT')

client = pymongo.MongoClient(database_url)

db = client["sample_supplies"]
collection = db["sales"]


def add_transaction(item_name, quantity, price, store_location, gender, age, email, coupon_used, purchase_method):
    transaction = {
        "saleDate": datetime.now(timezone.utc).isoformat(),
        "items": [
            {
                "name": item_name,
                "quantity": quantity,
                "price": round(price, 2) 
            }
        ],
        "storeLocation": store_location,
        "customer": {
            "gender": gender,
            "age": age,
            "email": email
        },
        "couponUsed": coupon_used,
        "purchaseMethod": purchase_method
    }

    collection.insert_one(transaction)


