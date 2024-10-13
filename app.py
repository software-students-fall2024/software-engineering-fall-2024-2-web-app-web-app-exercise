from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
        ###TODO###
        
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
        #signup logic
        ###TODO###
        
        #if invalid, display error message on the same page
        error = False
        if error:
            return render_template('signup.html', error="Error occurred!")
        
        # if valid, load signup success page
        return render_template("signup-success.html")
    
    
    @app.route("/user-info")
    def getUserInfo():
        #retrieve user info and return with template
        ###TODO###
        
        return render_template("user-info.html")
    
    
    @app.route("/user-info",methods=["PUT"])
    def updateUserInfo():
        #get the new user info and update the db
        title = request.form["title"]
        content = request.form["content"]
        ###TODO###
        
        
        #success
        flash("User Info updated!")
        return redirect(url_for("getUserInfo"))

    
    @app.route("/news")
    def getNews():
        #get News headline/timestamp/image/description/author/content info using external api
        ###TODO###
        
        return None
    
    
    @app.route("/contact-us")
    def contactUs():
        #get contact-us page
        return render_template("contact-us.html")
    
    @app.route("/contact-us",methods=["POST"])
    def sendMessage():
        #get the message title and content from form and email it to a specific address
        title = request.form["title"]
        content = request.form["content"]
        ###TODO###
        
        
        flash("Message Sent!")
        return redirect(url_for("contactUs"))
    
    
    @app.route("/vocab")
    def getVocab():
        #retrieve vocab list of the user and return with template
        ###TODO###
        
        return render_template("vocab.html")
    
    @app.route("/vocab",methods=["POST"])
    def sendVocab():
        #add vocab(word, definition) to the user vocab list
        word = request.form["word"]
        definition = request.form["definition"]
        ###TODO###
        
        
        flash("Word added to the list!")
        return jsonify({"message": "word added!"}), 200
    
    @app.route("/vocab",methods=["DELETE"])
    def deleteVocab():
        #delete word
        ###TODO###
        
        
        flash("Word successfully deleted!")
        return redirect(url_for("getVocab"))
    
    

    return app




    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
