import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
from models import User
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import os

bcrypt = Bcrypt()

def create_app():
    #initiate env
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    connection_string = os.getenv("MONGO_URI")  # Corrected to use "MONGO_URI" instead of MONGO_URI

    if connection_string is None:
        raise ValueError("MONGO_URI environment variable not found!")

    # Create a MongoDB client with the correct connection string
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
                return redirect(url_for("getNews"))
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
        user_info = {
            "username": current_user.username,
            "password": current_user.password,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname
        }
        
        return render_template("setting.html", user_info=user_info)
    
    @app.route("/update-info")
    @login_required
    def getUpdatePage():
        user_info = {
            "username": current_user.username,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname
        }
        
        return render_template("edit-user-info.html", user_info=user_info)
    
    @app.route("/user-info",methods=["POST"])
    @login_required
    def updateUserInfo():
        #get the new user info and update the db
        title = request.form["title"]
        content = request.form["content"]
        ###TODO###
        
        
        #success
        flash("User Info updated!")
        return redirect(url_for("getUserInfo"))
    

    @app.route("/log-out")
    @login_required 
    def logout():
        logout_user() 
        return redirect(url_for('home'))
    
    @app.route("/delete-acct")
    @login_required 
    def delete_acct():
        return render_template("delete-acct.html")
        
    @app.route('/delete-acct', methods=['POST'])
    @login_required
    def delete_account():
        # getting the form data
        username = request.form.get('username')
        password = request.form.get('password')
        # if username entered from form == logged in user's username
        if username == current_user.username:
            user = db.users.find_one({"username": username})

            # check if the user exists and the password matches
            if user and bcrypt.check_password_hash(user['password'], password):
                db.users.delete_one({"username": username})
                
                # log user out and redirect to home w/ success message
                logout_user()
                flash('Account has been successfully deleted.')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password. Please try again.')
        else:
            flash('The provided email does not match the current user.')

        return render_template('delete-acct.html')
    
    
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
    
    @app.route("/news")
    def getNews():
        
        return render_template("news.html", firstname=current_user.firstname, lastname = current_user.lastname)
    
    @app.route("/news-content")
    def getNewsContent():

        return render_template("news-content.html")
    
    @app.route("/menu")
    def getMenu():
        
        return render_template("Menu.html")
    
    

    return app



    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)