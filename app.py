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
        priority = request.form['priority']
        todos.insert_one({'content': content, 'priority': priority})
        return redirect(url_for('index'))

    return render_template('index.html')
