from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import bcrypt
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT'] = False

# Fetch the MongoDB URI from .env file
MONGO_URI = os.getenv('MONGO_URI')

# Establish MongoDB connection using PyMongo
client = MongoClient(MONGO_URI)

# Define your database
db = client["occasio"]

# Define collections
collection = db["users"]
events_collection = db["events"]

@app.route('/')
def home():
    if 'username' in session:
        # If the user is already authenticated, redirect them to the home feed
        return redirect(url_for('home_feed'))
    # Render the welcome page with buttons for login and register
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Check if user exists
        user = collection.find_one({"username": username})
        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            session.permanent = False  # Session expires when the browser closes
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

        # Check if user already exists
        if collection.find_one({"username": username}):
            flash("Username already exists. Please choose a different one.")
        else:
            # Hash the password before saving it to the database
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            collection.insert_one({"username": username, "password": hashed_password})
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear the session data to log the user out
    session.clear()
    return redirect(url_for('home'))


@app.route('/home_feed')
def home_feed():
    if 'username' in session:
        # Fetch all events from the MongoDB events collection
        events = list(events_collection.find())

        # Render the home feed page for authenticated users with events
        return render_template('home_feed.html', username=session['username'], events=events)
    else:
        # Redirect to the login page if the user is not authenticated
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
        creator = session['username']  # Get the username of the logged-in user

        # Insert the new event into the database
        events_collection.insert_one({
            "title": title,
            "description": description,
            "date": date,
            "location": location,
            "creator": creator  # Add the creator to the event data
        })

        flash("Event created successfully!")
        return redirect(url_for('home'))

    return render_template('create_event.html')

@app.route('/rsvp/<event_id>', methods=['GET'])
def rsvp_page(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Find the event using events_collection (corrected)
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

    # Add event to user's RSVP'd events
    if 'rsvped_events' not in user:
        user['rsvped_events'] = []

    if event_id not in user['rsvped_events']:
        collection.update_one({'_id': user['_id']}, {'$push': {'rsvped_events': event_id}})
        flash(f"RSVP confirmed for {event['title']}.")
    else:
        flash("You have already RSVP'd for this event.")

    # Redirect to the RSVPed events page
    return redirect(url_for('rsvp_list'))

@app.route('/rsvped_events')
def rsvp_list():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = collection.find_one({'username': session['username']})

    # Get the list of event IDs the user has RSVPed for
    rsvped_event_ids = user.get('rsvped_events', [])
    
    # Fetch all events corresponding to the IDs
    rsvped_events = [events_collection.find_one({'_id': ObjectId(event_id)}) for event_id in rsvped_event_ids]

    return render_template('rsvped_events.html', events=rsvped_events)


if __name__ == "__main__":
    app.run(debug=True)