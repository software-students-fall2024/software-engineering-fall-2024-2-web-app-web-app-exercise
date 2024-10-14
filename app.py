from flask import Flask, request, jsonify, redirect, url_for, flash, render_template, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def search_exersice(query: str):
    return []


def get_exersice(exercise_id: int):
    return {}


def get_todo():
    #test
    return [
        {"name": "Strength", "completed": False},
        {"name": "Cardio", "completed": True},
        {"name": "Interval Training", "completed": False},
        {"name": "Core Workouts", "completed": False},
        {"name": "Flexibility & Mobility", "completed": True}
    ]


def delete_todo(exercise_todo_id: int):
    return True


def add_todo(exercise_id: str):
    return True


def edit_exercise(exercise_todo_id, working_time, weight, reps):
    return


def get_exercise_in_todo(exercise_todo_id):
    return {}


def default_exercises():
    exercises_id = []  # add recommendation exercise id here
    exercises = []
    for i in exercises_id:
        exercises.append(get_exersice(i))

    return exercises


@app.route('/')
def home():
    return redirect(url_for('todo'))


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
        session['results'] = results
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
    exercises = session['results']
    return render_template('add.html', exercises=exercises)


@app.route('/add_exercise/<int:exercise_id>', methods=['POST'])
def add_exercise(exercise_id):
    success = add_todo(exercise_id)

    if success:
        return jsonify({'message': 'Added successfully'}), 200
    else:
        return jsonify({'message': 'Failed to add'}), 400


@app.route('/edit', methods=['GET', 'POST'])
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
    exercise = get_exersice(exercise_id)
    instruction = exercise['instruction']

    return render_template('instructions.html', instruction=instruction)


if __name__ == "__main__":
    app.run(debug=True)
