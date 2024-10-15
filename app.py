import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request, jsonify
import pymongo
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from flask import session
from bson.objectid import ObjectId
from flask_cors import CORS

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
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
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
        as_manager = []
        as_member = []

        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))
        
        # no matching projects
        if (projects == None):
            return render_template("main.html")
        
        for project in project_collection.find({}):
            managers = project.get("managers", []) 
            members = project.get("members", []) 

            # Check if the logged-in user is one of the managers
            if session["username"] in managers:
                as_manager.append(project)            
            if session["username"] in members:
                as_member.append(project)            
        return render_template("main.html", docs=as_manager, docs2=as_member)
    
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
                #store session
                session['username'] = username
                if (project_collection.find_one({'name': username}) != None):
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
            # project_description = request.form['project_description']
            project_members = request.form['project_members'].split(",")
            project_collection.insert_one({'projectName': project_name, 'managers': ["Terry"], 'members': project_members, 'tasks': []})
            flash("Project created!", "success")
            return redirect(url_for('main'))
        return render_template("create_project.html")      
        
    # team page
    @app.route('/project/<id>')
    def project(id):
        project = project_collection.find_one({"_id": ObjectId(id)})
        return render_template("team.html", project=project)
    
    # team page / Assign task
    @app.route('/<id>/assign-task', methods=['POST'])
    def addTask(id):
        data = request.get_json()
        task_name = data.get('taskName')
        task_date = data.get('taskDate')
        task_status = data.get('taskStatus')
        
        if task_name and task_date and task_status:
            project = project_collection.find_one({"_id": ObjectId(id)})
            project.project["tasks"].append({"taskName": taskName, "taskDate": taskDate, "taskStatus": taskStatus})
            return jsonify({"error": "project not found"}), 404
        else:
            return jsonify({"error": "Task name is required"}), 400
        
    # team page / Edit task
    @app.route('/<id>/edit-task/<task_id>', methods=['POST'])
    def edit_task(id, task_id):
        data = request.get_json()
        new_task_name = data.get('taskName')
        if new_task_name:
            for project in projects:
                if project["id"] == id:
                    for task in project["tasks"]:
                        if task["id"] == task_id:
                            task["id"] = new_task_name
                            return jsonify({"success": True, "task": {"id": task_id, "name": new_task_name}}), 200
            return jsonify({"error": "project or Task not found"}), 404
        else:
            return jsonify({"error": "Task name is required"}), 400    
             
    @app.route('/<id>/delete-task/<taskName>', methods=['GET'])
    def delete_task(id, taskName):
        print(f"Deleting task {taskName} from project {id}")  # Add logging to debug

        # Find the project by ID
        project = project_collection.find_one({"_id": ObjectId(id)})
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Find the task in the project's task list
        task_list = project.get("tasks", [])
        task_to_remove = None

        # Loop through the tasks to find the one matching taskName
        for task in task_list:
            print(f"Checking task: {task['taskName']}")  # Add logging to see tasks being checked
            if task["taskName"] == taskName:
                task_to_remove = task
                break

        # If task not found, return error
        if not task_to_remove:
            return jsonify({"error": "Task not found in the project"}), 404

        # Remove the task and update the project in the database
        task_list.remove(task_to_remove)
        project_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"tasks": task_list}}
        )

        return jsonify({"success": True}), 200 
    
    # team page / Delete member
    @app.route('/<id>/delete-member/<member>', methods=['DELETE'])
    def delete_member(id, member):
        project = project_collection.find_one({"_id": ObjectId(id)})
        # Check if the project exists
        if not project:
            return jsonify({"error": "Project not found"}), 404
        # Check if the member exists in the project's members list
        if member not in project["members"]:
            return jsonify({"error": "Member not found in the project"}), 404
        
        # Update the project in the database after removing the member
        project["members"].remove(member)
        project_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"members": project["members"]}}
        )
        return jsonify({"success": True}), 200
    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

