from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)

# mongo setup
mongo_uri = os.getenv('MONGO_CONNECTION_URI')
client = MongoClient(mongo_uri)
db = client.theCoders

@app.route('/')
def home():
    try:
        # Check MongoDB connection
        client.server_info()  # Will throw an exception if the connection is not successful
        return "Hello, Flask! MongoDB connection successful."
    except Exception as e:
        return f"Hello, Flask! MongoDB connection failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)