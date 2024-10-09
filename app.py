# Required libraries installation:
# pip install Flask pymongo python-dotenv bcrypt

from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Fetch the MongoDB URI from .env file
MONGO_URI = os.getenv('MONGO_URI')

# Establish MongoDB connection using PyMongo
client = MongoClient(MONGO_URI)

# Define your database (replace <database_name> with actual DB name)
db = client["occasio"]

# Define a test collection (replace <collection_name> with actual collection name)
collection = db["users"]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Check if user exists
        user = collection.find_one({"username": username})
        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return f"Login successful! Welcome, {username}."
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Check if user already exists
        if collection.find_one({"username": username}):
            flash("Username already exists. Please choose a different one.")
        else:
            # Hash the password before saving it to the database
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            collection.insert_one({"username": username, "password": hashed_password})
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)