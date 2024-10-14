from flask import Flask, request, json, redirect, url_for, flash, render_template, jsonify

app = Flask(__name__)


def get_available_exercises():
    #test
    return [
        {"id": 1, "name": "Burpees"},
        {"id": 2, "name": "Push-ups"},
        {"id": 3, "name": "Squat"},
        {"id": 4, "name": "Deadlift"},
        {"id": 5, "name": "Pilates"},
        {"id": 6, "name": "Box Jumps"}
    ]


def get_todo():
    #test
    return [
        {"id": 7, "name": "Strength", "completed": False},
        {"id": 8, "name": "Cardio", "completed": False},
        {"id": 9, "name": "Interval Training", "completed": False},
        {"id": 10, "name": "Core Workouts", "completed": False},
    ]

def add_todo_by_id(exercise_id):
    print(f"Adding todo with ID: {exercise_id}")
    return True
    

def delete_todo(exercise_id):
    # test
    # db.session.query(Todo).filter_by(id=exercise_id).delete()
    print(f"Deleting todo with ID: {exercise_id}")
    return True 

@app.route('/todo')
def todo():
    exercises = get_todo()
    return render_template('todo.html', exercises=exercises)

@app.route('/delete_exercise')
def delete_exercise():
    exercises = get_todo()
    return render_template('delete.html', exercises=exercises)

@app.route('/delete_exercise/<int:exercise_id>', methods=['DELETE'])
def delete_exercise_id(exercise_id):
    success = delete_todo(exercise_id)
    
    if success:
        return jsonify({'message': 'Deleted successfully'}), 204
    else:
        return jsonify({'message': 'Failed to delete'}), 404

@app.route('/add')
def search():
    exercises = get_available_exercises()
    return render_template('add.html', exercises=exercises)

@app.route('/add_exercise/<int:exercise_id>', methods=['POST'])
def add_exercise(exercise_id):
    success = add_todo_by_id(exercise_id)
    
    if success:
        return jsonify({'message': 'Added successfully'}), 200
    else:
        return jsonify({'message': 'Failed to add'}), 400

if __name__ == "__main__":
    app.run(debug=True)
