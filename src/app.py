import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)


    @app.route("/")
    def login():
        return render_template('login.html')
    
    return app

app = create_app()
app.run(port='5000')