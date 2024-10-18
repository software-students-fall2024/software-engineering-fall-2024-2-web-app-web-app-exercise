from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)

db = client["diary"]
entries = db["entries"]

@app.route('/')
def home():
    all_entries = entries.find() 
    return render_template('home.html', entries=all_entries)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        entries.insert_one({'title': title, 'content': content})
        return redirect(url_for('home'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)