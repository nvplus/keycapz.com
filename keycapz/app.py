from flask import Flask, g, render_template, request, redirect, url_for, jsonify
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
Temp Frontend Routes
"""
@app.route('/')
def index():
    return render_template('index.html', keysets = kkz_db.get_all_keysets())

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin-add', methods=['POST'])
def admin_add():
    kkz_db.add_keyset(request.form['k_name'], request.form['k_img_url'], request.form['k_website_link'], request.form['k_start_date'], request.form['k_end_date'])

    return redirect(url_for('admin'))

"""
HTTP Endpoints
"""
@app.route('/get-all', methods=["GET"])
def show_all():
    return jsonify(kkz_db.get_all_keysets())

@app.route('/search', methods=["GET"])
def search():
    return jsonify(kkz_db.search(request.json['k_name']))

@app.route('/add-set', methods=["POST"])
def add_set():
    """
    Accepts POST requests in the following format:
    "k_name": "Name",
	"k_img_url": "Image URL",
	"k_start_date": "YYYY-MM-DD",
	"k_end_date":"YYYY-MM-DD",
	"k_website_link": "url"
    """

    kkz_db.add_keyset(request)
    return 'Keyset added:\n' + str(request.json)