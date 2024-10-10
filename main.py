from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

#MongoDB connection
mongo_uri = "mongodb+srv://User:GoodEats@restaurantcluster.mny9a.mongodb.net/?retryWrites=true&w=majority&appName=RestaurantCluster"
client = MongoClient(mongo_uri)
db = client["RestaurantCluster"] 

#Home route
@app.route('/')
def home():
    restaurants=db.RestaurantCluster.find()
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
@app.route('/edit')
def edit():
    return render_template('edit.html')

#Search data route
@app.route('/search')
def search():
    return render_template('search.html')

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
    db.RestaurantCluster.insert_one(restaurantData)

    #change to a popup on screen
    return jsonify({'message': f"Restaurant '{request.form['restaurantName']}' submitted successfully!"}), 200

#Handle delete data form
@app.route('/deleteData', methods=['POST'])
def deleteData():
    userName = request.form['userName']
    restaurantName = request.form['restaurantName']
    cuisine = request.form['cuisine']
    deleteRestaurant = db.RecipeCluster.delete_one({'userName': userName, 'restaurantName': restaurantName, 'cuisine': cuisine})
    
    #change to a popup on screen
    if deleteRestaurant.deleted_count == 1: #if deleted ouput result to user
        return f"Restaurant '{restaurantName}' by '{userName}' deleted successfully!", 200
    else:
        return f"Restaurant '{restaurantName}' by '{userName}' not found / could not be deleted", 404

#run
if __name__ == '__main__':
    app.run(debug=True)
