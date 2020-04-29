from flask import g, request
import sqlite3
from .keyset import keyset

DB_PATH = "./db/keycapz.db"

def get_db():
    """
    Connects to the database specified in DB_PATH. Returns an sqlite3 connection object.\n
    Usage:\n
        db = get_db()
        cursor = db.cursor()
        cursor.execute("some query, like SELECT * FROM SOMETABLE")
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn

    except Exception as e:
        print("Could not connect to the databse. Error: ", e)
        return None

"""
Private methods
"""
def _do_query(query:str, args = (), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def _do_query_commit(query: str, args = ()):
    cur = g.db.execute(query, args)
    g.db.commit()

"""
Public methods for REST API
"""
def add_keyset(name:str, img_url:str, website_link:str, start_date:str, end_date:str):
    q =  'INSERT INTO kkz_keysets (name, image_url, start_date, end_date, website_url) VALUES(?, ?, ?, ?, ?);'
    
    try:
        args = (name, img_url, start_date, end_date, website_link)
        _do_query_commit(q, args)

        return _do_query('SELECT last_insert_rowid() FROM kkz_keysets')
    except Exception as e:
        return "Could not insert set: {}".format(e)
    
def add_keyset(request):
    r = request.json
    q =  'INSERT INTO kkz_keysets (name, image_url, start_date, end_date, website_url) VALUES(?, ?, ?, ?, ?);'

    try:
        args = (r.get('k_name'), r.get('k_img_url'), r.get('k_start_date'), r.get('k_end_date'), r.get('k_website_link'))
        _do_query_commit(q, args)

        return _do_query('SELECT * FROM kkz_keysets ORDER BY id DESC')
    except Exception as e:
        return False

def get_all_keysets():
    return _do_query("SELECT * FROM kkz_keysets ORDER BY end_date DESC")

def get_keyset(keyset_id):
    q = "SELECT * FROM kkz_keysets WHERE id = ?"
    return  _do_query(q, (keyset_id,), True)
    
def search_by_name(term):
    return _do_query("SELECT * FROM kkz_keysets WHERE name LIKE '?'", (term,))

def delete(id):
    keyset_exists = get_keyset(id)
    q = 'DELETE FROM kkz_keysets WHERE id = ?'

    if keyset_exists:
        _do_query_commit(q, (id,))
        return keyset_exists != get_keyset(id)

    return False