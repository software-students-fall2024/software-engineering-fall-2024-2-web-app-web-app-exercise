from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_bcrypt import Bcrypt
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
    app.secret_key = "secret key"
    
    # Flask-login and Flask-Bcrypt setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    bcrypt = Bcrypt(app)
    
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
    
    # User class for Flask-login
    class User(UserMixin):
        def __init__(self, user_id, username, password_hash):
            self.id = user_id
            self.username = username
            self.password_hash = password_hash
    
    @login_manager.user_loader
    def user_loader(user_id):
        """
        load user callback for Flask-Login
        Args:
            user_id (str): the ID of the user

        Returns:
            User object if this user exists
            None if this user does not exist
        """
        user = db.users.find_one({"_id":ObjectId(user_id)})
        if user:
            return User(str(user["_id"]),user["username"],user["password"])
        return None
    
    @app.route("/")
    def signin():
        """
        Route for GET requests to the sign in page
        Displays a form users can fill out to sign in
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("signin.html")
    
    @app.route("/signin_post",methods=["POST"])
    def signin_post():
        """
        Route for POST requests
        save the username and password to the database
        Returns:
            redirect (Response): a redirect response to the home page if sign in successfully
            OR
            redirect (Response): a redirect response to the signin page otherwise
        """
        username = request.form['username']
        password = request.form['password']
        
        user = db.users.find_one({"username":username})
        if user and bcrypt.check_password_hash(user["password"],password):
            user_obj = User(str(user["_id"]),user["username"],user["password"])
            login_user(user_obj)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('signin'))
    
    @app.route('/signup')
    def signup():
        """
        Route for GET requests to the sign up page
        Displays a form users can fill out to sign up
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("signup.html")
    
    @app.route('/signup_post',methods=["POST"])
    def signup_post():
        """
        Route for POST requests
        save the username and password to the database
        Returns:
            redirect (Response): a redirect response to the home page if sign up successfully
            OR
            redirect (Response): a redirect response to the signup page otherwise
        """
        username = request.form['username']
        password = request.form['password']
        if db.users.find_one({"username":username}):
            flash("Username already exists.")
            return redirect(url_for('signup'))
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        db.users.insert_one({"username":username, "password": password_hash})
        flash("registration successful, please sign in.")
        return redirect(url_for('signin'))

    @app.route('/home')
    def home():
        """
        Route for the home page
        Returns: 
            rendered template (str): The rendered HTML template.
        """
        docs = db.records.find({"user_id": current_user.id})
        return render_template("index.html",docs=docs)
    
    @app.route('/add')
    def add():
        """
        Route for GET requests to the add page
        Displays a form users can fill out to add a new record
        Returns:
            rendered template (str): The rendered HTML template.
        """
        doc = {}
        return render_template("add.html", doc=doc, count = 0)
    
    @app.route('/add_post', methods=["POST"])
    def add_post():
        """
        Route for POST requests
        Accepts the new job application and save it to the database
        Returns:
            redirect (Response): a redirect response to the home page
        """
        
        job_title = request.form["job_title"]
        company = request.form["company"]
        location = request.form["location"]
        link = request.form["link"]
        stage = request.form["stage"]
        time = request.form["time"]
        
        if validate_date(time)== False:
            # Insert data into MongoDB
            flash("Invalid date format. Please enter a valid date in YYYY/MM/DD format.")
            doc = {
                "user_id": current_user.id,
                "job_title": job_title,
                "company": company,
                "location": location,
                "link": link,
                "stage": stage,
            }
            #return redirect(url_for("add"), doc)
            return render_template("add.html", doc=doc, count = 1)
        else:
            doc = {
                "user_id": current_user.id,
                "job_title": job_title,
                "company": company,
                "location": location,
                "link": link,
                "stage": stage,
                "time": time
            }
            db.records.insert_one(doc)
            return redirect(url_for("home"))
    

    def validate_date(date_str):
        parts = date_str.split('/')
    
        if len(parts) != 3:
            return False
    
        year, month, day = parts

    # Check if year, month, and day are digits
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return False

    # Convert to integers
        year = int(year)
        month = int(month)
        day = int(day)

    # Basic checks for valid ranges
        if not (1000 <= year <= 9999):  # Check for 4-digit year
            return False
        if not (1 <= month <= 12):  # Month must be between 1 and 12
            return False
        if not (1 <= day <= 31):  # Day must be between 1 and 31 (basic check)
            return False

    # Additional checks for valid days per month
        if month in [4, 6, 9, 11] and day > 30:
            return False  # April, June, September, November have 30 days
        if month == 2:
            if is_leap_year(year):
                if day > 29:
                    return False  # February has 29 days in a leap year
            else:
                if day > 28:
                    return False  # February has 28 days in a non-leap year

        return True

    # Function to check if a year is a leap year
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
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
        return render_template('info.html',doc=doc)
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
        company_name = request.form["company"]
        location_name = request.form["location"]

        search_criteria = {}
        search_criteria["user_id"] = current_user.id
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