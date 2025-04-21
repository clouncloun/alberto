import requests
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
API_KEY = "live_xID7zgqcyR7lDxE0qssvubFHqGX8kJ7w5BHevQNoUh2jpvOU19ORgKX0uJSM3nXQ"

COUNTER_FILE = 'cat_counter.txt'

def get_current_index():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def save_current_index(index):
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(index))

def fetch_cat_data(api_key, limit=25):
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        print('Error Fetching Cat Data')
        return []
    
def get_next_batch(data, current_index, batch_size=25):
    end_index = min(current_index + batch_size, len(data))
    batch = data[current_index:end_index]
    return batch, end_index

def setup_database():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "petfinder_pets.db")
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
    current_index = get_current_index()
    batch, new_index = get_next_batch(catlist, current_index)
    conn, cur = setup_database()
    inserted = insert_cat_data(batch, cur)
    conn.commit()
    if len(batch) == 25:
        save_current_index(new_index)
    else:
        save_current_index(0)
    conn.close()

if __name__ == "__main__":
    main()