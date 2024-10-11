import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
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
    app.secret_key = os.getenv('SECRET_KEY') 

    @app.route("/main")
    def home():
        programs = [{"p_name": "1"}, {"p_name": "2"}]
        return render_template("main.html", programs=programs)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username == "admin" and password == "password123":
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid credentials, please try again.", "danger")
        
        return render_template("login.html")
    
    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
