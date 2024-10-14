import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo 
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

logged_in = False
projects = None


############## Database Organization ###############

''' Project Document Structure
{"_id": ObjectId('________'),
"projectName": "projectName",
"managers": ["manager1", "manager2"],
"members": ["member1", "member2"],
"tasks": [{"taskName": "xxx", "date", "yyy", "status": "not-complete"}, ...]

'''
#####################################################

def create_app():
    # APP SETUP
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


    ############# ROUTES #############
    # base route redirects to login
    @app.route("/")
    def base():
        return redirect(url_for('login'))

    # main route displays home screen with all projects
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

    # route to login page
    # if POST, check if username and password match
    # if match, redirect to main
    # if not, return to login with error message
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
    
    # route to register page
    # if POST, check if username is taken
    # if not, add to database and redirect to login
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
    

    # route to create project page
    # WIP - need to add project description
    #       need to assign project manager
    @app.route("/create_project", methods=['GET', 'POST'])
    def create_project():
        if request.method == 'POST':
            project_name = request.form['project_name']
            project_description = request.form['project_description']
            project_members = request.form['project_members'].split(",")
            project_manager = "Terry" 
            start_date = request.form.get('start_date', '')
            due_date = request.form.get('due_date', '')
        
            # Save the project into MongoDB
            project_collection.insert_one({
                'projectName': project_name,
                'description': project_description,
                'managers': [project_manager],
                'members': project_members,
                'start_date': start_date,
                'due_date': due_date,
                'tasks': []
            })
            
            flash("Project created successfully!", "success")
            return redirect(url_for('home'))

        return render_template("create_project.html")


    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(port="3000")

