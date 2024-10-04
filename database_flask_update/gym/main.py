from flask import Blueprint, render_template
from .extensions import mongo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user_collection = mongo.db.workoutInstructions
    document = user_collection.find_one({"id": "3303"})
    if document:
        path = document.get("gif_path")
        return render_template('index.html', gif_path=path)
    else:
        return "Document with id 3303 not found"
