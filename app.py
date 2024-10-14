import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo 
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

logged_in = False
projects = None


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
    app.secret_key = "KEY"

    uri = "mongodb+srv://FriedBananaBan:Wc6466512288@project2.nzxyf.mongodb.net/?retryWrites=true&w=majority&appName=project2"
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['tasks']
    project_collection = db['projects']
    user_list = db['users']

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)



    @app.route("/")
    def base():
        return redirect(url_for('login'))

    @app.route("/main")
    def home():
        global logged_in  
        global projects

        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))
        
        # no matching projects
        if (projects == None):
            return render_template("main.html")

        return render_template("main.html", docs=projects, docs2=projects)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # username within database, find matching projects then redirect
            if (user_list.find_one({'username': username, 'password': password}) != None):
                global projects
                if (project_collection.find_one({'name': username}) != None):
                    doc = project_collection.find({'name': username})
                    projects = project_collection.find({'name': username})
                else:
                    projects = None
                # redirect to main, logged_in is true
                global logged_in 
                logged_in = True
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                return render_template("login.html", err="Invalid credentials, please try again.")
        
        return render_template("login.html")
    
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if (user_list.find_one({'username': username}) == None):
                user_list.insert_one({'username': username, 'password': password})
                flash("Registration successful!", "success")
                return redirect(url_for('login'))
            else:
                return render_template("registration.html", err="Username taken, please try again.")
        return render_template("registration.html")
    

    @app.route("/logout")
    def logout():
        global logged_in  

        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))
        logout_user()
        flash("Logged out successfully.", "info")
        return redirect(url_for('login'))

    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(port="5000")

