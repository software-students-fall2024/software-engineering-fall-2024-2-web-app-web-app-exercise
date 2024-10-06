from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

# Initialize Flask application
app = Flask(__name__)

 
client = MongoClient('mongodb://localhost:27017/')
db = client['bankingSystem']
transactions_collection = db['transactions']
 



# homepage router
@app.route('/')
def home():
    
    budget = 5000   
    budget_left = 3000  
    return render_template('home.html', budget=budget, budget_left=budget_left)

# show transaction page
@app.route('/transactions')
def view_transactions():
    # get all transaction record
    transactions = transactions_collection.find()
    return render_template('transactions.html', transactions=transactions)

# the router for adding transactions
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        # get  data
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['type']
        date = request.form['date']

        # insert data into MongoDB
        transactions_collection.insert_one({
            'amount': float(amount),
            'category': category,
            'description': description,
            'type': transaction_type,
            'date': datetime.datetime.strptime(date, '%Y-%m-%d')
        })

        # re-direction to transaction page
        return redirect(url_for('view_transactions'))

    return render_template('add.html')

# router for edit 
@app.route('/edit/<transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['type']
        date = request.form['date']

        # update
        transactions_collection.update_one(
            {'_id': ObjectId(transaction_id)},
            {'$set': {
                'amount': float(amount),
                'category': category,
                'description': description,
                'type': transaction_type,
                'date': datetime.datetime.strptime(date, '%Y-%m-%d')
            }}
        )

        # redirction
        return redirect(url_for('view_transactions'))


    transaction = transactions_collection.find_one({'_id': ObjectId(transaction_id)})
    return render_template('edit.html', transaction=transaction)

# delete transaction 
@app.route('/delete/<transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    # delete record from datbase
    transactions_collection.delete_one({'_id': ObjectId(transaction_id)})
    return redirect(url_for('view_transactions'))

# search router
@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        query = request.form['query']
        
        results = transactions_collection.find({
            '$or': [
                {'category': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        })
        return render_template('search.html', results=results)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)