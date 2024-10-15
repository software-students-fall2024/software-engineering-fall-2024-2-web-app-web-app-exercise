import os
from flask import Flask, request, redirect, url_for, flash, render_template
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
print(f"MONGO_URI: {mongo_uri}")

app = Flask(__name__)
app.secret_key = os.urandom(13)

client = MongoClient(mongo_uri)
db = client['fitness_db']
todo_collection = db['todo']
exercises_collection = db['exercises']


def search_exercise(query: str):
    exercises = exercises_collection.find({
        "workout_name": {"$regex": query, "$options": "i"}  
    })
    return list(exercises)

def get_exercise(exercise_id: int):
    return exercises_collection.find_one({"_id": exercise_id})

def get_todo():
    todo_list = todo_collection.find_one({"_id": 1})
    if todo_list and "todo" in todo_list:
        return todo_list['todo']
    return []

def delete_todo(exercise_todo_id: int):
    result = todo_collection.update_one(
        {"_id": 1},
        {"$pull": {"todo": {"exercise_todo_id": exercise_todo_id}}}
    )
    
    if result.modified_count > 0:
        print(f"Exercise with To-Do ID {exercise_todo_id} deleted from To-Do List.")
        return True
    else:
        print(f"Exercise with To-Do ID {exercise_todo_id} not found.")
        return False


def add_todo(exercise_id: str):
    exercise = exercises_collection.find_one({"_id": int(exercise_id)})
    
    if exercise:
        todo = todo_collection.find_one({"_id": 1})
        
        if todo and "todo" in todo:
            max_id = max([item.get("exercise_todo_id", 999) for item in todo["todo"]], default=999)
            next_exercise_todo_id = max_id + 1
        else:
            next_exercise_todo_id = 1000

        exercise_item = {
            "exercise_todo_id": next_exercise_todo_id,
            "exercise_id": exercise['_id'],
            "workout_name": exercise["workout_name"],
            "working_time": exercise.get("working_time", 0),
            "reps": exercise.get("reps", 0),
            "weight": exercise.get("weight", 0)
        }

        if todo:
            result = todo_collection.update_one(
                {"_id": 1},
                {"$push": {"todo": exercise_item}}
            )
        else:
            result = todo_collection.insert_one({
                "_id": 1,
                "todo": [exercise_item]
            })

        if result.modified_count > 0 or result.inserted_id:
            print(f"Exercise {exercise['workout_name']} added to To-Do List with exercise_todo_id {next_exercise_todo_id}.")
            return True
        else:
            print(f"Failed to add exercise {exercise['workout_name']} to To-Do List.")
            return False
    else:
        print(f"Exercise with ID {exercise_id} not found.")
        return False

def edit_exercise(exercise_todo_id, times, weight, reps):
    result = todo_collection.update_one(
        {"_id": 1, "todo.exercise_todo_id": exercise_todo_id},
        {"$set": {
            "todo.$.working_time": times,
            "todo.$.reps": reps,
            "todo.$.weight": weight
        }}
    )
    
    if result.modified_count > 0:
        print(f"Exercise with To-Do ID {exercise_todo_id} updated in To-Do List.")
        return True
    else:
        print(f"Failed to update exercise with To-Do ID {exercise_todo_id}.")
        return False

def get_exercise_in_todo(exercise_todo_id: int):
    todo_item = todo_collection.find_one({"_id": 1, "todo.exercise_todo_id": exercise_todo_id})
    
    if not todo_item:
        print(f"Exercise with To-Do ID {exercise_todo_id} not found.")
        return None
    
    for item in todo_item['todo']:
        if item['exercise_todo_id'] == exercise_todo_id:
            return item

    print(f"Exercise with To-Do ID {exercise_todo_id} not found in the list.")
    return None


def get_instruction(exercise_id: int):

    exercise = exercises_collection.find_one({"_id": exercise_id}, {"instruction": 1, "workout_name": 1})
    
    if exercise:
        if "instruction" in exercise:
            return {
                "workout_name": exercise.get("workout_name", "Unknown Workout"),
                "instruction": exercise["instruction"]
            }
        else:
            return {
                "workout_name": exercise.get("workout_name", "Unknown Workout"),
                "instruction": "No instructions available for this exercise."
            }
    else:
        return {
            "error": f"Exercise with ID {exercise_id} not found."
        }

def default_exercises():
    exercises_id = []  # add recommendation exercise id here
    exercises = []
    for i in exercises_id:
        exercises.append(get_exercise(i))

    return exercises


@app.route('/')
def home():
    return redirect(url_for('todo'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        query = request.form.get("query")
        if not query:
            return jsonify({'message': 'Search content cannot be empty.'}), 400
            # return redirect(url_for('search'))
        results = search_exercise(query)
        if len(results) == 0:
            return jsonify({'message': 'Exercise was not found.'}), 404
            # return redirect(url_for('search'))
        
        # test
        # session['results'] = results
        return redirect(url_for('add'))

    exercises = default_exercises()
    return render_template('search.html', exercises=exercises)


@app.route('/todo')
def todo():
    exercises = get_todo()
    return render_template('todo.html', exercises=exercises)


@app.route('/delete_exercise')
def delete_exercise():
    exercises = get_todo()
    return render_template('delete.html', exercises=exercises)


@app.route('/delete_exercise/<int:exercise_todo_id>', methods=['DELETE'])
def delete_exercise_id(exercise_todo_id):
    success = delete_todo(exercise_todo_id)
    if success:
        return jsonify({'message': 'Deleted successfully'}), 204
    else:
        return jsonify({'message': 'Failed to delete'}), 404


@app.route('/add')
def add():
    # test
    # exercises = session['results']
    exercises = []
    return render_template('add.html', exercises=exercises)


@app.route('/add_exercise/<int:exercise_id>', methods=['POST'])
def add_exercise(exercise_id):
    success = add_todo(exercise_id)

    if success:
        return jsonify({'message': 'Added successfully'}), 200
    else:
        return jsonify({'message': 'Failed to add'}), 400


@app.route('/edit/<int:exercise_todo_id>', methods=['GET', 'POST'])
def edit():
    exercise_todo_id = request.args.get('exercise_todo_id')
    exercise_in_todo = get_exercise_in_todo(exercise_todo_id)
    if request.method == 'POST':
        working_time = request.form.get('working_time')
        weight = request.form.get('weight')
        reps = request.form.get('reps')
        edit_exercise(exercise_todo_id, working_time, weight, reps)
        flash('Updated successfully!')
        return redirect(url_for('edit'))

    return render_template('edit.html', exercise_todo_id=exercise_todo_id, exercise=exercise_in_todo)


@app.route('/instructions/<string:exercise_id>')
def instructions(exercise_id):
    exercise = get_exercise(exercise_id)
    instruction = exercise['instruction']

    return render_template('instructions.html', instruction=instruction)


if __name__ == "__main__":
    app.run(debug=True)