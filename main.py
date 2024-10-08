
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

#MongoDB connection
mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)
db = client["RecipeCluster"] 

#Home route
@app.route('/')
def index():
    return render_template('index.html')

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

#View all data route
@app.route('/view')
def view():
    return render_template('view.html')

#Handle add data form
@app.route('/addData', methods=['POST'])
def addData():
    recipeData = {
        'username': request.form['authorName'],
        'recipeTitle': request.form['recipeTitle'],
        'servings': request.form['servings'],
        'time': request.form['time'],
        'ingredients': request.form['ingredients'],
        'instructions': request.form['instructions']
    }
    #add recipe data to db
    db.RecipeCluster.insert_one(recipeData)

    #For testing/debugging purposes
    return f"Recipe '{recipeTitle}' submitted successfully!", 200

#Handle delete data form
@app.route('/deleteData', methods=['POST'])
def deleteData():
    username = request.form['authorName']
    recipeTitle = request.form['recipeTitle']
    return f"Recipe '{recipeTitle}' deleted successfully!", 200

if __name__ == '__main__':
    app.run(debug=True)
