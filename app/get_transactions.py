import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

database_url = os.getenv('DATABASE_ENDPOINT')

client = pymongo.MongoClient(database_url)

db = client["sample_supplies"]
collection = db["sales"]

def get_transactions(store_location):
    # Initialize a dictionary to hold the transactions
    transactions = []

    # Fetch sales records for the specified store location
    sales_records = collection.find({"storeLocation": store_location})
    
    for sale in sales_records:
        # Get the sale date and format it
        sale_date = sale['saleDate']
        formatted_date = sale_date.strftime("%Y-%m-") + str(sale_date.day)

        # Calculate the total sale amount
        sale_amount = 0
        for item in sale.get('items', []):
            # Assuming 'price' is stored as a decimal.Decimal type; convert it to float
            try:
                addition = float(item["price"].to_decimal()) * float(item["quantity"])
            except:
                addition = float(item["price"]) * float(item["quantity"])
                
            sale_amount += addition
        
        sale_amount = round(sale_amount, 2)  # Round to 2 decimal places

        # Get customer email and purchase method
        email = sale['customer']['email']
        purchase_method = sale['purchaseMethod']

        # Append the transaction details to the transactions list
        transactions.append({
            "date": formatted_date,
            "amount": sale_amount,
            "customer_email": email,
            "purchase_method": purchase_method
        })

    # Create the output dictionary
    output = {
        "transactions": transactions
    }

    return output