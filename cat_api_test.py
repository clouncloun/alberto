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

cur.execute("""
CREATE TABLE IF NOT EXISTS catinfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    breedname TEXT,
    temperament TEXT,
    origin TEXT,
    lifespan TEXT,
    shedding_level TEXT,
    health_issues TEXT,
    intelligence TEXT
)
""")



for cat in catlist:
    breedname = cat['name']
    temperament = cat['temperament']
    origin = cat['origin']
    lifespan = cat['life_span']
    shedding_level = cat['shedding_level']
    health_issues = cat['health_issues']
    intelligence = cat['intelligence']

    cur.execute("""
            INSERT OR IGNORE INTO catinfo
            (breedname, temperament, origin, lifespan, shedding_level, health_issues, intelligence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (breedname, temperament, origin, lifespan, shedding_level, health_issues, intelligence))
    
conn.commit()