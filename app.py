import os
from datetime import datetime, timezone
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
        past_sessions = db.sessions.find({}).sort("created_at", -1)

        return render_template("index.html", past=past_sessions)
    
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
        subject = request.form['subject']

        session_data = {
        "focus_time": focus_time,
        "subject": subject,
        "created_at": datetime.now(timezone.utc)
        }

        db.sessions.insert_one(session_data)

        return redirect(url_for("counter"))
    
    @app.route("/congrats")
    def congrats():
        """
        Route for the congratulations page.
        Renders a template that shows the session details and a congratulations message.
        """
        focus_time = request.args.get('focus')
        break_time = request.args.get('break_time')
        reps_no = request.args.get('reps')
        
        return render_template("congrats.html", focus_time=focus_time, break_time=break_time, reps_no=reps_no)

    return app

    @app.route("/counter")
    def counter():
        """
        Route to display the counter with the focus time.
        Retrieves the latest session from the database and passes the data to the template.
        """
        latest = db.sessions.find_one(sort=[("created_at", -1)])

        focus_time = int(latest['focus_time'])

        if focus_time == 0 or focus_time == None:
            focus_time = 0

        return render_template("counter.html", focus_time=focus_time)

    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)