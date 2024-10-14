import os
from flask import Flask, request, json, redirect, url_for, flash, render_template, session
from dotenv import load_dotenv

from pymongo import MongoClient
load_dotenv() 


mongo_uri = os.getenv('MONGO_URI')
print(f"MONGO_URI: {mongo_uri}")

mongo_uri = os.getenv('MONGO_URI')

app = Flask(__name__)
app.secret_key = os.urandom(13)

client = MongoClient(mongo_uri)
db = client['fitness_db']
todo_collection = db['todo']
exercises_collection = db['exercises']


def search_exercise(query: str):
    exercises = exercises_collection.find({
        "$or": [
            {"workout_name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    })
    return list(exercises)

def get_exercise(exercise_id: int):
    exercise = exercises_collection.find_one({"_id": exercise_id})
    return exercise
def get_todo():
    todo_list = todo_collection.find_one({"_id": 1})  
    if todo_list and "todo" in todo_list:
        return todo_list['todo']  
    return []

def delete_todo(exercise_todo_id: int):
    todo_collection.update_one(
        {"_id": 1},
        {"$pull": {"todo": {"exercise_id": exercise_todo_id}}}
    )
    print(f"Exercise with ID {exercise_todo_id} deleted from To-Do List.")



def add_todo(exercise_id: str):
    exercise = exercises_collection.find_one({"_id": int(exercise_id)})
    
    if exercise:
        exercise_item = {
            "exercise_id": exercise['_id'],  
            "workout_name": exercise["workout_name"],
            "working_time": exercise.get("working_time", 0),  
            "reps": exercise.get("reps", 0), 
            "weight": exercise.get("weight", 0)  
        }


        todo = todo_collection.find_one({"_id": 1})

        if todo:
            
            todo_collection.update_one(
                {"_id": 1},
                {"$push": {"todo": exercise_item}}
            )
        else:
 
            todo_collection.insert_one({
                "_id": 1,
                "todo": [exercise_item]
            })
        print(f"Exercise {exercise['workout_name']} added to To-Do List.")
    else:
        print(f"Exercise with ID {exercise_id} not found.")



def edit_exercise(exercise_todo_id, times, weight, reps):
    todo_collection.update_one(
        {"_id": 1, "todo.exercise_id": exercise_todo_id},
        {"$set": {
            "todo.$.working_time": times,
            "todo.$.reps": reps,
            "todo.$.weight": weight
        }}
    )
    print(f"Exercise with ID {exercise_todo_id} updated in To-Do List.")

def default_exercises():
    exercises_id = []  # add recommendation exercise id here
    exercises = []
    for i in exercises_id:
        exercises.append(get_exersice(i))

    return exercises

@app.route('/')
def home():
    return '<h1>This is the home page.</h1>'


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        query = request.form.get("query")
        if not query:
            flash('Search content cannot be empty.')
            redirect(url_for('search'))
        results = search_exersice(query)
        if len(results) == 0:
            flash('Exercise was not found.')
            redirect(url_for('search'))
        return render_template('add_exercise_page.html', query=query, results=results)

    exercises = default_exercises()
    return render_template('search.html', exercises=exercises)


@app.route('/todo')
def todo():
    exercises = get_todo()
    return render_template('todo.html', exercises=exercises)


@app.route('/delete_exercise')
def delete_exercise():
    exercises = get_todo()
    return render_template('delete_exercise.html', exercises=exercises)


@app.route('/delete_exercise/<int:exercise_todo_id>')
def delete_exercise_id(exercise_todo_id):
    delete_todo(exercise_todo_id)
    flash('Deleted successfully.')
    return redirect(url_for('delete_exercise'))


@app.route('/add_exercise/<str:exercise_id>')
def add_exercise(exercise_id):
    add_todo(exercise_id)
    flash('Added successfully.')
    return redirect(request.referrer or url_for('search'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    exercise_todo_id = request.args.get('exercise_todo_id')
    if request.method == 'POST':
        times = request.form.get('times')
        weight = request.form.get('weight')
        reps = request.form.get('reps')
        edit_exercise(exercise_todo_id, times, weight, reps)
        flash('Updated successfully!')
        return redirect(url_for('edit'))

    return render_template('edit.html', exercise_todo_id=exercise_todo_id)


@app.route('/instructions/<str:exercise_id>')
def instructions(exercise_id):
    exercise = get_exersice(exercise_id)
    instruction = exercise['instruction']

    return render_template('instructions.html', instruction=instruction)