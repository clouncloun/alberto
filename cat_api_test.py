import requests
from dotenv import load_dotenv
import os
import json
import sqlite3


API_KEY = "live_xID7zgqcyR7lDxE0qssvubFHqGX8kJ7w5BHevQNoUh2jpvOU19ORgKX0uJSM3nXQ"
load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.thecatapi.com/v1/breeds" 
headers = {"Authorization": f"Bearer {api_key}"}

catlist = []
page = 0

while True:
    params = {
        "limit": 25,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Message: {response.text}")
        break

    data = response.json()

    # Stop the loop if there's no more data
    if not data:
        break

    catlist.extend(data)
    page += 1

# setting up database
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + "petfinder_pets.db")
cur = conn.cursor()


# id tables setup
cur.execute("""CREATE TABLE IF NOT EXISTS cat_origins (
    id INTEGER PRIMARY KEY, 
    cat_origin TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS cat_lifespans (
    id INTEGER PRIMARY KEY, 
    cat_lifespan TEXT UNIQUE
)""")

# database with individual cat info 
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
)
""")

#print(catlist)

# putting data in the id tables
def insert_and_get_id(table, column, value):
    cur.execute(f"INSERT OR IGNORE INTO {table} ({column}) VALUES (?)", (value,))
    cur.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    return cur.fetchone()[0]

for cat in catlist:
    cat_breedname = cat['name']
    cat_temperament = cat.get('temperament', None)
    cat_origin = cat['origin']
    cat_lifespan = cat['life_span']
    cat_shedding_level = cat.get('shedding_level', None)
    cat_health_issues = cat.get('health_issues', None)
    cat_child_friendly = cat.get('child_friendly', None)
    cat_intelligence = cat.get('intelligence', None)
    cat_origin_id = insert_and_get_id('cat_origins', 'cat_origin', cat_origin)
    cat_lifespan_id = insert_and_get_id('cat_lifespans', 'cat_lifespan', cat_lifespan)

    cur.execute("""
        INSERT OR IGNORE INTO catinfo 
        (cat_breedname, cat_temperament, cat_origin_id, cat_lifespan_id, cat_shedding_level, cat_health_issues, cat_child_friendly, cat_intelligence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (cat_breedname, cat_temperament, cat_origin_id, cat_lifespan_id, cat_shedding_level, cat_health_issues, cat_child_friendly, cat_intelligence)
    )

conn.commit()
conn.close()