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

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    catlist = []
    for cat in data:
        catlist.append(cat)

else:
    print(f"Error: {response.status_code}, Message: {response.text}")


# setting up database
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + "catinfo.db")
cur = conn.cursor()


# id tables setup
cur.execute("""CREATE TABLE IF NOT EXISTS breeds (
    id INTEGER PRIMARY KEY, 
    breed TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS origins (
    id INTEGER PRIMARY KEY, 
    origin TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS lifespans (
    id INTEGER PRIMARY KEY, 
    lifespan TEXT UNIQUE
)""")

# database with individual cat info 
cur.execute("""
CREATE TABLE IF NOT EXISTS catinfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    breed_id INTEGER,
    temperament TEXT,
    origin_id INTEGER,
    lifespan_id INTEGER,
    shedding_level INTEGER,
    health_issues INTEGER,
    intelligence INTEGER,
    FOREIGN KEY (breed_id) REFERENCES breeds(id),
    FOREIGN KEY (origin_id) REFERENCES origins(id),
    FOREIGN KEY (lifespan_id) REFERENCES lifespans(id)
)
""")

#print(catlist)

# putting data in the id tables
def insert_and_get_id(table, column, value):
    cur.execute(f"INSERT OR IGNORE INTO {table} ({column}) VALUES (?)", (value,))
    cur.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    return cur.fetchone()[0]

for cat in catlist:
    breedname = cat['name']
    temperament = cat.get('temperament', None)
    origin = cat['origin']
    lifespan = cat['life_span']
    shedding_level = cat.get('shedding_level', None)
    health_issues = cat.get('health_issues', None)
    intelligence = cat.get('intelligence', None)

    breed_id = insert_and_get_id('breeds', 'breed', breedname)
    origin_id = insert_and_get_id('origins', 'origin', origin)
    lifespan_id = insert_and_get_id('lifespans', 'lifespan', lifespan)

    cur.execute("""
        INSERT OR IGNORE INTO catinfo 
        (breed_id, temperament, origin_id, lifespan_id, shedding_level, health_issues, intelligence)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (breed_id, temperament, origin_id, lifespan_id, shedding_level, health_issues, intelligence)
    )

conn.commit()
conn.close()