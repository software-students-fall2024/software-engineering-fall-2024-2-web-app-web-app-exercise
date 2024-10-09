from . import routes
from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
from dotenv import load_dotenv
import flask
import flask_login
from src.models.user import user_loader, request_loader
from src.models.user import User
from src.app import get_db

@routes.route("/login",methods=['GET','POST'])
def login():
    users = get_db().users
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    username = flask.request.form['username']
    password = flask.request.form['password']
    result = users.find_one({}, {"username":username, "password":password})
    if result:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('routes.protected'))

    return 'Bad login'

@routes.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id