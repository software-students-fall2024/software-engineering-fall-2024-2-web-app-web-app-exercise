import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymongo 
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId


logged_in = False
projects_as_manager = None
projects_as_member = None
username = None

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

    uri = os.getenv("MONGO_URI")
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
        global username
    
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))
        
        global projects_as_manager, projects_as_member
        projects_as_manager = project_collection.find({'managers': username})
        projects_as_member = project_collection.find({'members': username})
        
        # no matching projects
        if (projects_as_manager == None and projects_as_member == None):
            return render_template("main.html", username=username)
        # only have projects as a member
        elif (projects_as_manager == None):
            return render_template("main.html", username=username, docs_as_member=projects_as_member)
        # only have projects as manager
        elif (projects_as_member == None):
            return render_template("main.html", username=username, docs_as_manager=projects_as_manager)
        # have both manager and member roles in projects
        else:
            return render_template("main.html", username=username, docs_as_manager=projects_as_manager, docs_as_member=projects_as_member)

    # route to login page
    # if POST, check if username and password match
    # if match, redirect to main
    # if not, return to login with error message
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        global username
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
                return redirect(url_for('home',username=username))
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
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        global username
        if request.method == 'POST':
            # Get managers and members as comma-separated strings from the form
            managers = request.form['managers'].split(',')
            members = request.form['members'].split(',')
            if (managers[0] == ""):
                managers = []
            if (members[0] == ""):
                members = []
            managers.append(username) # Creator of project is automatically a manager

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
            return redirect(url_for('home', username=username))

        return render_template('create_project.html')

    # allows the edit of an available project
    @app.route('/edit_project/<post_id>', methods=['GET', 'POST'])
    def edit_project(post_id):
        if (logged_in == False):
            return redirect(url_for('login'))
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        if (request.method == 'POST'):
            managers = request.form['managers'].split(',')
            members = request.form['members'].split(',')
            project_data = {
                "_id": ObjectId(post_id),
                'projectName': request.form['project_name'],
                'description': request.form['description'],
                'start_date': request.form['start_date'],
                'due_date': request.form['due_date'],
                'managers': managers,  # Store managers as an array 
                'members': members,    # Store members as an array
                'tasks': []  # Initially no tasks
            }
            project_collection.replace_one(
                {"_id": ObjectId(post_id)},
                project_data
            )
            return redirect(url_for('project_view', post_id=post_id))
        else:
            managers = ",".join(cur_project['managers'])
            members = ",".join(cur_project['members'])
            return render_template('create_project.html', edit=True, project=cur_project, managers=managers, members=members)

    # route to remove an available project
    @app.route('/remove_project/<post_id>',  methods=['GET'])
    def remove_project(post_id):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})

        project_collection.delete_one(
            {"_id": ObjectId(post_id)}
            )
        return redirect(url_for("home"))

    # route to create task page
    @app.route('/add_task/<post_id>',  methods=['GET', 'POST'])
    def add_task(post_id):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        if (request.method == "POST"):
            tasks = cur_project["tasks"]
            new_task = {
                'taskName': request.form['taskName'],
                'description': request.form['description'],
                'members': request.form['members'].split(','),
                'due_date': request.form['due_date']
            }
            project_collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$push": {"tasks": new_task}}
            )
            return redirect(url_for('project_view', post_id=post_id))
        else:
            return render_template('add_task.html', project=cur_project)

   # this page allows you to edit available tasks
    @app.route("/edit_task/<post_id>/<post_name>", methods=['POST'])
    def edit_task(post_id, post_name):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})

        if (request.method == "POST"):
            tasks = cur_project["tasks"]
            old_task = None

            for task in tasks:
                if (task["taskName"] == post_name):
                    old_task = task
                    break

            members = request.form['members'].split(',')
            new_task = {
                'taskName': request.form['taskName'],
                'description': request.form['description'],
                'members': members,
                'due_date': request.form['due_date']
            }

            if (old_task != new_task):
                project_collection.update_one(
                    {"_id": ObjectId(post_id)},
                    {"$push": {"tasks": new_task}}
                )

                project_collection.update_one(
                    {"_id": ObjectId(post_id)},
                    {"$pull": {"tasks": old_task}}
                )
            return redirect(url_for('project_view', post_id=post_id, post_name=post_name))

    # route to remove an available task
    @app.route('/remove_task/<post_id>/<post_name>',  methods=['GET'])
    def remove_task(post_id, post_name):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        tasks = cur_project["tasks"]
        for task in tasks:
            if (task["taskName"] == post_name):
                old_task = task
                break

        project_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"tasks": old_task}}
            )
        return redirect(url_for('project_view', post_id=post_id, post_name=post_name))
        
    # renders team.html
    # displays team members and tasks
    # will allow you to add/delete/edit tasks
    @app.route("/project_view/<post_id>")
    def project_view(post_id):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})

        managers = cur_project["managers"]
        members = cur_project["members"]
        if (managers[0] == "" and members[0] == ""):
            return render_template("team.html", username=username, project=cur_project, tasks=cur_project["tasks"])
        elif (managers[0] == ""):
            return render_template("team.html", username=username, project=cur_project, tasks=cur_project["tasks"], members=members)
        elif (members[0] == ""):
            return render_template("team.html", username=username, project=cur_project, tasks=cur_project["tasks"], managers=managers)
        else:
            return render_template("team.html", username=username, project=cur_project, tasks=cur_project["tasks"], managers=managers, members=members)
        


    @app.route("/task_view/<post_id>/<post_name>")
    def task_view(post_id, post_name):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))
        
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        tasks = cur_project["tasks"]
        cur_task = None
        # find the correct task to view
        for task in tasks:
            if (task["taskName"] == post_name):
                cur_task = task
                break

        if (cur_task == None):
            # shouldn't happen
            print("Task not found!")
        else:
            return render_template("create_project.html", project=cur_project, task=cur_task, members=",".join(cur_task['members']))
        

    @app.route('/profile')
    def profile():
        global username
        # Check if the user is logged in
        if not logged_in:
            return redirect(url_for('login'))

        # Ensure that the global username is set
        if not username:
            return redirect(url_for('login'))

        # Find the user in the database using the username passed during login
        user = user_list.find_one({'username': username})

        # If the user is found, render the profile page
        if user:
            return render_template(
                "profile.html", 
                username=user['username'], 
                docs_as_manager=projects_as_manager, 
                docs_as_member=projects_as_member
            )
        else:
            return redirect(url_for('login'))
        
    @app.route('/logout')
    def logout():
        global logged_in, projects_as_manager, projects_as_member, username
            
        # Reset the logged_in flag and project variables
        logged_in = False
        projects_as_manager = None
        projects_as_member = None
        username = None
            
        # Flash a message to inform the user of successful logout
        flash("You have been logged out successfully.", "info")
            
        # Redirect the user to the login page
        return redirect(url_for('login'))

    return app
    
if __name__ == "__main__":
    app = create_app()
    flask_port = os.getenv("FLASK_PORT")
    app.run(port=flask_port, debug=True)

