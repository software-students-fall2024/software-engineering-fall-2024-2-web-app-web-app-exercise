import os
import requests
from datetime import datetime

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
            , "weely_values": [
                {
                    "weekly_weight": [None] * 7
                    , "weekly_calorie": [None] * 7
                    , "weekly_bmi": [None] * 7                    
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

    # only accept metrics units (cm, m, g, kg etc)
    def cacluate_bmi(self, user_name, weight):
        user = self.find_user(user_name)
        height = user.get("height")

        if height and weight:
            height_m = height / 100
            bmi = round(weight / (height_m ** 2), 2)
            current_day_index = datetime.now().weekday()
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
    
    def add_workout_plan(self, user_name, workout):
        self.__collection.update_one(
            {"user_name": user_name}
            , {"$push": {"daily_workout_plan": workout}}
            , upsert=True
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

        query_name = food.get("query_name")    
        # fetch food nutrtion info
        nutrition_info = self.fetch_nutrition_info(f"{amount} {query_name}")
        if not nutrition_info:
            return {"error": "Unable to fetch nutrition info"}, 500
        
        for n in nutrition_info:
            self.__daily_calorie += n.get("calories", 0)
            self.__daily_protein += n.get("protein_g", 0)
            self.__daily_carbs += n.get("carbohydrates_total_g", 0)
            self.__daily_fats += n.get("fat_total_g", 0)
        
        # update the user's weekly calorie data in the databse
        current_day_index = datetime.now().weekday()
        self.__collection.update_one(
            {"user_name": user_name}
            , {"$set": {f"weekly_values.0.weekly_calorie.{current_day_index}": self.__daily_calorie}}
            , upsert=True
        )

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
