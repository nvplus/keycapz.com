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

@app.route('/admin-add', methods=["POST"])
def admin_add():
    kkz_db.add_keyset(request.form['k_name'], request.form['k_img_url'], request.form['k_website_link'], request.form['k_start_date'], request.form['k_end_date'])

    return redirect(url_for('admin'))

"""
HTTP Endpoints
"""

# Create methods
@app.route('/keysets/add/', methods=["POST"])
def add_set():
    """
    Accepts POST requests in the following format:
    "k_name": "Name",
	"k_img_url": "Image URL",
	"k_start_date": "YYYY-MM-DD",
	"k_end_date":"YYYY-MM-DD",
	"k_website_link": "url"
    """

    result = kkz_db.add_keyset(request)
    return jsonify(result) if result else "Could not add the keyset."

# Retrieve methods
@app.route('/keysets/', methods=["GET"])
def keysets():
    result = kkz_db.get_all_keysets() 
    return jsonify(result) if result != None else "no keysounds found"

@app.route('/keysets/<int:keyset_id>', methods=["GET"])
def get_keyset(keyset_id):
    result = kkz_db.get_keyset(keyset_id)
    return result if result != None else "No keyset found with id {}".format(keyset_id) 

@app.route('/search', methods=["GET"])
def search():   
    return jsonify(kkz_db.search(request.json['k_name']))

# Update methods -- Todo: Make these not doodoo
@app.route('/keysets/update/<int:keyset_id>/name/<string:name>', methods=["PUT"])
def update_name(name):
    pass

@app.route('/keysets/update/<int:keyset_id>/img/<string:image>', methods=["PUT"])
def update_img(image):
    pass

@app.route('/keysets/update/<int:keyset_id>/start/<string:start>', methods=["PUT"])
def update_start_date(start):
    pass

@app.route('/keysets/update/<int:keyset_id>/end/<string:end>', methods=["PUT"])
def update_end_date(end):
    pass

@app.route('/keysets/update/<int:keyset_id>/website/<string:website>', methods=["PUT"])
def update_website_link(website):
    pass

# Delete methods
@app.route('/keysets/delete/<int:keyset_id>', methods=["DELETE"])
def delete(keyset_id):
    deleted = kkz_db.delete(keyset_id)
    return "Successfully deleted keyset with id {}".format(keyset_id) if deleted else "could not delete keyset with id {}".format(keyset_id)