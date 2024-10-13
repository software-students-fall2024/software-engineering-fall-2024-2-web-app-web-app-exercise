import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import datetime

load_dotenv()

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


################# Sample Data ################# 
user_doc = {
    "username": "admin",   # make usernames unique?, so that it can be searched with find_one()
    "password": "admin",       # or add another unique user id 
    "project_id": ["x43gbf34", "a87gkf39"],
    "access_level": "admin",  # or "user"
    "created_at": datetime.datetime.utcnow() # the date time now
}

project_doc = {
    "project_name": "Project 1",
    "project_id": "x43gbf34",     # unique id, can be searched with find_one()
    "tasks": ["task1", "task2"],
    "team members": ["user1", "user2"],  # all unique usernames of team members
    "created_at": datetime.datetime.utcnow() # the date time now
}

task_doc = {
    "task_name": "task1",
    "task_id": "hc619c71",     # unique id, can be searched with find_one()
    "task_description": "This is task 1",
    "task_status": "completed",
    "task_members":["user1", "user2"],
    "task_deadline": "2022-12-31",
    "created_at": datetime.datetime.utcnow() # the date time now
}
###############################################

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    client = MongoClient(os.getenv('MONGO_URI'))
    db = client.get_database("your_database_name")
    users_collection = db["users"]

    @login_manager.user_loader
    def load_user(user_id):
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(str(user_data['_id']), user_data['username'])
        return None

    @app.route("/main")
    @login_required
    def home():
        programs = [{"p_name": "1", "id": "1"}, {"p_name": "2", "id": "2"}]
        return render_template("main.html", programs=programs)
        
    # team page
    @app.route('/program/<id>')
    def program(id):
        programs = [{"p_name": "1", "id": "1", "task": ["1.1", "1.2"]}, {"p_name": "2", "id": "2", "task": ["2.1", "2.2"]}]
        for program in programs:
            if program["id"] == id:
                return render_template("team.html", program=program)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

        
            user_data = users_collection.find_one({"username": username})
            if user_data and user_data['password'] == password:  
                user_obj = User(str(user_data['_id']), user_data['username'])
                login_user(user_obj)
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid credentials, please try again.", "danger")
        
        return render_template("login.html")
    
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        return render_template("register.html")
    

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully.", "info")
        return redirect(url_for('login'))

    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

