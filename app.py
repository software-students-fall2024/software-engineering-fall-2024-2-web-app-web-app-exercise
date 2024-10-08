from pymongo import MongoClient
from hashlib import sha256
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Fetch the MongoDB URI from .env file
MONGO_URI = os.getenv('MONGO_URI')

# Establish MongoDB connection using PyMongo
client = MongoClient(MONGO_URI)

# Define your database (replace <database_name> with actual DB name)
db = client["occasio"]

# Define a test collection (replace <collection_name> with actual collection name)
collection = db["users"]

class UserSchema:
    def __init__(self, username, password):
        self.username = username
        self.password = sha256(password.encode()).hexdigest()

    def __repr__(self):
        return f"UserSchema({self.username}, {self.password})"

    def save_to_db(self):
        user_data = {
            "username": self.username,
            "password": self.password
        }
        collection.insert_one(user_data)

    @staticmethod
    def find_by_username(username):
        return collection.find_one({"username": username})

    @staticmethod
    def update_password(username, new_password):
        hashed_password = sha256(new_password.encode()).hexdigest()
        collection.update_one({"username": username}, {"$set": {"password": hashed_password}})

@app.route('/')
def home():
    try:
        # Perform a simple query to check the connection
        client.admin.command('ping')
        return "MongoDB and Flask connection successful!"
    except Exception as e:
        return f"Error connecting to MongoDB: {str(e)}", 500

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    user = UserSchema(data['username'], data['password'])
    user.save_to_db()
    return jsonify({"message": "User added successfully!"}), 201

@app.route('/get_user/<username>', methods=['GET'])
def get_user(username):
    user = UserSchema.find_by_username(username)
    if user:
        return jsonify({"username": user['username'], "password": user['password']})
    return jsonify({"message": "User not found"}), 404

@app.route('/update_password', methods=['PUT'])
def update_password():
    data = request.get_json()
    UserSchema.update_password(data['username'], data['new_password'])
    return jsonify({"message": "Password updated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)