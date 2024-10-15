
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


# Homepage route
@app.route('/index/<username>')
def index(username):
    # Check whether the user is logged in
    if session.get('username') != username:
        return redirect(url_for('login'))
    
    # Fetch budget data from the 'budgets' collection
    budget_data = db['budgets'].find_one({'username': username})

    if budget_data is None:
        return redirect(url_for('account'))

    # Set the budget and spending budget values
    name = budget_data.get('name', 'User')
    total_budget = budget_data.get('total_budget', 0)
    spending_budget = budget_data.get('spending_budget', 0)

    # Fetch all transactions for the logged-in user
    transactions = list(transactions_collection.find({'username': username}))

    # Calculate total income and total expenses
    total_income = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'income')
    total_expenses = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'expense')

    # Corrected calculations:
    # Balance should be total_budget (initial budget) + income - expenses
    balance = total_budget + total_income - total_expenses

    # Spending Budget Left should be spending_budget - expenses
    budget_left = spending_budget - total_expenses

    # Update the remaining budget in the database
    db['budgets'].update_one(
        {'username': username},  # Ensure to update the current user's budget
        {'$set': {'budget_left': budget_left}}
    )

    return render_template(
        'index.html', 
        transactions=transactions, 
        balance=balance,  # total budget + income - expenses
        spending_budget=spending_budget,  # User-specified spending budget
        budget_left=budget_left,  # Remaining spending budget after expenses
        name=name,
        username=username
    )


# View all transactions
@app.route('/transactions')
def view_transactions():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Fetch transactions for the current user only
    transactions = list(transactions_collection.find({'username': username}))
    
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
            'username': username,
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
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Fetch transactions for the logged-in user only
    transactions = list(transactions_collection.find({'username': username}))  # Filter by username
 
    if request.method == 'POST':
        selected_transaction_id = request.form['transaction_id']

        if selected_transaction_id:
            # Redirect to the edit page using the selected transaction ID
            return redirect(url_for('edit_transaction', transaction_id=selected_transaction_id))

    return render_template('search_edit.html', transactions=transactions)


@app.route('/edit_transaction/<transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Fetch the transaction for the logged-in user only
    transaction = transactions_collection.find_one({'_id': ObjectId(transaction_id), 'username': username})  # Ensure the transaction belongs to the user

    if not transaction:
        return "Transaction not found or you don't have permission to edit this transaction", 404
 

    if request.method == 'POST':
        # Get updated form data
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['type']
        date = request.form['date']

        # Update transaction in MongoDB
        transactions_collection.update_one(
            {'_id': ObjectId(transaction_id),'username': username},  
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
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Ensure the transaction belongs to the logged-in user
    transactions_collection.delete_one({'_id': ObjectId(transaction_id), 'username': username})  # Delete only the user's transaction
    return redirect(url_for('view_transactions'))

# Search route for transactions
@app.route('/search_transactions', methods=['GET', 'POST'])
def search_transactions():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']

        results = transactions_collection.find({
            'username': username,
            '$or': [
                {'category': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        })
        return render_template('search.html', results=results)

    return render_template('search.html')

#log out page
@app.route('/logout')
def logout():
    # clear session
    session.clear()
    #go to login
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
