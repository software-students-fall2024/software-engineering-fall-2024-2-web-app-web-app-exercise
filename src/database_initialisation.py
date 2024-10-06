import pymongo
import os
import json


def database_add(db, collection_name, file_name):
    print("testing")
    if os.path.exists(file_name):
        collection = db[collection_name]
        print("collection created")
        with open(file_name, 'r') as file:
            data = json.load(file)
            print("file read")

        if not isinstance(data, list):
            data = [data]
            print("data converted")

        for item in data:
            print("adding item to db")
            collection.update_one({'_id': item['_id']}, {
                '$set': item}, upsert=True)

    else:
        print("file doesn't exist")
