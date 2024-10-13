from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os


def create_app():
    #initiate env
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # connection_string = os.getenv("MONGO_URI")  # Corrected to use "MONGO_URI" instead of MONGO_URI

    # if connection_string is None:
    #     raise ValueError("MONGO_URI environment variable not found!")

    # # Create a MongoDB client with the correct connection string
    # client = MongoClient(connection_string)
    # db = client["test_db"]
    # collection = db["test_collection"]
    # sample_data = {"name": "John Doe", "age": 30, "city": "New York"}
    # collection.insert_one(sample_data)

    # print("Document inserted successfully!")
    
    @app.route("/")
    def login():
        return render_template("home.html")
    
    @app.route("/login",methods=["POST"])
    def login_post():
        ### login Logic ###
        
        
        #if invalid, display error message on the same page
        error = False
        if error:
            return render_template('home.html', error="Error occurred!")
        
        # if valid, load signup success page
        return render_template("")
    
    
    @app.route("/signup")
    def signup():
        return render_template("signup.html")
    
    
    @app.route("/signup",methods=["POST"])
    def signup_post():
        ### signup Logic ###
        
        
        #if invalid, display error message on the same page
        error = False
        if error:
            return render_template('signup.html', error="Error occurred!")
        
        # if valid, load signup success page
        return render_template("signup-success.html")

    return app


    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
