from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Replace this with your actual Cosmos DB connection string
cosmos_db_uri = "mongodb+srv://Fatima:Niklo137138.@mycluster0101.mongocluster.cosmos.azure.com/?authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000&appName=mongosh+1.10.1"
database_name = "BookStore"

# Connect to Cosmos DB
client = MongoClient(cosmos_db_uri)
db = client[database_name]
collection = db["BookStore"]

@app.route('/')
def index():
    # Read all records from the collection
    books = collection.find({})
    return render_template('index.html', books=books)

@app.route('/book_detail/<id>')
def book_detail(id):
    # Retrieve a single book by its ObjectId
    book = collection.find_one({"_id": ObjectId(id)})
    return render_template('book_detail.html', book=book)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        author = request.form.get('author')
        pages = int(request.form.get('pages'))

        # Insert new record into the collection
        new_book = {"title": title, "author": author, "pages": pages}
        collection.insert_one(new_book)

        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/edit_book/<id>', methods=['GET', 'POST'])
def edit_book(id):
    book = collection.find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        author = request.form.get('author')
        pages = int(request.form.get('pages'))

        # Update record in the collection
        collection.update_one({"_id": ObjectId(id)}, {"$set": {"title": title, "author": author, "pages": pages}})

        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<id>', methods=['POST'])
def delete_book(id):
    # Delete record from the collection
    collection.delete_one({"_id": ObjectId(id)})

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
