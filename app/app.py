from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from connection import *
from store_data import get_store_location
from get_transactions import get_transactions
from add_transaction import add_transaction
from get_transaction_to_edit import get_transaction_to_edit
from edit_transaction import edit_transaction
from delete_transaction import delete_transaction

# Home Screen (Select location) 
# Store information Screen
# List of Transaction Screen (For selected location)    -read.html
# Add Transaction Screen (CREATE transaction)   -create.html
# Edit Transaction Screen (UPDATE transaction)  -edit.html
# Delete Transaction Screen (DELETE transaction)  - delete.html

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location/<store_location>')
def location(store_location):
    store_data = get_store_data(store_location)
    store_data['total_revenue'] = "{:,.2f}".format(store_data['total_revenue'])
    
    return render_template('location.html',store_location=store_location, **store_data)

@app.route('/transactions/<store_location>')
def transactions(store_location):
    transaction_data =  get_transaction_data(store_location)
    return render_template('transaction.html', store_location=store_location, transaction_data=transaction_data['transactions'])

#get
@app.route('/get_store_data/<store_location>')
def get_store_data(store_location):
    return get_store_location(store_location)

#get
@app.route('/get_transactions/<store_location>')
def get_transaction_data(store_location): 
    return get_transactions(store_location)

#post
@app.route('/add/<item_name>/<int:quantity>/<float:price>/<store_location>/<gender>/<int:age>/<email>/<coupon_used>/<purchase_method>')
def add(item_name, quantity, price, store_location, gender, age, email, coupon_used, purchase_method): 
    add_transaction(item_name, quantity, price, store_location, gender, age, email, coupon_used, purchase_method)

#get
@app.route('/get_to_edit/<email>')
def get_to_edit(email):
    return get_transaction_to_edit(email)
    
#post
@app.route('/edit/<email>/<purchase_method>')   
def edit(email, purchase_method):
    edit_transaction(email, purchase_method)

#post
@app.route('/delete/<email>')
def delete(email):
    delete_transaction(email)


if __name__ == '__main__':
    app.run(debug=True)