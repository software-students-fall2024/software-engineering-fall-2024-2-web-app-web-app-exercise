import os
from flask import Flask, render_template, request, redirect, url_for, flash
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
        programs = [{"p_name": "1"}, {"p_name": "2"}]
        return render_template("main.html", programs=programs)

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

