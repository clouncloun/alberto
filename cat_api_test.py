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

cur.execute("""CREATE TABLE IF NOT EXISTS cat_trait1 (
    id INTEGER PRIMARY KEY, 
    cat_trait1 TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS cat_trait2 (
    id INTEGER PRIMARY KEY, 
    cat_trait2 TEXT UNIQUE
)""")

# database with individual cat info 
cur.execute("""
CREATE TABLE IF NOT EXISTS catinfo (
    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cat_breedname TEXT,
    cat_trait1_id INTEGER,
    cat_trait2_id INTEGER,
    cat_origin_id INTEGER,
    cat_lifespan_id INTEGER,
    cat_shedding_level INTEGER,
    cat_health_issues INTEGER,
    cat_intelligence INTEGER,
    FOREIGN KEY (cat_origin_id) REFERENCES cat_origins(id),
    FOREIGN KEY (cat_lifespan_id) REFERENCES cat_lifespans(id)
    FOREIGN KEY (cat_trait1_id) REFERENCES cat_trait1(id)
    FOREIGN KEY (cat_trait2_id) REFERENCES cat_trait2(id)


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
    cat_temp_split = cat_temperament.split(", ")
    if len(cat_temp_split) == 2:
        cat_trait1 = cat_temp_split[0]
        cat_trait2 = cat_temp_split[1]
    elif len(cat_temp_split) == 3:
        cat_trait1 = cat_temp_split[1]
        cat_trait2 = cat_temp_split[2]
    elif len(cat_temp_split) >= 4:
        cat_trait1 = cat_temp_split[2]
        cat_trait2 = cat_temp_split[3]
    cat_origin = cat['origin']
    cat_lifespan = cat['life_span']
    cat_shedding_level = cat.get('shedding_level', None)
    cat_health_issues = cat.get('health_issues', None)
    cat_intelligence = cat.get('intelligence', None)

    cat_trait1_id = insert_and_get_id('cat_trait1', 'cat_trait1', cat_trait1)
    cat_trait2_id = insert_and_get_id('cat_trait2', 'cat_trait2', cat_trait2)
    cat_origin_id = insert_and_get_id('cat_origins', 'cat_origin', cat_origin)
    cat_lifespan_id = insert_and_get_id('cat_lifespans', 'cat_lifespan', cat_lifespan)

    cur.execute("""
        INSERT OR IGNORE INTO catinfo 
        (cat_breedname, cat_trait1_id, cat_trait2_id, cat_origin_id, cat_lifespan_id, cat_shedding_level, cat_health_issues, cat_intelligence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (cat_breedname, cat_trait1_id, cat_trait2_id, cat_origin_id, cat_lifespan_id, cat_shedding_level, cat_health_issues, cat_intelligence)
    )

conn.commit()
conn.close()