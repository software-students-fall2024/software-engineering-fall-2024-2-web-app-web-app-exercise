from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from models import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import os


def create_app():
    #initiate env
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    connection_string = os.getenv("MONGO_URI")  # Corrected to use "MONGO_URI" instead of MONGO_URI

    if connection_string is None:
        raise ValueError("MONGO_URI environment variable not found!")

    # # Create a MongoDB client with the correct connection string
    client = MongoClient(connection_string)
    db = client["test_db"]
    
    # user auth stuff
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    
    # user loader for flask login
    @login_manager.user_loader
    def load_user(user_id):
        user = db.users.find_one({"_id": user_id})
        if user:
            return User(str(user["_id"]), user["username"])
        return None
    
    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            # Login Logic
            username = request.form["username"]
            password = request.form["password"]
            user = User.validate_login(db, username, password)
            if user:
                login_user(user)
                return redirect(url_for("contact_us")) ## change this for when news page gets implemented 
            else:
                flash("Invalid username or password. Try again.")
                return render_template('home.html', error="Error occurred!")
        return render_template("home.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if User.find_by_username(db, username):
                flash("Username with that email already exists!")
                return render_template('signup.html', error="Error occurred!")
            User.create_user(db, username, password)
            flash("User created successfully!")
            return redirect(url_for("login"))
        return render_template("signup.html")
    
    
    @app.route("/user-info")
    @login_required # this decorator makes it so you can only be logged in to view this page.... put this on any new routes you make pls
    def getUserInfo():
        #retrieve user info and return with template
        ###TODO###
        
        return render_template("user-info.html")
    
    
    @app.route("/user-info",methods=["PUT"])
    @login_required
    def updateUserInfo():
        #get the new user info and update the db
        title = request.form["title"]
        content = request.form["content"]
        ###TODO###
        
        
        #success
        flash("User Info updated!")
        return redirect(url_for("getUserInfo"))
    
    
    @app.route("/contact_us")
    @login_required
    def contact_us():
        #get contact-us page
        return render_template("Contact_us.html")
    
    @app.route("/contact_us",methods=["POST"])
    def sendMessage():
        #get the message title and content from form and email it to a specific address
        title = request.form["title"]
        content = request.form["content"]
        ###TODO###
        
        
        flash("Message Sent!")
        return redirect(url_for("contact_us"))
    
    
    @app.route("/vocab")
    @login_required
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
