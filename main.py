
from flask import Flask, render_template
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database_name"
mongo = PyMongo(app)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def add():
    return render_template('add.html')

@app.route('/')
def delete():
    return render_template('delete.html')

@app.route('/')
def edit():
    return render_template('edit.html')

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/')
def view():
    return render_template('view.html')

if __name__ == '__main__':
    app.run(debug=True)
