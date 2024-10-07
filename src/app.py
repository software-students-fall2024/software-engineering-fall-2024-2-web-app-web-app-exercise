import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv


def db_connect():

    load_dotenv()
    username = os.getenv('MONGO_USERNAME')
    password = os.getenv('MONGO_PASSWORD')
    db_name = os.getenv('MONGO_DBNAME')

    uri = f"mongodb+srv://{username}:{password}@cluster0.lrz8n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client[db_name]
    return db


def create_app():
    app = Flask(__name__)

    db = db_connect()

    @app.route("/")
    def login():
        return render_template('login.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port='5000')
