from flask import Flask, g
import sqlite3

DATABASE = '/path/to/database.db'

''' def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
   db = getattr(g, '_database', None)
    if db is not None:
        db.close() '''

app = Flask(__name__)

@app.route('/')
def index():
    return 'test'