from flask import Flask
import sqlite3
from flask import g

app = Flask(__name__)

@app.route('/')
def index():
    return 'test'