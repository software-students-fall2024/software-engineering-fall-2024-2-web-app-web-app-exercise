from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os
load_dotenv()


def create_app():
    """
    Create and configure the Flask application
    Returns: app: the Flask application object
    """
    app = Flask(__name__)
    
    # mongo setup
    mongo_uri = os.getenv('MONGO_CONNECTION_URI')
    client = MongoClient(mongo_uri)
    db = client.theCoders
    try:
        # Check MongoDB connection
        #client.server_info()  # Will throw an exception if the connection is not successful
        client.admin.command("ping")
        print("Hello, Flask! MongoDB connection successful.")
    except Exception as e:
        print(f"Hello, Flask! MongoDB connection failed: {e}")

    @app.route('/')
    def home():
        """
        Route for the home page
        Returns: 
            rendered template (str): The rendered HTML template.
        """
        docs = db.messages.find()
        return render_template("index.html",docs=docs)
    
    @app.route('/add')
    def add():
        """
        Route for GET requests to the add page
        Displays a form users can fill out to add a new record
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("add.html")
    
    @app.route('/add', methods=["POST"])
    def add_post():
        """
        Route for POST requests
        Accepts the new job application and save it to the database
        Returns:
            _type_: _description_
        """
        
        job_title = request.form["job title"]
        company = request.form["company"]
        doc = {
            "job_title": job_title,
            "company": company,
        }
        db.messages.insert_one(doc)
        return redirect(url_for("home"))
    @app.route('/info/<post_id>')
    def info(post_id):
        """
        Route for GET requests
        Shows the specific info of the record

        Args:
            post_id (str): the ID of the record to see the specific info

        Returns:
            render_template(str): The rendered HTML template.
        """
        doc = db.messages.find_one({"_id": ObjectId(post_id)})
        return render_template('info.html',doc=doc);
    @app.route('/edit/<post_id>')
    def edit(post_id):
        """
        Route for GET requests to the edit page
        Displays a form users can fill out to edit an existing record
        Args:
            post_id (str): The ID of the post to edit
        Returns:
            rendered template (str): The rendered HTML template.
        """
        doc = db.messages.find_one({"_id": ObjectId(post_id)})
        return render_template("edit.html",doc=doc)
    @app.route('/edit/<post_id>',methods=["POST"])
    def edit_post(post_id):
        """
        Route for POST requests to the edit page
        Args:
            post_id (str): The ID of the post edited

        Returns:
            redirect (Response): a redirect response to the home page
        """
        job_title = request.form["job title"]
        company = request.form["company"]
        doc = {
            "job_title": job_title,
            "company": company,
        }
        db.messages.update_one({"_id": ObjectId(post_id)},{"$set": doc})
        return redirect(url_for("home"))
    @app.route("/delete/<post_id>")
    def delete(post_id):
        """
        Route for GET requests to the delete page.
        Deletes the specified record from the database, and then redirects the browser to the home page.
        Args:
            post_id (str): The ID of the post to delete
        Returns:
            redirect (Response): a redirect response to the home page
        """
        db.messages.delete_one({"_id": ObjectId(post_id)})
        return redirect(url_for("home"))
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)