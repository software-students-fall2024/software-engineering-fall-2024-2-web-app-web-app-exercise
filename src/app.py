import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv

from database_initialisation import *


def create_app():
    app = Flask(__name__)

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['db']
    database_add(db, "pedals", "data/pedal_data.json")

    @app.route("/")
    def login():
        return render_template('login.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port='5000')
