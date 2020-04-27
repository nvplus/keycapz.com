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


def _do_query(query:str, args = (), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def _do_query_commit(query: str, args = ()):
    cur = g.db.execute(query, args)
    g.db.commit()

def add_keyset(name:str, img_url:str, website_link:str, start_date:str, end_date:str):
    args = name, img_url, start_date, end_date, website_link
    q =  'INSERT INTO kkz_keysets (name, image_url, start_date, end_date, website_url) VALUES("%s", "%s", "%s", "%s", "%s");'
    _do_query_commit(q, args)
    
def add_keyset(request):
    r = request.json
    args = r.get('k_name'), r.get('k_img_url'), r.get('k_start_date'), r.get('k_end_date'), r.get('k_website_link')
    q =  'INSERT INTO kkz_keysets (name, image_url, start_date, end_date, website_url) VALUES("%s", "%s", "%s", "%s", "%s");'
    _do_query_commit(q)

def get_all_keysets():
    return _do_query("SELECT * FROM kkz_keysets ORDER BY end_date DESC")

def search_keyset_by_name(term):
    return _do_query("SELECT * FROM kkz_keysets WHERE name LIKE %s", term)

def delete_keyset_by_id(id):
    q = 'DELETE FROM kkz_keysets WHERE id={}'.format(id)
    return _do_query_commit(q)