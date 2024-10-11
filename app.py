import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
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

    @app.route("/")
    def home():
        # mock data for testing
        programs = [{"p_name": "1"}, {"p_name": "2"}]
        return render_template("main.html", programs=programs)

    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)