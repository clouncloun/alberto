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
cur.execute("""CREATE TABLE IF NOT EXISTS origins (
    id INTEGER PRIMARY KEY, 
    origin TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS lifespans (
    id INTEGER PRIMARY KEY, 
    lifespan TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS trait1 (
    id INTEGER PRIMARY KEY, 
    trait1 TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS trait2 (
    id INTEGER PRIMARY KEY, 
    trait2 TEXT UNIQUE
)""")

# database with individual cat info 
cur.execute("""
CREATE TABLE IF NOT EXISTS catinfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    breedname TEXT,
    trait1_id INTEGER,
    trait2_id INTEGER,
    origin_id INTEGER,
    lifespan_id INTEGER,
    shedding_level INTEGER,
    health_issues INTEGER,
    intelligence INTEGER,
    FOREIGN KEY (origin_id) REFERENCES origins(id),
    FOREIGN KEY (lifespan_id) REFERENCES lifespans(id)
    FOREIGN KEY (trait1_id) REFERENCES trait1(id)
    FOREIGN KEY (trait2_id) REFERENCES trait2(id)


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
    temp_split = temperament.split(", ")
    if len(temp_split) == 2:
        trait1 = temp_split[0]
        trait2 = temp_split[1]
    elif len(temp_split) == 3:
        trait1 = temp_split[1]
        trait2 = temp_split[2]
    elif len(temp_split) >= 4:
        trait1 = temp_split[2]
        trait2 = temp_split[3]
    origin = cat['origin']
    lifespan = cat['life_span']
    shedding_level = cat.get('shedding_level', None)
    health_issues = cat.get('health_issues', None)
    intelligence = cat.get('intelligence', None)

    trait1_id = insert_and_get_id('trait1', 'trait1', trait1)
    trait2_id = insert_and_get_id('trait2', 'trait2', trait2)
    origin_id = insert_and_get_id('origins', 'origin', origin)
    lifespan_id = insert_and_get_id('lifespans', 'lifespan', lifespan)

    cur.execute("""
        INSERT OR IGNORE INTO catinfo 
        (breedname, trait1_id, trait2_id, origin_id, lifespan_id, shedding_level, health_issues, intelligence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (breedname, trait1_id, trait2_id, origin_id, lifespan_id, shedding_level, health_issues, intelligence)
    )

conn.commit()
conn.close()