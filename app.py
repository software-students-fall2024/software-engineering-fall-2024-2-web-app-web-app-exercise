import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import flask_login
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

    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]
    users = db['users']

    class User(flask_login.UserMixin):
        pass

    #tasks = db['tasks']

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
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Check if the username and password match
            user = users.find_one({'username': username, 'password': password})
            if user:
                flash('Login successful.', 'success')
            # Add any additional logic, such as session management
            else:
                flash('Invalid username or password. Please try again.', 'danger')

        return render_template('login.html')

    @app.route("/")
    def home():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        #docs = db.tasks.find({}).sort("created_at", -1)
        return render_template("index.html")# docs=docs)

    @app.route("/create")
    def add_task():
        """
        Route for the adding task page
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
            "finished": "false",
            "created_at": datetime.datetime.utcnow(),
        }
        db.messages.insert_one(doc)

        return redirect(url_for("home"))

    @app.route("/edit/<post_id>")
    def edit(post_id):
        """
        Route for GET requests to the edit page.
        Displays a form users can fill out to edit an existing record.
        Args:
            post_id (str): The ID of the post to edit.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        doc = db.messages.find_one({"_id": ObjectId(post_id)})
        return render_template("edit.html", doc=doc)

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
            "finished": "true",
            "created_at": datetime.datetime.utcnow(),
        }

        db.messages.update_one({"_id": ObjectId(post_id)}, {"$set": doc})

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
        db.messages.delete_one({"_id": ObjectId(post_id)})
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