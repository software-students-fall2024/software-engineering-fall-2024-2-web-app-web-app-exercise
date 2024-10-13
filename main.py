import os
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId

load_dotenv()

def create_app():
    app = Flask(__name__)

    cxn = pymongo.MongoClient(os.getenv('MONGO_URI'))
    MONGO_URI = os.getenv('MONGO_URI')
    db = cxn[os.getenv('MONGO_DBNAME')]
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB")
    except Exception as e:
        print("MongoDB connection error:", e)

    #Home route
    @app.route('/')
    def home():
        restaurants=db.MONGO_DBNAME.find().sort('restaurantName')
        restaurant_list = list(restaurants)
        return render_template('index.html', restaurants=restaurant_list)

    #Add data route
    @app.route('/add')
    def add():
        return render_template('add.html')

    #Delete data route
    @app.route('/delete')
    def delete():
        return render_template('delete.html')

    #Edit data route
    @app.route("/edit/<post_id>")
    def edit(post_id):
        restaurant=db.MONGO_DBNAME.find_one({"_id": ObjectId(post_id)})
        return render_template('edit.html', restaurant=restaurant)

    #Search data route
    @app.route('/search', methods=['GET'])
    def search():
        query = {}
        nameSearch = request.args.get('resName')
        cuisineSearch = request.args.get('resCuisine')
        userSearch = request.args.get('resUser')
        if nameSearch or cuisineSearch or userSearch:
            if nameSearch:
                query['restaurantName'] = {'$regex': nameSearch, '$options': 'i'}
            if cuisineSearch:
                query['cuisine'] = {'$regex': cuisineSearch, '$options': 'i'}
            if userSearch:
                query['userName'] = {'$regex': userSearch, '$options': 'i'} 
            restaurants = db.RestaurantCluser.find(query)
            restaurantList = list(restaurants)
        else:
            restaurantList = []
        return render_template('search.html', restaurants=restaurantList)

    #Handle add data form
    @app.route('/addData', methods=['POST'])
    def addData():
        restaurantData = {
            'userName': request.form['userName'],
            'restaurantName': request.form['restaurantName'],
            'cuisine': request.form['cuisine'],
            'location': request.form['location'],
            'review': request.form['review']
        }

        #Add recipe data to db
        db.MONGO_DBNAME.insert_one(restaurantData)

        #change to a popup on screen
        return jsonify({'message': f"Restaurant '{request.form['restaurantName']}' submitted successfully!"}), 200

    #Handle delete data form
    @app.route('/deleteData', methods=['POST'])
    def deleteData():
        userName = request.form['userName']
        restaurantName = request.form['restaurantName']
        cuisine = request.form['cuisine']
        deleteRestaurant = db.MONGO_DBNAME.delete_one({'userName': userName, 'restaurantName': restaurantName, 'cuisine': cuisine})
        
        #change to a popup on screen
        if deleteRestaurant.deleted_count == 1: #if deleted ouput result to user
            return f"Restaurant '{restaurantName}' by '{userName}' deleted successfully!", 200
        else:
            return f"Restaurant '{restaurantName}' by '{userName}' not found / could not be deleted", 404
    
    app.debug = True
    return app

#run
if __name__ == '__main__':
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)