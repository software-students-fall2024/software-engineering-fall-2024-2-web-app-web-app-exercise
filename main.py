
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/addData', methods=['POST'])
def addData():
    username = request.form['username']
    password = request.form['password']
    recipeTitle = request.form['recipeTitle']
    servings = request.form['servings']
    time = request.form['time']
    ingredients = request.form['ingredients']
    instructions = request.form['instructions']
    return request.form
    #return f"Recipe '{recipeTitle}' submitted successfully!", 200

@app.route('/deleteData', methods=['POST'])
def deleteData():
    username = request.form['username']
    password = request.form['password']
    recipeTitle = request.form['recipeTitle']
    return f"Recipe '{recipeTitle}' deleted successfully!", 200

if __name__ == '__main__':
    app.run(debug=True)
