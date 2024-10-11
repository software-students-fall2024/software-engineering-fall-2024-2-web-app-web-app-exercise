from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import bcrypt
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT'] = False

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client["occasio"]

collection = db["users"]
events_collection = db["events"]

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('home_feed'))
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        user = collection.find_one({"username": username})
        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            session.permanent = False  
            return redirect(url_for('home_feed'))
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if collection.find_one({"username": username}):
            flash("Username already exists. Please choose a different one.")
        else:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            collection.insert_one({"username": username, "password": hashed_password})
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/home_feed', methods=['GET'])
def home_feed():
    if 'username' in session:
        search_query = request.args.get('search', '')

        if search_query:
            query = {"title": {"$regex": search_query, "$options": "i"}}
        else:
            query = {}  

        events = list(events_collection.find(query))

        return render_template('home_feed.html', username=session['username'], events=events)
    else:
        return redirect(url_for('login'))

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'username' not in session:
        flash("You need to be logged in to create an event.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        location = request.form['location']
        creator = session['username']  

        event_id = events_collection.insert_one({
            "title": title,
            "description": description,
            "date": date,
            "location": location,
            "creator": creator, 
            "attendees": []  
        }).inserted_id

        collection.update_one(
            {"username": creator},
            {"$push": {"created_events": event_id}}
        )

        flash("Event created successfully!")
        return redirect(url_for('home_feed'))

    return render_template('create_event.html')

@app.route('/rsvp/<event_id>', methods=['GET'])
def rsvp_page(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    event = events_collection.find_one({'_id': ObjectId(event_id)})

    if not event:
        flash("Event not found.")
        return redirect(url_for('home_feed'))

    return render_template('rsvp_page.html', event=event)

@app.route('/rsvp/<event_id>', methods=['POST'])
def rsvp_event(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = collection.find_one({'username': session['username']})
    event = events_collection.find_one({'_id': ObjectId(event_id)})

    if not event:
        flash("Event not found.")
        return redirect(url_for('home_feed'))

    if 'attendees' not in event:
        event['attendees'] = []
        events_collection.update_one({'_id': event['_id']}, {'$set': {'attendees': event['attendees']}})

    if 'rsvped_events' not in user:
        user['rsvped_events'] = []

    if event_id not in user['rsvped_events']:
        collection.update_one({'_id': user['_id']}, {'$push': {'rsvped_events': event_id}})
        flash(f"RSVP confirmed for {event['title']}.")
    elif user['_id'] not in event['attendees']:
        events_collection.update_one({'_id': event['_id']}, {'$push': {'attendees': user['_id']}})
    else:
        flash("You have already RSVP'd for this event.")

    return redirect(url_for('rsvp_list'))

@app.route('/rsvped_events')
def rsvp_list():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = collection.find_one({'username': session['username']})

    rsvped_event_ids = user.get('rsvped_events', [])
    
    rsvped_events = [events_collection.find_one({'_id': ObjectId(event_id)}) for event_id in rsvped_event_ids]

    return render_template('rsvped_events.html', events=rsvped_events)


if __name__ == "__main__":
    app.run(debug=True)