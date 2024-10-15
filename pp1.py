import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

def create_app():
    app = Flask(__name__)
    programs = [{"p_name": "1", "id": "1", "tasks": [{"id": "1.1"},{"id": "1.2"}]}, {"p_name": "2", "id": "2", "tasks": [{"id": "2.1"}]}]

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
        return render_template("main.html", programs=programs)
    
    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html")
        
    # team page
    @app.route('/program/<id>')
    def program(id):
        for program in programs:
            if program["id"] == id:
                return render_template("team.html", program=program)
    
    # team page / Assign task
    @app.route('/<id>/assign-task', methods=['POST'])
    def addTask(id):
        data = request.get_json()
        task_name = data.get('taskName')
        if task_name:
            for program in programs:
                if program["id"] == id:
                    program["tasks"].append({"id": task_name})
                return jsonify({"success": True}), 200
            return jsonify({"error": "Program not found"}), 404
        else:
            return jsonify({"error": "Task name is required"}), 400
        
    # team page / Edit task
    @app.route('/<id>/edit-task/<task_id>', methods=['POST'])
    def edit_task(id, task_id):
        data = request.get_json()
        new_task_name = data.get('taskName')
        if new_task_name:
            for program in programs:
                if program["id"] == id:
                    for task in program["tasks"]:
                        if task["id"] == task_id:
                            task["id"] = new_task_name
                            return jsonify({"success": True, "task": {"id": task_id, "name": new_task_name}}), 200
            return jsonify({"error": "Program or Task not found"}), 404
        else:
            return jsonify({"error": "Task name is required"}), 400    
             
    # team page / Delete task
    @app.route('/<id>/delete-task/<task_id>', methods=['DELETE'])
    def delete_task(id, task_id):
        # Find the program with the given id
        for program in programs:
            if program["id"] == id:
                # Find the task with the given task_id
                for task in program["tasks"]:
                    if task["id"] == task_id:
                        # Remove the task from the program
                        program["tasks"].remove(task)
                        return jsonify({"success": True}), 200
                return jsonify({"error": "Task not found"}), 404
        return jsonify({"error": "Program not found"}), 404        
        
        
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

