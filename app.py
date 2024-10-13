import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from Models import User, Nutrition
from bson.objectid import ObjectId
from fuzzywuzzy import fuzz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify, render_template, request, redirect, abort, url_for, make_response, send_from_directory,session
from functools import wraps
"""
Deafult root of the flask: templates

HTTP status code reference: https://docs.python.org/3/library/http.html
APScheduler reference: https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/background.html#module-apscheduler.schedulers.background
"""
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# mongodb connection - exercise_data
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["exercise_db"]
exercise_collection = db["exercise"]

# mongodb connection - usr
user_service = User(db)

# mongodb connection - food
nutrition_service = Nutrition(db)

# this function is for customize rout to serve the image
@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory('images', filename)

# index means home
@app.route("/")
def index():
    user_name = session.get('user_name')
    if user_name:
        daily_workout_plan = user_service.get_workout_plan(user_name)
    else:
        daily_workout_plan = []
    return render_template("index.html", daily_workout_plan=daily_workout_plan, user_name=user_name)

# return authentication page
@app.route('/auth', methods=['GET'])
def auth():
    return render_template('auth.html')

@app.route('/logout')
# logout and return to index page
def logout():
    session.pop('user_name', None)
    return redirect(url_for('index'))

@app.route("/workout_instruction", methods=["GET", "POST"])
def show_workout_instruction():
    user_name = session.get('user_name')
    # Check if the request is for adding a plan, default to be False
    for_plan = request.args.get("for_plan", "false").lower() == "true" or request.form.get("for_plan", "false").lower() == "true"
    
    # Only allow for_plan if the user is authenticated
    if not user_name:
        for_plan = False
    exercises = None
    # get distinct categories from the exercise collection
    categories = exercise_collection.distinct("categories")

    sub_category_equipment = []
    selected_equipment = None

    # check if the request is for adding a plan, default to be false
    for_plan = request.args.get("for_plan", "false").lower() == "true" or request.form.get("for_plan", "false").lower() == "true"

    # handle post request for filtering workouts
    if request.method == "POST":
        selected_category = request.form.get("category")
        selected_equipment = request.form.get("equipment")

        if selected_equipment:
            exercises = exercise_collection.find({
                "categories": selected_category
                , "equipment": selected_equipment
                })
        # filter exercise by category
        else:
            exercises = exercise_collection.find({"categories": selected_category})
        
        # get equipment list for the selected category
        exercises_for_equipment = exercise_collection.find({"categories": selected_category})
        equipment_set = {e.get("equipment") for e in exercises_for_equipment}
        sub_category_equipment = list(equipment_set) # cast it into list

    # handle the initial get request (no category selected yet)
    # display all exercises
    else:
        exercises = exercise_collection.find()
        selected_category = None

    workouts = [
        {
            "id": str(exercise["_id"]),
            "name": exercise["name"],
            "gif_path": exercise.get("gif_path", ""),
            "target_muscle": exercise.get("target_muscle", "")
        }
        for exercise in exercises
    ]

    return render_template("workout_instruction.html", categories=categories, workouts=workouts
    , selected_category=selected_category, sub_category_equipment=sub_category_equipment
    , selected_equipment=selected_equipment, for_plan=for_plan)

@app.route("/workout_instruction/exercise_details/<exercise_id>")
def exercise_details(exercise_id):
    try:
        # Fetch the exercise directly from the database
        exercise = exercise_collection.find_one({"_id": ObjectId(exercise_id)})
        if not exercise:
            abort(404, description="Exercise not found")

        # Prepare the exercise data to pass to the template
        exercise_data = {
            "id": str(exercise["_id"]),
            "name": exercise["name"],
            "gif_path": exercise.get("gif_path", ""),
            "target_muscle": exercise.get("target_muscle", ""),
            "secondaryMuscles": exercise.get("secondaryMuscles", []),
            "instructions": exercise.get("instructions", [])
        }

        return render_template("details.html", exercise=exercise_data)
    except Exception as e:
        abort(500, description=str(e))


@app.route("/add_workout_to_plan", methods=["POST"])
def add_workout_to_plan():
    # 'imyhalex' is for tempoary use,
    # this function creates a workout dictionary and append it into user's daily_workout_value
    workout = {
        "name": request.form.get("name")
        , "setNum": int(request.form.get("setNum"))
        , "gif_path": request.form.get("gif_path")
        , "target_muscle": request.form.get("target_muscle")
    }

    user_service.add_workout_plan("imyhalex", workout)
    return redirect(url_for("index"))

# serve as functionality to remove all exercise card decks in the index.html
@app.route("/clear_workout_plan", methods=["POST"])
def clear_workout_plan():
    user_service.clear_workout_plan("imyhalex") # tempoary user
    return redirect(url_for("index"))

# serve as functionality to delete on exercise card deck each time in index.html
@app.route("/delete_workout_plan", methods=["POST"])
def delete_workout_plan():
    exercise_name = request.form.get("name")

    # 'imyhalex' is for temporary use, replace it with the authenticated user's name
    user_service.delet_from_workout_plan("imyhalex", exercise_name)
    return redirect(url_for("index"))

# require user login - create decorator for other functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            return redirect(url_for('auth', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# render the weely report page
@app.route("/my_weekly_report", methods=["GET"])
@login_required
def show_my_weekly_report():
    return render_template("my_weekly_report.html")

food_collection = db["food"]

# marked - modified later
@app.route("/food_instruction", methods=["GET", "POST"])
def show_food_instruction():
    # Get distinct categories from the food collection
    categories = food_collection.distinct("category")

    selected_category = None
    foods = []

    if request.method == "POST":
        selected_category = request.form.get("category")
        if selected_category:
            # Fetch foods based on the selected category
            foods = food_collection.find({"category": selected_category})
    else:
        # Fetch all foods if no category is selected
        foods = food_collection.find()

    # Prepare the food data for rendering
    food_items = [{"id": str(food["_id"]), "name": food["food_name"]} for food in foods]

    return render_template(
        "food_instruction.html",
        categories=categories,
        foods=food_items,
        selected_category=selected_category,
    )

# marked - modified later
@app.route("/search_food", methods=["POST"])
def search_food():
    query = request.form.get("query", "")
    if query:
        foods = food_collection.find({"food_name": {"$regex": query, "$options": "i"}})
        food_items = [{"id": str(food["_id"]), "name": food["food_name"]} for food in foods]
        categories = food_collection.distinct("category")
        return render_template(
            "food_instruction.html",
            categories=categories,
            foods=food_items,
            search_query=query,
        )
    else:
        return redirect(url_for("show_food_instruction"))

"""some timer functionalities"""
# all 'imyhalex' here should be changed later when login-register authentication is implemented
@app.route("/start_timer/<workout_name>", methods=["POST"])
def start_timer(workout_name):
    duration_minutes = int(request.form.get("duration"))
    duration_seconds = duration_minutes * 60
    user_service.update_workout_timer("imyhalex", workout_name, duration_seconds, "running")
    return make_response("", 204) # 204 means no content response in http status code

@app.route("/stop_timer/<workout_name>", methods=["POST"])
def stop_timer(workout_name):
    user_service.update_workout_timer("imyhalex", workout_name, 0, "stopped")
    return make_response("", 204)

@app.route("/reset_timer/<workout_name>", methods=["POST"])
def reset_timer(workout_name):
    user_service.update_workout_timer("imyhalex", workout_name, 0, "stopped")
    return make_response("", 204)

"""-------------------------------------------------------------------------------------------------------------------"""
# this function is for temporary use
def seed_user():
    if not user_service.find_user("imyhalex"):
        user_service.register_user("imyhalex", "imyhalex")
        print("Temporary user 'imyhalex' seeded into the database.")

"""-------------------------------------End of the page render functions------------------------------------------------"""


"""-----------------------------------------API Endpoints--------------------------------------------------------------"""

# endpoint search exercise (workout instruction action) by name
@app.route("/api/exercises/search", methods=["GET", "POST"])
def search_exercise():
    if request.method == "POST":
        # request.args is used to access the query parameters
        query = request.form.get("query", "")

        # check if the request is for adding a plan, default to be false
        for_plan = request.args.get("for_plan", "false").lower() == "true" or request.form.get("for_plan", "false").lower() == "true"

        if query:
            all_exercises = list(exercise_collection.find())
            exercises = [exercise for exercise in all_exercises if fuzz.partial_ratio(query.lower(), exercise["name"].lower()) > 70]

            workouts = [
                {
                    "id": str(exercise["_id"]),
                    "name": exercise["name"],
                    "gif_path": exercise.get("gif_path", ""),
                    "target_muscle": exercise.get("target_muscle", "")
                } 
                for exercise in exercises
            ]

            # return the result list of dictionaries for use
            return render_template("workout_instruction.html", categories=exercise_collection.distinct("categories")
            , workouts=workouts, search_query=query, for_plan=for_plan)
    
    # return an empty form with all workouts
    return redirect(url_for("show_workout_instruction"))

# endpoint for exercise by category (on click categories side-bar)
@app.route("/api/exercises/category/<category>", methods=["GET"])
def get_exercise_by_category(category):
    exercises = exercise_collection.find({
        "categories": {"$regex": category}
        })

    # find() return cursor varible, it is iterable but can only be traced once, use list for multiple uses
    exercise_list = list(exercises)
    result = [{"id": str(e["_id"]), "name": e["name"]} for e in exercise_list]
    
    # get a unique list of equipment used for each category
    equipment_set = {e.get("equipment", "") for e in exercise_list}
    response = {
        "exercise": result
        , "sub_category_equipment": list(equipment_set)
    }
    return jsonify(response)

# endpoint for exercise by catgoery with subcategory in equipment (sub side-bar maybe)
@app.route("/api/exercises/category/<category>/equipment/<equipment>", methods=["GET"])
def get_exercises_by_category_and_equipment(category, equipment):
    exercise = exercise_collection.find({
        "categories": {"$regex": category}
        , "equipment": {"$regex": equipment}
        })
    result = [{"id": str(e["_id"]), "name": e["name"]} for e in exercises]
    return jsonify(result)

# endpoint for update flask to server timer data
@app.route("/api/timer_status/<workout_name>", methods=["GET"])
def get_timer_status(workout_name):
    user = user_service.find_user("imyhalex")  # Temporary user
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # get the specific workout details
    workout = next((w for w in user.get("daily_workout_plan", []) if w["name"] == workout_name), None)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify({"duration": workout["timer"]["duration"], "status": workout["timer"]["status"]})
    
# user register
@app.route('/api/user/register', methods=['POST'])
def register_api():
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")
    if not user_name or not password:
        return jsonify({"error": "Username and password are required"}), 400

    response, status_code = user_service.register_user(user_name, password)
    if status_code == 201:
        # Do not log the user in automatically
        # session['user_name'] = user_name  # Remove or comment out this line
        pass
    return jsonify(response), status_code


# user login
@app.route('/api/user/login', methods=['POST'])
def login_api():
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")
    if not user_name or not password:
        return jsonify({"error": "Username and password are required"}), 400

    response, status_code = user_service.login_user(user_name, password)
    if status_code == 200:
        session['user_name'] = user_name
    return jsonify(response), status_code
 
# update user height
@app.route("/api/user/<user_name>/update_height", methods=["PUT"])
def update_height(user_name):
    data = request.json
    height = data.get("height")
    if height is None:
        return jsonify({"error": "Height is required"}), 400

    user_service.update_user_height(user_name, height)
    return jsonify({"message": "User height updated successfully"}), 200

# update user data (weight, calorie intake)
@app.route("/api/user/<user_name>/update_data", methods=["PUT"])
def update_user_data(user_name):
    data = request.json
    date = data.get("date")
    weight = data.get("weight")
    calorie_intake = data.get("calorie_intake")
    if not data:
        return jsonify({"error": "Date is required"}), 400
    
    user_service.update_user_data(user_name, date, weight, calorie_intake)
    return jsonify({"message": "User data updated successfully"}), 200

# endpoint to add food intake for a user
@app.route("/api/user/<user_name>/add_food", methods=["POST"])
def add_food(user_name):
    data = request.json
    food_name = data.get("food_name")
    amount = data.get("amount")

    if not food_name or not amount:
        return jsonify({"error": "Food name and amount are required"}), 400

    response, status_code = nutrition_service.add_food_intake(user_name, food_name, amount)
    return jsonify(response), status_code


"""-----------------------------------------APScheduler--------------------------------------------------------------"""
# APScheduler to implement the countdown timer
def decrement_all_timers():
    user_service.decrement_timer()

# APScheduler to reset daily nutrition at midnight
def reset_daily_nutrition():
    nutrition_service.reset_daily_nutrition()

# APScheduler to reset daily values (weight and bmi)
def reset_daily_values():
    nutrition_service.reset_daily_nutrition()
    user_service.reset_body_values()

# function to reset the daily workout plan
def reset_daily_workout_plans():
    # iterate over all users in the database to clear the daily workout plan
    users = user_service.get_all_users()
    for user in users:
        user_service.clear_workout_plan(user["user_name"])

# initialize APScheduler background job object
scheduler = BackgroundScheduler()
# schedule the reset job to run at midnight every day
scheduler.add_job(reset_daily_values, 'cron', hour=0, minute=0)
scheduler.add_job(reset_daily_workout_plans, 'cron', hour=0, minute=0)
# this scheduler is the countdown scheduler for all users
scheduler.add_job(decrement_all_timers, IntervalTrigger(seconds=1))

# start the scheduler
scheduler.start()

if __name__ == "__main__":
    try:
        seed_user() # for tempoary use
        app.run(debug=True, use_reloader=False)  # set use_reloader=False to avoid starting the scheduler multiple times
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

