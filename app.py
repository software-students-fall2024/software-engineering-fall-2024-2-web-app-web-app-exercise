from flask import Flask, request, json, redirect, url_for, flash, render_template

app = Flask(__name__)


def search_exersice(query: str):
    return []


def get_exersice(exercise_id: int):
    return {}


def get_todo():
    return []


def delete_todo(exercise_todo_id: int):
    return


def add_todo(exercise_id: str):
    return


def edit_exercise(exercise_todo_id, times, weight, reps):
    return


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
