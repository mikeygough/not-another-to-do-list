from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# get dbkey
load_dotenv()
db_key = os.getenv("DB_KEY").strip('"')

# create app
app = Flask(__name__)

# connect to db
client = MongoClient(db_key)

# get database and collection
db = client.flask_db
todos = db.todos

# routes:
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['priority']
        todos.insert_one({'content': content, 'priority': degree, 'complete': False})
        return redirect(url_for('index'))
    
    # sort by alphabetical english
    incomplete_todos = list(todos.find({"complete": False}).collation({'locale': 'en'}).sort('content'))
    complete_todos = list(todos.find({"complete": True}).collation({'locale': 'en'}).sort('content'))
    
    context = {"incomplete_todos": incomplete_todos, "complete_todos": complete_todos}
    return render_template('index.html', **context)

@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.post('/<id>/complete/')
def complete(id):
    filter = { '_id': ObjectId(id) }
    new_values = { '$set': { 'complete': True } }
    todos.update_one(filter, new_values)
    return redirect(url_for('index'))