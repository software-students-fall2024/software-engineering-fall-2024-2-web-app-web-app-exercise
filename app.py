import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo 
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

logged_in = False
projects_as_manager = None
projects_as_member = None

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

        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))
        
        # no matching projects
        if (projects_as_manager == None and projects_as_member == None):
            return render_template("main.html")
        # only have projects as a member
        elif (projects_as_manager == None):
            return render_template("main.html", docs_as_member=projects_as_member)
        # only have projects as manager
        elif (projects_as_member == None):
            return render_template("main.html", docs_as_manager=projects_as_manager)
        # have both manager and member roles in projects
        else:
            return render_template("main.html", docs_as_manager=projects_as_manager, docs_as_member=projects_as_member)

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
                
                # check if any projects contain the username as a manager
                if (project_collection.find_one({'managers': username}) != None):
                    global projects_as_manager
                    projects_as_manager = project_collection.find({'managers': username})
                # check if any projects contain the username as a member
                if (project_collection.find_one({'members': username}) != None):
                    global projects_as_member
                    projects_as_member = project_collection.find({'members': username})

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
    @app.route('/create_project', methods=['GET', 'POST'])
    def create_project():
        if request.method == 'POST':
            # Get managers and members as comma-separated strings from the form
            managers = request.form['managers'].split(',')
            members = request.form['members'].split(',')

            # Create the project data
            project_data = {
                'projectName': request.form['project_name'],
                'description': request.form['description'],
                'start_date': request.form['start_date'],
                'due_date': request.form['due_date'],
                'managers': managers,  # Store managers as an array
                'members': members,    # Store members as an array
                'tasks': []  # Initially no tasks
            }

            # Insert the project into the database
            project_collection.insert_one(project_data)
            flash("Project created successfully!", "success")
            return redirect(url_for('home'))

        return render_template('create_project.html')

    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(port="3000")

