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
        docs = db.records.find()
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
            redirect (Response): a redirect response to the home page
        """
        
        job_title = request.form["job title"]
        company = request.form["company"]
        location = request.form["location"]
        link = request.form["link"]
        stage = request.form["stage"]
        time = request.form["time"]
        doc = {
            "job_title": job_title,
            "company": company,
            "location": location,
            "link": link,
            "stage": stage,
            "time": time
        }
        db.records.insert_one(doc)
        return redirect(url_for("home"))
    @app.route('/info/<record_id>')
    def info(record_id):
        """
        Route for GET requests
        Shows the specific info of the record

        Args:
            record_id (str): the ID of the record to see the specific info

        Returns:
            render_template(str): The rendered HTML template.
        """
        doc = db.records.find_one({"_id": ObjectId(record_id)})
        return render_template('info.html',doc=doc);
    @app.route('/edit/<record_id>')
    def edit(record_id):
        """
        Route for GET requests to the edit page
        Displays a form users can fill out to edit an existing record
        Args:
            record_id (str): The ID of the record to edit
        Returns:
            rendered template (str): The rendered HTML template.
        """
        doc = db.records.find_one({"_id": ObjectId(record_id)})
        return render_template("edit.html",doc=doc)
    @app.route('/edit/<record_id>',methods=["POST"])
    def edit_post(record_id):
        """
        Route for POST requests to the edit page
        Args:
            record_id (str): The ID of the record edited

        Returns:
            redirect (Response): a redirect response to the home page
        """
        job_title = request.form["job title"]
        company = request.form["company"]
        location = request.form["location"]
        link = request.form["link"]
        stage = request.form["stage"]
        time = request.form["time"]
        doc = {
            "job_title": job_title,
            "company": company,
            "location": location,
            "link": link,
            "stage": stage,
            "time": time
        }
        db.records.update_one({"_id": ObjectId(record_id)},{"$set": doc})
        return redirect(url_for("home"))
    @app.route("/delete/<record_id>")
    def delete(record_id):
        """
        Route for GET requests to the delete page.
        Deletes the specified record from the database, and then redirects the browser to the home page.
        Args:
            record_id (str): The ID of the record to delete
        Returns:
            redirect (Response): a redirect response to the home page
        """
        db.records.delete_one({"_id": ObjectId(record_id)})
        return redirect(url_for("home"))
    @app.route("/search")
    def search():
        """
        Route for GET requests to the search page.
        Searchs the certain records based on the user's inputs
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("search.html")
    @app.route("/search_post",methods=["POST"])
    def search_post():
        """
        Route for POST requests to the result page
        Shows the result of the user's search
        Returns:
            rendered template (str): The rendered HTML template.
        """
        job_title = request.form["job title"]
        company_name = request.form["company"]#
        location_name = request.form["location"]

        search_criteria = {}
        if job_title and job_title.strip():  # Check if job is not empty
            search_criteria['job_title'] = job_title
        if company_name and company_name.strip():  # Check if company is not empty
            search_criteria['company'] = company_name
        if location_name and location_name.strip():  # Check if location is not empty
            search_criteria['location'] = location_name

     #   docs = db.records.find({"job_title":job_title, "company":company_name})#
        docs = db.records.find(search_criteria)
        docs_list = list(docs)
        return render_template("result.html",docs=docs_list,count=len(docs_list))
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)