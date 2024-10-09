from . import routes
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv
import flask
import flask_login
from src.app import get_db
from src.models.user import user_loader, request_loader
from src.models.user import User



@routes.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Validate form data
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if not (username and password and email):
            return render_template("sign-up.html", message="All fields are required.")

        # Hash the password
        users = get_db().users

        if users.count_documents({ 'email': email }, limit = 1) != 0:
            return render_template("sign-up.html", message="This email is already associated with an account!")
        
        users.insert_one()
        # Store user data in the database
        # Your database insertion code goes here

        return redirect("/login")

    return render_template("sign-up.html")