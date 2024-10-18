from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from bson import ObjectId #to handle mongodb's objectid type

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

@app.route('/edit/<string:entry_id>', methods=['GET','POST'])
def edit(entry_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        entries.update_one({'_id': ObjectId(entry_id)}, {'$set': {'title': new_title, 'content': new_content}})
        return redirect(url_for('home'))
    entry = entries.find_one({'_id': ObjectId(entry_id)})
    return render_template('edit.html', entry=entry)


if __name__ == '__main__':
    app.run(debug=True)