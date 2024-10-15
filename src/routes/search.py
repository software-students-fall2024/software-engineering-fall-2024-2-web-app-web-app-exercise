from . import routes
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv
import flask
import flask_login
from src.models.user import user_loader, request_loader
from src.models.user import User
from src.app import get_db

@routes.route('/search', methods=["GET"])
@flask_login.login_required
def search():

    query = request.args.get('query', '')
    board_id = request.args.get('board_id', '')

    pedals = get_db().pedals
  
    all_pedals = list(pedals.find({}))
    
   
    pedals = [pedal for pedal in all_pedals if query.lower() in pedal['name'].lower()]

   
    return render_template('search.html', pedals=pedals, board_id=board_id)