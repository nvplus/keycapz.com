from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
from src import kkz_db, keyset

"""
Meta stuff
"""
app = Flask(__name__)

@app.before_request
def before_request():
    g.db = kkz_db.get_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

"""
Routes
"""
@app.route('/')
def index():
    all_sets = kkz_db.get_all_keysets()
    return render_template('index.html', keysets = all_sets)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add', methods=['POST'])
def add():
    db = kkz_db.get_db()

    kkz_db.add_keyset(request.form['k_name'], request.form['k_img_url'], request.form['k_website_link'], request.form['k_start_date'], request.form['k_end_date'])

    return redirect(url_for('admin'))