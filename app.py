import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from Models import User, Nutrition
from bson.objectid import ObjectId
from fuzzywuzzy import fuzz
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, render_template, request, redirect, abort, url_for, make_response, send_from_directory

"""
Deafult root of the flask: templates

HTTP status code reference: https://docs.python.org/3/library/http.html
APScheduler reference: https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/background.html#module-apscheduler.schedulers.background
"""
load_dotenv()

app = Flask(__name__)

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
    return render_template("index.html")

@app.route("/workout_instruction", methods=["GET", "POST"])
def show_workout_instruction():
    exercises = None
    # get distinct categories from the exercise collection
    categories = exercise_collection.distinct("categories")

    sub_category_equipment = []
    selected_equipment = None

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
    , selected_category=selected_category, sub_category_equipment=sub_category_equipment, selected_equipment=selected_equipment)

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

@app.route("/my_weekly_report", methods=["GET"])
def show_my_weekly_report():
    return render_template("my_weekly_report.html")

class Plan:
    def __init__(self, name, setNum, gif_path, target_muscle):
        self.name = name
        self.setNum = setNum
        self.gif_path = gif_path
        self.target_muscle = target_muscle

    def __str__(self):
        return f"Plan(name='{self.name}', setNum={self.setNum}, gif_path='{self.gif_path}', target_muscle='{self.target_muscle}')"
    def to_dict(self):
        return {
            'name': self.name,
            'setNum': self.setNum,
            'gif_path': self.gif_path,
            'target_muscle': self.target_muscle}

def output_plans():
    if not selected_plans:
        print("No plans selected yet.")
    else:
        for plan in selected_plans:
            print(plan)

selected_plans = []

@app.route("/workout_plan", methods=['GET', 'POST'])
def show_workout_plan():
    return render_template("workout_plan.html", plans=selected_plans)

@app.route("/workout_plan/select", methods=['GET','POST'])
def show_workout_plan_select():
    exercises = None
    # get distinct categories from the exercise collection
    categories = exercise_collection.distinct("categories")

    sub_category_equipment = []
    selected_equipment = None

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

    return render_template("workout_plan_select.html", categories=categories, workouts=workouts
    , selected_category=selected_category, sub_category_equipment=sub_category_equipment, selected_equipment=selected_equipment)

@app.route("/add_workout_to_plan", methods=["POST"])
def add_workout_to_plan():
    name = request.form.get("name")
    setNum = int(request.form.get("setNum"))
    gif_path = request.form.get("gif_path")
    target_muscle = request.form.get("target_muscle")
    new_plan = Plan(name, setNum, gif_path, target_muscle)
    selected_plans.append(new_plan.to_dict())


    return redirect(url_for("show_workout_plan"))



@app.route("/delete_exercise_from_plan", methods=["POST"])
def delete_exercise_from_plan():
    data = request.get_json()
    exercise_name = data.get('exerciseName')

    # Remove the exercise from selected_plans
    global selected_plans
    selected_plans = [plan for plan in selected_plans if plan.name != exercise_name]

    return jsonify({'success': True})

food_collection = db["food"]

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

"""-----------------------------------------API Endpoints--------------------------------------------------------------"""

# endpoint search exercise (workout instruction action) by name
@app.route("/api/exercises/search", methods=["GET", "POST"])
def search_exercise():
    if request.method == "POST":
        # request.args is used to access the query parameters
        query = request.form.get("query", "")

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
            , workouts=workouts, search_query=query)
    
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
    
# user register
@app.route("/api/user/register", methods=["POST"])
def register():
    data = request.json
    user_name = data.get("user_name")
    password = data.get("password")
    if not user_name or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    response, status_code = user_service.register_user(user_name, password)
    return jsonify(response), status_code

# user login
@app.route("/api/user/login", methods=["POST"])
def login():
    data = request.json
    user_name = data.get("user_name")
    password = data.get("password")
    if not user_name or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    response, status_code = user_service.login_user(user_name, password)
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

# APScheduler to reset daily nutrition at midnight
def reset_daily_nutrition():
    nutrition_service.reset_daily_nutrition()

# APScheduler to reset daily values (weight and bmi)
def reset_daily_values():
    nutrition_service.reset_daily_nutrition()
    user_service.reset_body_values()

scheduler = BackgroundScheduler()
# Schedule the reset job to run at midnight every day
scheduler.add_job(reset_daily_values, 'cron', hour=0, minute=0)
scheduler.start()

if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)  # set use_reloader=False to avoid starting the scheduler multiple times
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

