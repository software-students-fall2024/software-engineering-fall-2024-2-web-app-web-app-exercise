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
app.config['SESSION_PERMANENT'] = False

# Fetch the MongoDB URI from .env file
MONGO_URI = os.getenv('MONGO_URI')

# Establish MongoDB connection using PyMongo
client = MongoClient(MONGO_URI)

# Define your database
db = client["occasio"]

# Define a test collection
collection = db["users"]

@app.route('/')
def home():
    if 'username' in session:
        # If the user is already authenticated, redirect them to the home feed
        return redirect(url_for('home_feed'))
    # Render the welcome page with buttons for login and register
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Check if user exists
        user = collection.find_one({"username": username})
        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            session.permanent = False  # Session expires when the browser closes
            return redirect(url_for('home_feed'))
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

@app.route('/logout')
def logout():
    # Clear the session data to log the user out
    session.clear()
    flash("You have been logged out successfully.")
    return redirect(url_for('home'))


@app.route('/home_feed')
def home_feed():
    if 'username' in session:
        # Render the home feed page for authenticated users
        return render_template('home_feed.html', username=session['username'])
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)