import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """

    app = Flask(__name__)
    app.secret_key = 'secret'

    #mongodb connect
    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]
    users = db['users']
    tasks = db['tasks']

    #Configure Flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)

    #define user
    class User(UserMixin):
        def __init__(self, username):
            self.username = username

        def get_id(self):
            return self.username
 
    user = None
    @login_manager.user_loader
    def load_user(user_id):
        user = users.find_one({"username": user_id})
        return User(username=user["username"]) if user else None

    login_manager.user_loader(load_user)

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Check if the username already exists
            if users.find_one({'username': username}):
                flash('Username already exists. Choose a different one.', 'danger')
            else:
                users.insert_one({'username': username, 'password': password})
                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect('/')

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Check if the username and password match
            user = users.find_one({'username': username, 'password': password})

            if user :
                user = User(user['username'])
                login_user(user)
                return redirect('/')
            else:
                flash('Invalid username or password.')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        # Logout the user
        logout_user()
        return redirect('/login')

    @app.route('/api/status')
    def status():
        return jsonify({'logged_in': current_user.is_authenticated})   

    @app.route('/')
    def home():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        if not current_user.is_authenticated :
            return redirect('/login')
        docs = tasks.find({"user": {'$in': [current_user.username]}})
        return render_template("index.html", docs=docs)

    @app.route("/create")
    @login_required
    def add_task():
        """
        Route for the adding task page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("form.html")

    @app.route("/create", methods=["POST"])
    def create_task():
        """
        Route for POST requests to the create page.
        Accepts the form submission data for a new document and saves the document to the database.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        name = request.form["fname"]
        description = request.form["fmessage"]

        doc = {
            "name": name,
            "description": description,
            "user": current_user.username,
        }
        db.tasks.insert_one(doc)

        return redirect(url_for("home"))

    @app.route("/edit/<post_id>")
    @login_required
    def edit(post_id):
        """
        Route for GET requests to the edit page.
        Displays a form users can fill out to edit an existing record.
        Args:
            post_id (str): The ID of the post to edit.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        doc = tasks.find_one({"_id": ObjectId(post_id)})
        return render_template("item.html", doc=doc)

    @app.route("/edit/<post_id>", methods=["POST"])
    def edit_post(post_id):
        """
        Route for POST requests to the edit page.
        Accepts the form submission data for the specified document and updates the document in the database.
        Args:
            post_id (str): The ID of the post to edit.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        name = request.form["fname"]
        description = request.form["fmessage"]

        doc = {
            "name": name,
            "description": description,
            "user": current_user.username
        }

        db.tasks.update_one({"_id": ObjectId(post_id)}, {"$set": doc})

        return redirect(url_for("home"))

    @app.route("/delete/<post_id>")
    def delete(post_id):
        """
        Route for GET requests to the delete page.
        Deletes the specified record from the database, and then redirects the browser to the home page.
        Args:
            post_id (str): The ID of the post to delete.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        tasks.delete_one({"_id": ObjectId(post_id)})
        return redirect(url_for("home"))


    @app.errorhandler(Exception)
    def handle_error(e):
        """
        Output any errors - good for debugging.
        Args:
            e (Exception): The exception object.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("error.html", error=e)

    return app


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "3000")
    app = create_app()

    app.run(port=FLASK_PORT)