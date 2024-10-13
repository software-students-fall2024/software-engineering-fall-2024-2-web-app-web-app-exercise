import os
from flask import Flask, request, json, redirect, url_for, flash, render_template, session

app = Flask(__name__)
app.secret_key = os.urandom(13)


def get_user(username: str):
    return {}


def get_exersice(query: str):
    return []


def get_todo(username: str):
    return []


def update_todo(username: str, new_todo: []):
    return


@app.route('/')
def home():
    return '<h1>This is the home page.</h1>'


@app.route('/profile')
def profile():
    if 'user' not in session:
        flash("Please Login!")
        redirect(url_for('login'))
    user = session['user']
    return render_template('profile.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash("Please enter username and password!")
            return redirect(url_for('login'))

        user = get_user(username)

        if user is None:
            flash("Please enter correct username!")
            return redirect(url_for('login'))
        elif user['password'] != password:
            flash('Please enter correct password!')
            return redirect(url_for('login'))
        else:
            session['user'] = {'username': user['username']}
            flash('Login successfully!')
            return redirect(url_for('profile'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You are logged out!")
    return redirect(url_for('login'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        query = request.form.get("query")
        if not query:
            flash('Search content cannot be empty.')
            redirect(url_for('search'))
        results = get_exersice(query)
        return render_template('search.html', query=query, results=results)

    return render_template('search.html', results=None)


@app.route('/todo')
def todo():
    if 'user' not in session:
        flash("Please Login!")
        redirect(url_for('login'))

    username = session['user']['username']
    exercises = get_todo(username)
    return render_template('todo.html', exercises=exercises)


@app.route('/delete_exercise')
def delete_exercise():
    username = session['user']['username']
    exercises = get_todo(username)
    return render_template('delete_exercise.html', exercises=exercises)


@app.route('/delete_exercise/<int:exercise_id>', methods=['POST'])
def delete_exercise_id(exercise_id):
    username = session['user']['username']
    exercises = get_todo(username)

    new_todo = []
    for i in exercises:
        if i['id'] != exercise_id:
            new_todo.append(i)

    update_todo(username, new_todo)
    flash('Delete successfully.')
    return redirect(url_for('delete_exercise'))








