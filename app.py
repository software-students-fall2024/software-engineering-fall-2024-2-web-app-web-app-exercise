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

            # Create the project data
            project_data = {
                'projectName': request.form['project_name'],
                'description': request.form['description'],
                'start_date': request.form['start_date'],
                'due_date': request.form['due_date'],
                'managers': [username],  # Store managers as an array 
                'members': [],    # Store members as an array
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
            managers = cur_project['managers']
            members = cur_project['members']
            project_data = {
                "_id": ObjectId(post_id),
                'projectName': request.form['project_name'],
                'description': request.form['description'],
                'start_date': request.form['start_date'],
                'due_date': request.form['due_date'],
                'managers': managers,  # Store managers as an array 
                'members': members,    # Store members as an array
                'tasks': cur_project['tasks'] 
            }
            project_collection.replace_one(
                {"_id": ObjectId(post_id)},
                project_data
            )
            return redirect(url_for('project_view', post_id=post_id))
        else:
            managers = cur_project['managers']
            members = cur_project['members']

            if (len(managers) == ""):
                global username
                managers.append(username)

            all_users = user_list.find({
                "username":
                {"$nin": managers}
            })

            all_users2 = user_list.find({
                "username":
                {"$nin": members}
            })
            return render_template('create_project.html', edit=True, project=cur_project, managers=managers, members=members, all_users=all_users, all_users2=all_users2)

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

    @app.route('/remove_user/<post_id>/<post_name>', methods=['GET'])
    def remove_user(post_id, post_name):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        name = request.args.get('username')

        if (post_name == "member"):
            project_collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$pull": {"members": name}}
            )
        elif (post_name == "manager"):
            project_collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$pull": {"managers": name}}
            )
        return redirect(url_for("edit_project", post_id=post_id))
    
    @app.route('/remove_task_user/<post_id>/<post_name>', methods=['GET'])
    def remove_task_user(post_id, post_name):
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        name = request.args.get('username')
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        if (post_name == "No Members Added Yet"):
            return redirect(url_for("add_task", post_id=post_id, post_name=post_name))
        else:
            cur_members = post_name
            cur_members = cur_members.split(",")
            cur_members.remove(name)
            if (len(cur_members) == 0):
                return redirect(url_for("add_task", post_id=post_id, post_name="No Members Added Yet"))
            else:
                cur_members = ",".join(cur_members)
                return redirect(url_for("add_task", post_id=post_id, post_name=cur_members))

    @app.route('/add_task_user/<post_id>/<post_name>', methods=['GET'])
    def add_task_user(post_id, post_name):
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        name = request.args.get('username')
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        if (post_name == "No Members Added Yet"):
            cur_members = name
            print("setting default\n")
            return redirect(url_for("add_task", post_id=post_id, post_name=cur_members))
        else:
            print("adding to array\n")
            cur_members = post_name
            cur_members = cur_members.split(",")
            cur_members.append(name)
            cur_members = ",".join(cur_members)
            return redirect(url_for("add_task", post_id=post_id, post_name=cur_members, cur_members=cur_members))

    @app.route('/add_task_user_edit/<post_id>/<post_name>/<post_task>', methods=['GET'])
    def add_task_user_edit(post_id, post_name, post_task):
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        name = request.args.get('username_for_edit')
        task_list = cur_project["tasks"]
        cur_task = None
        for task in task_list:
            if task['taskName'] == post_task:
                cur_task = task
                break
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        all_members = task['members']
        if (post_name == "No Members Added Yet"):
            cur_members = name
            print("setting default\n")
            return render_template("add_task.html", post_id=post_id, post_name=cur_members, members=all_members, cur_task=cur_task, project=cur_project, edit=True)
        else:
            cur_members = post_name
            cur_members_arr = cur_members.split(",")
            cur_members_arr.append(name)
            for member in cur_members_arr:
                if member in all_members:
                    all_members.remove(member)
            cur_members = ",".join(cur_members_arr)
            
            return render_template("add_task.html", post_id=post_id, post_name=cur_members, members=all_members, members2=cur_members_arr, project=cur_project, cur_members=cur_members, cur_task=cur_task, edit=True)
    
    @app.route('/remove_task_user_edit/<post_id>/<post_name>/<post_task>', methods=['GET'])
    def remove_task_user_edit(post_id, post_name, post_task):
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        name = request.args.get('username_for_edit')
        task_list = cur_project["tasks"]
        cur_task = None
        for task in task_list:
            if task['taskName'] == post_task:
                cur_task = task
                break
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        all_members = task['members']
        if (post_name == "No Members Added Yet"):
            cur_members = name
            print("setting default\n")
            return render_template("add_task.html", post_id=post_id, post_name=cur_members, members=all_members, cur_task=cur_task, project=cur_project, edit=True)
        else:
            cur_members = post_name
            cur_members_arr = cur_members.split(",")
            cur_members_arr.remove(name)
            for member in cur_members_arr:
                if member in all_members:
                    all_members.remove(member)
            cur_members = ",".join(cur_members_arr)
            if (len(cur_members_arr) == 0):
                cur_members = "No Members Added Yet"
            return render_template("add_task.html", post_id=post_id, post_name=cur_members, members=all_members, members2=cur_members_arr, project=cur_project, cur_members=cur_members, cur_task=cur_task, edit=True)
    
    @app.route('/add_user/<post_id>/<post_name>', methods=['GET'])
    def add_user(post_id, post_name):
        # not logged in yet, return to login
        if (logged_in == False):
            return redirect(url_for('login'))

        name = request.args.get('username')

        if (post_name == "member"):
            project_collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$push": {"members": name}}
            )
        elif (post_name == "manager"):
            project_collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$push": {"managers": name}}
            )
        return redirect(url_for("edit_project", post_id=post_id))

    # route to create task page
    @app.route('/add_task/<post_id>/<post_name>',  methods=['GET', 'POST'])
    def add_task(post_id, post_name):
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
            cur_members = post_name
            all_members = cur_project['members'] + cur_project['managers']
            members2 = cur_members.split(",")
            for member in members2:
                if member in all_members:
                    all_members.remove(member)
            return render_template('add_task.html', cur_members=cur_members, project=cur_project, members=all_members, members2=members2)

   # this page allows you to edit available tasks
    @app.route("/edit_task/<post_id>/<post_name>", methods=['POST', 'GET'])
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
        if (len(managers) == 0 and len(members) == 0):
            return render_template("team.html", username=username, project=cur_project, tasks=cur_project["tasks"])
        elif (len(managers) == 0):
            return render_template("team.html", username=username, project=cur_project, tasks=cur_project["tasks"], members=members)
        elif (len(members) == 0):
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
            members2 = cur_task['members']
            if (len(members2) == 0):
                all_members = cur_project['managers'] + cur_project['members']
                return render_template('add_task.html', cur_members="No Members Added Yet", project=cur_project, members=all_members, members2=members2, edit=True)
            else:
                all_members = cur_project['managers'] + cur_project['members']
                for member in members2:
                    if member in all_members:
                        all_members.remove(member)
                cur_members = ",".join(members2)
                
                return render_template('add_task.html', cur_members=cur_members, project=cur_project, members=all_members, members2=members2, edit=True, cur_task=cur_task)

    @app.route('/search_tasks/<post_id>', methods=['GET'])
    def search_tasks(post_id):
        task_name = request.args.get('task_name', '').lower()
        cur_project = project_collection.find_one({"_id": ObjectId(post_id)})
        # check if exists - no - return to project view
        if not cur_project:
            return redirect(url_for('project_view', post_id=post_id))
        # tasks = [task for task in cur_project['tasks'] if task_name in task['taskName'].lower()]

        return redirect(url_for('task_view', post_id=post_id, post_name=task_name))


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

