
from flask import Flask, render_template, request, redirect, url_for, flash, session
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
app.secret_key = os.getenv('SECRET_KEY')
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['SWE_Project_2-Webstars']
transactions_collection = db['transactions']
users_collection = db['users']


# Homepage route
@app.route('/account', methods=['GET', 'POST'])
def account():
    # Render the account creation page if it's a GET request
    if request.method == 'GET':
        return render_template('account.html')
    # Handle form submission here when it's a POST request
    return redirect(url_for('save_account'))

# Login route
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")

        user = users_collection.find_one({'username': username})

        if user:
            if (user['password']==password):
                session['username'] = username
                return redirect(url_for('index', username=username))
        else:
             flash('Incorrect Username or Password', 'danger')

    return render_template('login.html')

# Save account route from Create an account 
@app.route('/save_account', methods=['POST'])
def save_account():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    total_budget = float(request.form['total_budget'])
    spending_budget = float(request.form['spending_budget'])

    # Save the username, name, total budget, and spending budget to the 'budgets' collection
    existing_user = users_collection.find_one({'username': username, 'password': password})
    if existing_user is None:
        new_user = {'name': name, 'username': username, 'password': password}
        users_collection.insert_one(new_user)

        # Insert user's budget
        db['budgets'].insert_one({
            'username': username,
            'name': name,
            'total_budget': total_budget,
            'spending_budget': spending_budget,
            'budget_left': total_budget
        })

        return redirect(url_for('index',username=username))
    else: 
        flash("Username already exists.")
    return redirect(url_for('login'))
    
@app.route('/')
def home():
    # Redirect to login if no session exists
    if 'username' not in session:
        # No session exists, redirect to account creation page
        return redirect(url_for('account'))
    else:
        # If logged in, redirect to the user's homepage
        return redirect(url_for('index', username=session['username']))


@app.route('/index/<username>')
def index(username):
    # Debugging statement
    print(f"Session Username: {session.get('username')}, URL Username: {username}")

    # Check whether the user is logged in
    if session.get('username') != username:
        print("User is not logged in or session username doesn't match.")
        return redirect(url_for('login'))
    
    # Fetch budget data from the 'budgets' collection
    budget_data = db['budgets'].find_one({'username': username})

    if budget_data is None:
        print("No budget data found, redirecting to account setup.")
        return redirect(url_for('account'))

    # Fetch transactions for the logged-in user
    transactions = list(transactions_collection.find({'username': username}))

    # Debugging statements for transactions
    print(f"Transactions for {username}: {transactions}")

    # Calculate balance and remaining budget
    total_expenses = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'expense')
    balance = budget_data.get('total_budget', 0) - total_expenses
    budget_left = budget_data.get('spending_budget', 0) - total_expenses

    # Debugging statements for balance and budget
    print(f"Balance: {balance}, Budget Left: {budget_left}")

    # Update the remaining budget in the database
    db['budgets'].update_one({'username': username}, {'$set': {'budget_left': budget_left}})

    # Pass the data to the template
    return render_template(
        'index.html', 
        transactions=transactions, 
        balance=balance,  
        spending_budget=budget_data.get('spending_budget', 0),  
        budget_left=budget_left,  
        name=budget_data.get('name', 'User'),
        username=username  # Pass the username to the template
    )


# View all transactions
@app.route('/transactions')
def view_transactions():
    transactions = list(transactions_collection.find())  # Convert cursor to list
    return render_template('transactions.html', transactions=transactions)

# Add transaction route
@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
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
