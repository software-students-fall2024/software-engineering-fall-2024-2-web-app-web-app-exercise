import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")


client = MongoClient(mongo_uri)
db = client["exercise_db"]
food_collection = db["food"]


def seed_food_data(file_path):
    with open(file_path, "r") as food_file:
        foods = []
        update_operations = []
        
        for f in food_file:
            food_name, category, query_name = f.strip().split(",")
            food_name = food_name.strip()
            category = category.strip()
            query_name = query_name.strip()

            food_data = {
                "food_name": food_name
                , "category": category
                , "query_name": query_name
            }

            # check if the food item exits
            existing_food = food_collection.find_one({"food_name": food_name})

            if existing_food:
                update_operations.append(
                    UpdateOne(
                        {"food_name": food_name}
                        , {"$set": food_data}
                        , upsert=True
                    )
                )
            else:
                foods.append(food_data)
        
        if foods:
            food_collection.insert_many(foods)
            print(f"Inserted {len(foods)} foods items into the databse")
        
        if update_operations:
            food_collection.bulk_write(update_operations)
            print(f"Updated {len(update_operations)} food items in the database.")

if __name__ == "__main__":
    seed_food_data("food_data.txt")
