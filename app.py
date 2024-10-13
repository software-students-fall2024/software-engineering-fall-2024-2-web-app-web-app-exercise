from dotenv import load_dotenv
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
import os
from pymongo.mongo_client import MongoClient

load_dotenv()

def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """
    
    app = Flask(__name__)
    
    db_uri = os.getenv("DB_URI")
    # Create a new client and connect to the server
    client = MongoClient(db_uri)
    db = client['bookstore']
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("MongoDB connection error:", e)
        
    @app.route("/search")
    def search():
        """
        Search function to filter books based on title, author, genre, or date added.
        """
        query = {}
        
        #Get the query parameters from the request's query string
        title = request.args.get('title')
        author = request.args.get('author')
        genre = request.args.get('genre')
        date_added = request.args.get('date_added')
        
        #Build the query
        #Search for containment and case-insensitive
        if title:
            query['title'] = {'$regex': title, '$options':'i'}
        if author:
            query['author'] = {'$regex': author, '$options':'i'}
        if genre:
            query['genre'] = {'$regex': genre, '$options':'i'}
        if date_added:
            try:
                date_obj = datetime.datetime.strptime(date_added, "%Y-%m-%d")
                query['date_added'] = date_obj
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD.", 400
        
        # Perform the search on the books collection
        results = db.books.find(query) if query else []
        
        #Render the search results
        return render_template('search.html', books=results)
    
    @app.route("/delete/<book_id>", methods=["POST"])
    def delete(book_id):
        """
        Route for POST requests to the delete page.
        Deletes the specified book from the database, and then redirects the browser to the home page.
        Args:
            book_id (str): The ID of the book to delete.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        db.books.delete_one({"_id": ObjectId(book_id)})
        return redirect(url_for("home"))
    
    return app
            
    


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)