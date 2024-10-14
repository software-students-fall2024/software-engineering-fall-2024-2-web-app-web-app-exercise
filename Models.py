import os
import requests
from datetime import datetime

"""
for any mongodb operators, this is the reference:
    https://www.mongodb.com/docs/manual/reference/operator

for datetime.timedelta reference, please check in here:
    https://docs.python.org/3/library/datetime.html#timedelta-objects
"""

class User:
    def __init__(self, db):
        self.__collection = db['usr']
    
    def register_user(self, user_name, password):
        if self.__collection.find_one({"user_name": user_name}):
            return {"error": "User already exists."}, 409
        
        new_user = {
            "user_name": user_name
            , "password": password
            , "height": None
            , "weekly_values": [
                {
                    "weekly_weight": [0] * 7
                    , "weekly_calorie": [0] * 7
                    , "weekly_bmi": [0] * 7   
                    , "weekly_protein": [0] * 7
                    , "weekly_carbs": [0] * 7
                    , "weekly_fats": [0] * 7
                    , "weekly_sugar": [0] * 7              
                }
            ]
            , "daily_workout_plan": []
        }

        self.__collection.insert_one(new_user)
        return {"message": "User registered successfully"}, 201

    def login_user(self, user_name, password):
        user = self.__collection.find_one({"user_name": user_name, "password": password})
        if not user:
            return {"error": "Invalid username or password"}, 401
        return {"message": "User logged in successfully"}, 200
    
    def find_user(self, user_name):
        return self.__collection.find_one({"user_name": user_name})
    
    def get_all_users(self):
        return self.__collection.find()
    
    def update_user_height(self, user_name, height):
        self.__collection.update_one(
            {"user_name": user_name}
            , {"$set": {"height": height}}
            , upsert=True
        )
    
    def update_user_data(self, user_name, date, weight=None, calorie_intake=None):
        current_day_index = datetime.now().weekday()

        update_fields = {}
        if weight is not None:
            update_fields[f"weekly_values.0.weekly_weight.{current_day_index}"] = weight
        
        if calorie_intake is not None:
            update_fields[f"weekly_values.0.weekly_calorie.{current_day_index}"] = calorie_intake
        
        self.__collection.update_one(
            {"user_name": user_name}
            , {"$set": update_fields}
            , upsert=True
        )

    # only accept imperial units (feet, inches, pounds)
    def calculate_bmi(self, user_name, weight_pounds, height_feet, height_inches):
        user = self.find_user(user_name)
        
        if weight_pounds is not None and (height_feet is not None or height_inches is not None):
            # Convert height to meters
            total_height_inches = height_feet * 12 + height_inches
            height_m = total_height_inches * 0.0254

            # Convert weight to kg
            weight_kg = weight_pounds * 0.453592

            # Calculate BMI
            if height_m > 0:
                bmi = round(weight_kg / (height_m ** 2), 2)
                current_day_index = datetime.now().weekday()
                
                # Update user's weekly BMI in the database
                self.__collection.update_one(
                    {"user_name": user_name}
                    , {"$set": {f"weekly_values.0.weekly_bmi.{current_day_index}": bmi}}
                )
                return bmi

        return None

    def reset_body_values(self):
        current_day_index = datetime.now().weekday()
        update_fields = {
            f"weekly_values.0.weekly_calorie.{current_day_index}": None,
            f"weekly_values.0.weekly_weight.{current_day_index}": None,
            f"weekly_values.0.weekly_bmi.{current_day_index}": None
        }
        self.__collection.update_many({}, {"$set": update_fields})

    # document for $addToSet: https://www.mongodb.com/docs/manual/reference/operator/update/addToSet/
    def add_workout_plan(self, user_name, workout):
        """
        add a default timer field to each workout item
        workout["timer"] = {
            "duration": 0               # in seconds
            , "status": "stopped"       # could be 'stopped', 'running', 'completed'
        }
        """
        workout["timer"] = {
            "duration": 0              
            , "status": "stopped"
        }

        self.__collection.update_one(
            {"user_name": user_name}
            , {"$addToSet": {"daily_workout_plan": workout}}
            , upsert=True
        )
    
    # update timer details for a workout in the user's plan
    def update_workout_timer(self, user_name, workout_name, duration_seconds, status):
        self.__collection.update_one(
            {"user_name": user_name, "daily_workout_plan.name": workout_name},
            {"$set": {
                "daily_workout_plan.$.timer.duration": duration_seconds,
                "daily_workout_plan.$.timer.status": status
            }}
        )
    
    # implementation of the countdown logic here - this method will be called every single second
    def decrement_timer(self):
        users = self.__collection.find({})
        # iterates through all users in the databse
        for user in users:
            # access theirs daily_workout_plan
            for workout in user.get("daily_workout_plan", []):
                # decrement timer duration by 1 second if two conditions are satisfied
                if workout.get("timer", {}).get("status") == "running" and workout["timer"]["duration"] > 0:
                    new_duration = workout["timer"]["duration"] - 1
                    # if duration reach 0, set status to 'completed'
                    if new_duration <= 0:
                        status = "completed"
                        new_duration = 0
                    else:
                        status = "running"
                    
                    self.__collection.update_one(
                        {"user_name": user["user_name"], "daily_workout_plan.name": workout["name"]}
                        , {"$set": {
                            "daily_workout_plan.$.timer.duration": new_duration
                            , "daily_workout_plan.$.timer.status": status
                        }}
                    )
    
    def get_workout_plan(self, user_name):
        user = self.find_user(user_name)
        if user and "daily_workout_plan" in user:
            return user["daily_workout_plan"]
        return []
    
    # let user to specifiy one exercise to delete from the his/her personal data
    def delet_from_workout_plan(self, user_name, exercise_name):
        self.__collection.update_one(
            {"user_name": user_name}
            , {"$pull": {"daily_workout_plan": {"name": exercise_name}}}
        )

    # this is the method to let user to clear all his today's exercise data, or automatically clear this data when 00:00 (a new day beigns)
    def clear_workout_plan(self, user_name):
        self.__collection.update_one(
            {"user_name": user_name}
            , {"$set": {"daily_workout_plan": []}} # set it back to empty list (remove all)
        )
    

class Nutrition:
    def __init__(self, db):
        self.__collection = db['usr']
        self.__food_collection = db['food']
        self.__daily_calorie = 0
        self.__daily_protein = 0
        self.__daily_carbs = 0
        self.__daily_fats = 0
    
    def fetch_nutrition_info(self, query):
        api_key = os.getenv("API_NINJAS_KEY")
        api_url = f"https://api.api-ninjas.com/v1/nutrition?query={query}"
        headers = {'X-Api-Key': api_key}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def add_food_intake(self, user_name, food_name, amount):
        # fetch food into from 'food' collection
        food = self.__food_collection.find_one({"food_name": food_name})
        if not food:
            return {"error": "Food not found in database"}, 404

        nutrition_info = self.fetch_nutrition_info(f"{amount}g {food['query_name']}")
        if not nutrition_info:
            return {"error": "Unable to fetch nutrition info"}, 500

        # Update daily values in user's profile
        user = self.__collection.find_one({"user_name": user_name})
        current_day_index = datetime.now().weekday()

        # Get current values, if None, default to 0
        weekly_values = user.get("weekly_values", [{}])[0]
        current_calories = weekly_values.get("weekly_calorie", [0] * 7)[current_day_index] or 0
        current_protein = weekly_values.get("weekly_protein", [0] * 7)[current_day_index] or 0
        current_carbs = weekly_values.get("weekly_carbs", [0] * 7)[current_day_index] or 0
        current_fats = weekly_values.get("weekly_fats", [0] * 7)[current_day_index] or 0
        current_sugar = weekly_values.get("weekly_sugar", [0] * 7)[current_day_index] or 0

        # Update fields with new values
        update_fields = {
            f"weekly_values.0.weekly_calorie.{current_day_index}": current_calories + nutrition_info[0].get("calories", 0),
            f"weekly_values.0.weekly_protein.{current_day_index}": current_protein + nutrition_info[0].get("protein_g", 0),
            f"weekly_values.0.weekly_carbs.{current_day_index}": current_carbs + nutrition_info[0].get("carbohydrates_total_g", 0),
            f"weekly_values.0.weekly_fats.{current_day_index}": current_fats + nutrition_info[0].get("fat_total_g", 0),
            f"weekly_values.0.weekly_sugar.{current_day_index}": current_sugar + nutrition_info[0].get("sugar_g", 0)
        }

        # Update in the database
        self.__collection.update_one({"user_name": user_name}, {"$set": update_fields}, upsert=True)
        return {"message": "Food intake updated successfully"}, 200

    def reset_daily_nutrition(self):
        self.__daily_calorie = 0
        self.__daily_protein = 0
        self.__daily_carbs = 0
        self.__daily_fats = 0
    
    def get_my_calorie(self):
        return self.__daily_calorie
    
    def get_my_protien(self):
        return self.__daily_protein
    
    def get_my_carbs(self):
        return self.__daily_carbs
    
    def get_my_fats(self):
        return self.__daily_fats
        
    def get_food_collection(self):
        return self.__food_collection