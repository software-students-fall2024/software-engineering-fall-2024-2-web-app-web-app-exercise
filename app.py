from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from bson import ObjectId #to handle mongodb's objectid type
from login import init_login, create_login_routes
import flask_login

load_dotenv()

app = Flask(__name__)
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)

init_login(app)
create_login_routes(app)

db = client["diary"]
entries = db["entries"]
users= db["users"]

@app.route('/')
@flask_login.login_required
def home():
    search_query = request.args.get('search', '')
    user = flask_login.current_user.id
    if search_query:
        filtered_entries = entries.find({"title": {"$regex": search_query, "user_id": ObjectId(user),"$options": "i"}})  # Case-insensitive search
        filtered_entries = list(filtered_entries) 
    else:
        filtered_entries = list(entries.find({"user_id": ObjectId(user)}))  

    if not filtered_entries:
        no_matches = True
    else:
        no_matches = False
    
    return render_template('home.html', entries=filtered_entries, search_query=search_query, no_matches=no_matches)

@app.route('/add', methods=['GET','POST'])
@flask_login.login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        entries.insert_one({'title': title, 'content': content, 'user_id': ObjectId(flask_login.current_user.id)})
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<string:entry_id>', methods=['GET','POST'])
@flask_login.login_required
def edit(entry_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        entries.update_one({'_id': ObjectId(entry_id)}, {'$set': {'title': new_title, 'content': new_content}})
        return redirect(url_for('home'))
    entry = entries.find_one({'_id': ObjectId(entry_id)})
    return render_template('edit.html', entry=entry)

@app.route('/delete/<entry_id>', methods=['GET', 'POST'])
@flask_login.login_required
def delete_entry(entry_id):
    if request.method == 'POST':
        entries.delete_one({'_id': ObjectId(entry_id)})
        return redirect(url_for('home'))
    entry = entries.find_one({'_id': ObjectId(entry_id)})
    return render_template('delete.html', entry_id=entry_id, entry=entry)


if __name__ == '__main__':
    app.run(debug=True)