
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
# Initialize Flask application
app = Flask(__name__)

''' MongoDB Remote Server connection
client = MongoClient('mongodb://localhost:27017/')
db = client['bankingSystem']
transactions_collection = db['transactions']'''

# client = MongoClient('mongodb://localhost:27017/')
# db = client['bankingSystem']
# transactions_collection = db['transactions']

# MongoDB Atlas connection 
# client = MongoClient('mongodb+srv://nsb8225:<webstars>@cluster0.i1yb0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
# db = client['SWE_Project_2-Webstars']
# transactions_collection = db['transactions']

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['SWE_Project_2-Webstars']
transactions_collection = db['transactions']

# Homepage route
@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html')


@app.route('/save_account', methods=['POST'])
def save_account():
    name = request.form['name']
    total_budget = float(request.form['total_budget'])
    spending_budget = float(request.form['spending_budget'])

    # Save the name, total budget, and spending budget to the 'budgets' collection
    db['budgets'].update_one(
        {}, 
        {'$set': {'name': name, 'total_budget': total_budget, 'spending_budget': spending_budget, 'budget_left': total_budget}},
        upsert=True
    )

    return redirect(url_for('home'))


# Homepage route
@app.route('/')
def index():
    # Fetch budget data from the 'budgets' collection
    budget_data = db['budgets'].find_one()

    if not budget_data:
        return redirect(url_for('account'))

    # Set the budget and spending budget values
    name = budget_data.get('name', 'User')
    total_budget = budget_data.get('total_budget', 0)
    spending_budget = budget_data.get('spending_budget', 0)

    # Fetch all transactions and calculate total expenses
    transactions = list(transactions_collection.find())  # Convert cursor to list
    total_expenses = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'expense')

    # Corrected calculations:
    # Balance should be total_budget minus expenses
    balance = total_budget - total_expenses

    # Spending Budget Left should be spending_budget minus expenses
    budget_left = spending_budget - total_expenses

    # Update the remaining budget in the database
    db['budgets'].update_one(
        {}, 
        {'$set': {'budget_left': budget_left}}
    )

    return render_template(
        'index.html', 
        transactions=transactions, 
        balance=balance,  # total budget - expenses
        spending_budget=spending_budget,  # user gives - stays constant
        budget_left=budget_left,  # spending budget minus expenses
        name=name
    )

# View all transactions
@app.route('/transactions')
def view_transactions():
    transactions = list(transactions_collection.find())  # Convert cursor to list
    return render_template('transactions.html', transactions=transactions)

# Add transaction route
@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        # Get form data
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['type']
        date = request.form['date']

        # Insert transaction into MongoDB
        transactions_collection.insert_one({
            'amount': float(amount),
            'category': category,
            'description': description,
            'type': transaction_type,
            'date': datetime.datetime.strptime(date, '%Y-%m-%d')
        })

        # Redirect to transactions page
        return redirect(url_for('view_transactions'))

    return render_template('add.html')
@app.route('/edit_transaction', methods=['GET', 'POST'])
def search_and_edit_transaction():
    # Fetch all transactions for the dropdown menu
    transactions = list(transactions_collection.find())

    if request.method == 'POST':
        selected_transaction_id = request.form['transaction_id']

        if selected_transaction_id:
            # Redirect to the edit page using the selected transaction ID
            return redirect(url_for('edit_transaction', transaction_id=selected_transaction_id))

    return render_template('search_edit.html', transactions=transactions)


@app.route('/edit_transaction/<transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    transaction = transactions_collection.find_one({'_id': ObjectId(transaction_id)})

    if not transaction:
        return "Transaction not found", 404

    if request.method == 'POST':
        # Get updated form data
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['type']
        date = request.form['date']

        # Update transaction in MongoDB
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

        return redirect(url_for('view_transactions'))

    return render_template('edit.html', transaction=transaction)


# Delete transaction route
@app.route('/delete/<transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    transactions_collection.delete_one({'_id': ObjectId(transaction_id)})
    return redirect(url_for('view_transactions'))

# Search route for transactions
@app.route('/search_transactions', methods=['GET', 'POST'])
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



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
