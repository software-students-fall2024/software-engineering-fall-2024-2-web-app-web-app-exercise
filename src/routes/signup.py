from . import routes
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv
import flask
import flask_login

from src.models.user import user_loader, request_loader
from src.models.user import User

@routes.route('/sign-up', methods=["GET"])
def signup():
    return(render_template('sign-up.html'))