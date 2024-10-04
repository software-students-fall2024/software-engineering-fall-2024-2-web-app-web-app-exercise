# Database seeding and updating script with ObjectId handling
import os
import json
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError, PyMongoError


def load_environment_variables():
    # load environment variables from .env file (this is not included in version control)
    load_dotenv()

    # fetch the MONGO_URI from environmental variables
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in environment variables. Please check your .env file.")
    return mongo_uri


def connect_to_mongodb(mongo_uri):
    try:
        client = pymongo.MongoClient(mongo_uri)
        print("Successfully connected to MongoDB.")
        return client
    except ServerSelectionTimeoutError as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

def load_json_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"file not found at path: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON data should be a list of exercise objects.")
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            raise

def create_unique_index(collection, field_name):
    try:
        collection.create_index(field_name, unique=True)
        print(f"Unique index created on field '{field_name}'.")
    except PyMongoError as e:
        print(f"Error creating unique index on field '{field_name}': {e}")
        raise

def seed_database(collection, exercises):
    try:
        collection.insert_many(exercises, ordered=False)
        print(f"Inserted {len(exercises)} exercises into the database.")
    except DuplicateKeyError as e:
        print(f"Duplicate key error during seeding: {e.details}")
    except PyMongoError as e:
        print(f"An error occurred during seeding: {e}")
        raise

def update_database(collection, exercises):
    upsert_count = 0
    for exercise in exercises:
        try:
            result = collection.update_one(
                {"id": exercise["id"]},     # Filter by unique 'id'
                {"$set": exercise},         # Update the document with exercise data
                upsert=True                 # Insert if not exists
            )
            if result.upserted_id:
                upsert_count += 1
        except PyMongoError as e:
            print(f"Error upserting exercise with id {exercise.get('id', 'N/A')}: {e}")
    print(f"Upserted {upsert_count} new exercises.")


def main():
    """Main function to seed or update the MongoDB database."""
    try:
        # Load environment variables
        mongo_uri = load_environment_variables()

        # Connect to MongoDB
        client = connect_to_mongodb(mongo_uri)

        # Access the database and collection
        exercise_db = client["exercise_db"]
        exercise_collection = exercise_db["exercise"]

        # Create a unique index on 'id' to prevent duplicates
        create_unique_index(exercise_collection, "id")

        # Load exercise data from JSON
        json_file_path = os.path.join(os.path.dirname(__file__), "../exercise_data.json")
        exercises = load_json_data(json_file_path)

        # Check if the collection is empty: https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.count_documents
        count = exercise_collection.count_documents({})
        if count == 0:
            print("Exercise collection is empty. Seeding the database...")
            seed_database(exercise_collection, exercises)
        else:
            print("Exercise collection already has data. Updating existing entries...")
            update_database(exercise_collection, exercises)

        print("Database operation completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the MongoDB connection
        try:
            client.close()
            print("MongoDB connection closed.")
        except:
            pass

if __name__ == "__main__":
    main()