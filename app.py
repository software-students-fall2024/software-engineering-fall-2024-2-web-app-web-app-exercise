import os
from flask import Flask, request, json, redirect, url_for, flash, render_template

app = Flask(__name__)


def get_exersice(query: str):
    return []


def get_todo():
    return []


def delete_todo(exercise_id: int):
    return


def add_todo(exercise_name: str):
    return


def default_exercises():
    exercises = []
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
        results = get_exersice(query)
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


@app.route('/delete_exercise/<int:exercise_id>', methods=['POST'])
def delete_exercise_id(exercise_id):
    delete_todo(exercise_id)
    flash('Delete successfully.')
    return redirect(url_for('delete_exercise'))


@app.route('/add_exercise/<str:exercise_name>', methods=['POST'])
def add_exercise(exercise_name):
    add_todo(exercise_name)
    flash('Add successfully.')
    return redirect(request.referrer or url_for('search'))









