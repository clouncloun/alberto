import requests
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch_cat_data(api_key, limit=25):
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"Authorization": f"Bearer {api_key}"}
    catlist = []
    page = 0

    while True:
        params = {"limit": limit, "page": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, Message: {response.text}")
            break

        data = response.json()
        if not data:
            break

        catlist.extend(data)
        page += 1

    return catlist

def setup_database():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "petfinder_test.db")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cat_origins (
        id INTEGER PRIMARY KEY, 
        cat_origin TEXT UNIQUE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS cat_lifespans (
        id INTEGER PRIMARY KEY, 
        cat_lifespan TEXT UNIQUE
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS catinfo (
        cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cat_breedname TEXT,
        cat_temperament TEXT,
        cat_origin_id INTEGER,
        cat_lifespan_id INTEGER,
        cat_shedding_level INTEGER,
        cat_health_issues INTEGER,
        cat_child_friendly INTEGER,
        cat_intelligence INTEGER,
        FOREIGN KEY (cat_origin_id) REFERENCES cat_origins(id),
        FOREIGN KEY (cat_lifespan_id) REFERENCES cat_lifespans(id)
    )""")

    return conn, cur

def insert_and_get_id(cur, table, column, value):
    cur.execute(f"INSERT OR IGNORE INTO {table} ({column}) VALUES (?)", (value,))
    cur.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    return cur.fetchone()[0]

def insert_cat_data(catlist, cur):
    for cat in catlist:
        cat_breedname = cat.get('name')
        cat_temperament = cat.get('temperament')
        cat_origin = cat.get('origin')
        cat_lifespan = cat.get('life_span')
        cat_shedding_level = cat.get('shedding_level')
        cat_health_issues = cat.get('health_issues')
        cat_child_friendly = cat.get('child_friendly')
        cat_intelligence = cat.get('intelligence')

        cat_origin_id = insert_and_get_id(cur, 'cat_origins', 'cat_origin', cat_origin)
        cat_lifespan_id = insert_and_get_id(cur, 'cat_lifespans', 'cat_lifespan', cat_lifespan)

        cur.execute("""
            INSERT OR IGNORE INTO catinfo 
            (cat_breedname, cat_temperament, cat_origin_id, cat_lifespan_id, cat_shedding_level, 
            cat_health_issues, cat_child_friendly, cat_intelligence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (cat_breedname, cat_temperament, cat_origin_id, cat_lifespan_id,
             cat_shedding_level, cat_health_issues, cat_child_friendly, cat_intelligence)
        )

def main():
    catlist = fetch_cat_data(API_KEY)
    conn, cur = setup_database()
    insert_cat_data(catlist, cur)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()