from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
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
    store_data = get_store_location(store_location)
    store_data['total_revenue'] = "{:,.2f}".format(store_data['total_revenue'])
    return render_template('location.html',store_location=store_location, **store_data)

@app.route('/transactions/<store_location>')
def transactions(store_location):
    transaction_data =  get_transactions(store_location)
    return render_template('read.html', store_location=store_location, transaction_data=transaction_data['transactions'])

@app.route('/add_transaction_page/<store_location>')
def add_transaction_page(store_location):
    return render_template('create2.html', store_location=store_location)

@app.route('/submit/<store_location>', methods=['POST'])
def submit_form(store_location):
    form_data = {
        'item_name': request.form.get('item_name'),
        'quantity': int(request.form.get('quantity')),
        'price': float(Decimal128(request.form.get('price')).to_decimal()),
        'store_location': store_location,
        'gender': request.form.get('gender'),
        'age': int(request.form.get('age')),
        'email': request.form.get('email'),
        'coupon_used': request.form.get('coupon_used'),
        'purchase_method': request.form.get('purchase_method')
    }
    add_transaction(**form_data)
    return form_data

@app.route('/edit/<store_location>')
def edit_page(store_location):
    return render_template('edit.html', store_location=store_location)

@app.route('/get_to_edit')
def get_to_edit():
    email = request.args.get('customer_email')
    print(email)
    purchase_method = request.args.get('purchase_method')
    print(purchase_method)
    if get_transaction_to_edit(email) != "Transaction not found.":
        edit_transaction(email, purchase_method)
        ## Where will this go?
    return get_transaction_to_edit(email)

@app.route('/delete')
def delete_page():
    return render_template('delete.html')

@app.route('/delete_transaction', methods=['POST'])
def delete():
    email = request.form.get('customer_email')
    if email:
        try: 
            delete_transaction(email)
            return f"Transaction for {email} deleted successfully.", 200
        except:
            return f"No transaction found for {email}.", 404
    return "Email is required.", 400


# GET
# @app.route('/get_store_data/<store_location>')
# def get_store_data(store_location):
#     return get_store_location(store_location)

# GET
# @app.route('/get_transactions/<store_location>')
# def get_transaction_data(store_location): 
#     return get_transactions(store_location)

# POST
# @app.route('/add/<item_name>/<int:quantity>/<float:price>/<store_location>/<gender>/<int:age>/<email>/<coupon_used>/<purchase_method>')
# def add(item_name, quantity, price, store_location, gender, age, email, coupon_used, purchase_method): 
#     add_transaction(item_name, quantity, price, store_location, gender, age, email, coupon_used, purchase_method)

# GET
# @app.route('/get_to_edit/<email>')
# def get_to_edit(email):
#     return get_transaction_to_edit(email)
    
# POST
# @app.route('/edit/<email>/<purchase_method>')   
# def edit(email, purchase_method):
#     edit_transaction(email, purchase_method)

# POST
# @app.route('/delete/<email>')
# def delete(email):
#     delete_transaction(email)

if __name__ == '__main__':
    app.run(debug=True)