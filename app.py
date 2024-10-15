import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
import flask_login
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

    app.secret_key = 'Amos_Bloomberg'
    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
    db = cxn[os.getenv("MONGO_DBNAME")]

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    
    class User(UserMixin):
        pass

    @login_manager.user_loader
    def load_user(user_id):
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            user = User()
            user.id = str(user_data['_id'])
            return user
        return None


    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user_data = db.users.find_one({"username": username})

            if user_data and user_data['password'] == password: 
                user = User()
                user.id = str(user_data['_id'])
                login_user(user)
                return redirect(url_for('home_screen'))
            else:
                flash('Invalid username or password.')

        return render_template('login.html')

    @app.route("/home_screen")
    @login_required
    def home_screen():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """

        past_sessions = db.sessions.find({"username": current_user.id}).sort("created_at", -1)

        return render_template("home_screen.html", past=past_sessions, username=current_user.id)
    
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
        "username": current_user.id,
        "focus_time": focus_time,
        "subject": subject,
        "created_at": datetime.now(timezone.utc)
        }

        db.sessions.insert_one(session_data)

        return redirect(url_for("counter"))

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