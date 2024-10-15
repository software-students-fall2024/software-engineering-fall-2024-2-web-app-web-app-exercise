from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from models import User
from flask_login import LoginManager, login_user, login_required
import os


def create_app():
    #initiate env
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
        user = db.users.find_one({"username": user_id}) # user is unique id'd by username (email)
        if user:
            return User(
                username=user["username"],
                password=user.get("password"),
                firstname=user.get("firstname"),
                lastname=user.get("lastname"),
            )
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
            password2 = request.form["password2"]
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            # check if passwords match
            if password != password2:
                flash("Passwords don't match!")
                return render_template("signup.html")
            
            if User.find_by_username(db, username):
                flash("Username with that email already exists!")
                return render_template('signup.html', error="Error occurred!")
            User.create_user(db, username, password, firstname, lastname)
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
