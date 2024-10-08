from flask import Blueprint, render_template
from .extensions import mongo
from flask import request

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user_collection = mongo.db.workoutInstructions
    ids_to_find = ["3303","0112","0634","1330","0199","0746","0191","1308","1263"]
    documents = user_collection.find({"id": {"$in":  ids_to_find}})
    workouts=[]
    for document in documents:
        path = document.get("gif_path")
        categories = document.get("categories")
        id = document.get("id")
        name = document.get("name")
        instructions = document.get("instructions")
        target_muscle = document.get("target_muscle")
        workouts.append({"gif_path": path, "categories": categories, "id": id, "name": name, "instructions": instructions, "target_muscle": target_muscle})  # Append each workout to the list

    return render_template('workout_instruction.html', workouts=workouts)  

@main.route('/filter_workouts', methods=['POST'])
def filter_workouts():
    selected_category = request.form.get('category')  # Get the selected category from the form
    user_collection = mongo.db.workoutInstructions
    documents = user_collection.find({"categories": selected_category})  # Filter by category
    workouts = []
    for document in documents:
        path = document.get("gif_path")
        categories = document.get("categories")
        id = document.get("id")
        name = document.get("name")
        instructions = document.get("instructions")
        target_muscle = document.get("target_muscle")
        workouts.append({"gif_path": path, "categories": categories, "id": id, "name": name, "instructions": instructions, "target_muscle": target_muscle})

    return render_template('workout_instruction.html', workouts=workouts, selected_category=selected_category)