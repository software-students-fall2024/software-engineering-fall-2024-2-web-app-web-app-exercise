import pymongo
import os
from dotenv import load_dotenv
from bson import BSON
from bson import json_util
from bson.decimal128 import Decimal128
from statistics import mean

load_dotenv()

database_url = os.getenv('DATABASE_ENDPOINT')

client = pymongo.MongoClient(database_url)

db = client["sample_supplies"]
collection = db["sales"]

def get_store_location(store_location):
    sales_records = collection.find({"storeLocation": store_location})
    
    total_revenue = 0
    coupon_counter = 0
    sales_counter = 0
    best_sellers = dict()

    genders = []
    ages = []

    purchase_method_dict = dict()

    for sale in sales_records:
        sales_counter += 1

        if sale['couponUsed']:
            coupon_counter += 1

        customer = sale['customer']

        genders.append(customer['gender'])
        ages.append(customer['age'])

        purchase_method = sale['purchaseMethod']

        if purchase_method not in purchase_method_dict:
            purchase_method_dict[purchase_method] = 1
        else:
            purchase_method_dict[purchase_method] += 1

        for item in sale.get('items', []):
            # Calculate revenue
            # addition = (float(item["price"].to_decimal()) * float(item["quantity"]) 
            # if isinstance(item["price"], Decimal128) 
            # else float(item["price"]) * float(item["quantity"]))
            try:
                addition = float(item["price"].to_decimal()) * float(item["quantity"])
            except:
                addition = float(item["price"]) * float(item["quantity"])
            total_revenue += addition

            # Track quantities for each item
            item_name = item["name"]
            item_quantity = item["quantity"]

            if item_name not in best_sellers:
                best_sellers[item_name] = item_quantity
            else:
                best_sellers[item_name] += item_quantity

    # Calculate total revenue and coupon usage rate
    total_revenue = round(total_revenue, 2)
    coupon_percentage = round((coupon_counter / sales_counter) * 100, 2) if sales_counter > 0 else 0

    # Calculate gender distribution
    male_percentage = round((genders.count("M") / len(genders)) * 100, 2) if genders else 0
    female_percentage = round((genders.count("F") / len(genders)) * 100, 2) if genders else 0

    # Calculate average age
    average_age = round(mean(ages), 2) if ages else 0

    # Find the top three best-selling items by quantity
    top_three_best_sellers = sorted(best_sellers.items(), key=lambda x: x[1], reverse=True)[:3]
    best_sellers_dict = {item[0]: "{:,}".format(item[1]) for item in top_three_best_sellers}

    purchase_method_dict = {method: "{:,}".format(count) for method, count in purchase_method_dict.items()}

    # Prepare the output dictionary
    result = {
        "total_revenue": total_revenue,
        "coupon_percentage": coupon_percentage,
        "best_sellers": best_sellers_dict,
        "demographics": {
            "male_percentage": male_percentage,
            "female_percentage": female_percentage,
            "average_age": average_age
        },
        "purchase_methods": purchase_method_dict
    }

    return result

# client.close()
