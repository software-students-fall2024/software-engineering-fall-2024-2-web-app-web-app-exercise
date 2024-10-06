import os
from User import User
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, jsonify, render_template, request, redirect, abort, url_for, make_response

"""
Deafult root of the flask: templates

HTTP status code reference: https://docs.python.org/3/library/http.html
"""
load_dotenv()

app = Flask(__name__)

class Nutrition:
    pass

# mongodb connection - exercise_data
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["exercise_db"]
exercise_collection = db["exercise"]

# mongodb connection
user_service = User(db)

# index means home
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/workout_instruction")
def show_workout_instruction():
    return render_template("workout_instruction.html")

# endpoint search exercise (workout instruction action) by name
@app.route("/api/exercises/search", methods=["GET"])
def search_exercise():
    # request.args is used to access the query parameters
    query = request.args.get("query", "")

    if query:
        # perform a search in mongodb 'exercise' collection based on query
        # $option: 'i' to search name in case insensitive
        exercises = exercise_collection.find({
            "name": {"$regex": query, "$option": "i"}
            })
    
        result = [{"id": str(e["_id"]), "name": e["name"]} for e in exercises]
        return jsonify(result)
    
    return jsonify([]) # empty if no query

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
    return jsonify(result)

# endpoint for exercise by catgoery with subcategory in equipment (sub side-bar maybe)
@app.route("/api/exercises/category/<category>/equipment/<equipment>", methods=["GET"])
def get_exercises_by_category_and_equipment(category, equipment):
    exercise = exercise_collection.find({
        "categories": {"$regex": category}
        , "equipment": {"$regex": equipment}
        })
    result = [{"id": str(e["_id"]), "name": e["name"]} for e in exercises]
    return jsonify(result)

# endpoint to get exercise details by id, return coresponding details in json format if success, return error message with status code if failed
@app.route("/api/exercises/<exercise_id>", methods=["GET"])
def get_exercise_details(exercise_id):
    # https://flask.palletsprojects.com/en/3.0.x/errorhandling/  Returning API Errors as JSON (Returning API Errors as JSON)
    try:
        exercise = exercise_collection.find_one({"_id": ObjectId(exercise_id)})
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404
        
        result = {
            "id": str(exercise["_id"])
            , "name": exercise["name"]
            # , "categories": exercise.get("categories", "")
            # , "equipment": exercise.get("equipment", "")
            , "gif_path": exercise.get("gif_path", "")
            , "target_muscle": exercise.get("target_muscle", "")
            , "secondaryMuscles": exercise.get("secondaryMuscles", [])
            , "instructions": exercise.get("instructions", [])
        }
        return jsonify(result)
    except Exception as e:
        # catch whatever errors here, status is 500 - internal server error
        return jsonify({"error": str(e)}), 500

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

if __name__ == "__main__":
    app.run(debug=True)

