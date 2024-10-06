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
            , "height": None,
            , "weely_values": [
                {
                    "weekly_weight": [None] * 7,
                    "weekly_calorie": [None] * 7,
                    "weekly_bmi": [None] * 7                    
                }
            ]
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
