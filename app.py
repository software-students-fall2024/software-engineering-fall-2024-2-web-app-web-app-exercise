import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
import certifi
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """

    app = Flask(__name__)

    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
    db = cxn[os.getenv("MONGO_DBNAME")]

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    @app.route("/")
    def home_screen():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        # past_sessions = db.sessions.find({}).sort("created_at", -1)
        return render_template("home.html")
    
    @app.route("/start-session")
    def session_form():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("start-session.html")
    
    @app.route("/start-session", methods=["POST"])
    def create_session():
        """
        Route for POST requests to the create page.
        Accepts the form submission data for a new document and saves the document to the database.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        focus_time = request.form['focus']
        break_time = request.form['break']
        reps_no = request.form['reps']
        # add session info to database
        return redirect(url_for("counter"))

    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)