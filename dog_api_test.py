import requests
from dotenv import load_dotenv
import os
import json
import sqlite3


API_KEY = "live_oadwgtqrmuVZflDBSxQeLM3WNpsySPYhMtQS7sDLrFlnMtMF8fVgHCyFY6wWCPrN"
load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.thedogapi.com/v1/breeds" 
headers = {"Authorization": f"Bearer {api_key}"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    doglist = []
    for dog in data:
        doglist.append(dog)

else:
    print(f"Error: {response.status_code}, Message: {response.text}")


# setting up database
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + "doginfo.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS doginfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    breedname TEXT,
    temperament TEXT,
    origin TEXT,
    life_span TEXT
)
""")



for dog in doglist:
    breedname = dog['name']
    temperament = dog['temperament']
    origin = dog['origin']
    life_span = dog['life_span']


    cur.execute("""
            INSERT OR IGNORE INTO doginfo
            (breedname, temperament, origin, lifespan)
            VALUES (?, ?, ?, ?)
            """, (breedname, temperament, origin, life_span))
    
conn.commit()