# database implementation
import os
import pymongo
from dotenv import load_dotenv

# load environment variables from .env file (this is not included in version control)
load_dotenv()

# fetch the MONGO_URI from environmental variables
mongo_uri = os.getenv("MONGO_URI")

# initialized mongodb client with fetched uri
myclient = pymongo.MongoClient(mongo_uri)

# access the 'exercise_db' database
exercise_db = myclient["exercise_db"]

print(myclient.list_database_names())