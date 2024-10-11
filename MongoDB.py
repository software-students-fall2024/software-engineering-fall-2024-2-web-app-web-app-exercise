from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

connection_string = os.getenv("MONGO_URI")  # Corrected to use "MONGO_URI" instead of MONGO_URI

if connection_string is None:
    raise ValueError("MONGO_URI environment variable not found!")

# Create a MongoDB client with the correct connection string
client = MongoClient(connection_string)
db = client["test_db"]
collection = db["test_collection"]
sample_data = {"name": "John Doe", "age": 30, "city": "New York"}
collection.insert_one(sample_data)

print("Document inserted successfully!")
