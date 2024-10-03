# database implementation
import pymongo
from dotenv import load_dotenv

load_dotenv()

myclient = pymongo.MongoClient("MONGO_URI")

exercise_db = myclient["exercise_db"]

print(myclient.list_database_names())