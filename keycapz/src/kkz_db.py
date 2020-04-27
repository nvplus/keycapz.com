from flask import g
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
        print("Database connection successful")
        return conn

    except Exception as e:
        print("Could not connect to the databse. Error: ", e)
        return None


def do_query(query:str, args = (), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def insert(query: str):
    cur = g.db.execute(query)
    g.db.commit()

def add_keyset(name:str, img_url:str, website_link:str, start_date:str, end_date:str):
    q =  'INSERT INTO kkz_keysets (name, image_url, start_date, end_date, website_url) VALUES("{}", "{}", "{}", "{}", "{}");'.format(name, img_url, start_date, end_date, website_link)
    print(q)
    insert(q)

def get_all_keysets():
    return do_query("SELECT * FROM kkz_keysets")