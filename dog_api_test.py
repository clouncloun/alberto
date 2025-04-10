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
    bred_for TEXT,
    life_span TEXT
)
""")

#print(doglist)

for dog in doglist:
    breedname = dog['name']
    temperament = dog.get('temperament', 'Unknown')  
    bred_for = dog.get('bred_for', 'Unknown')
    life_span = dog.get('life_span', 'Unknown')

    cur.execute("""
            INSERT OR IGNORE INTO doginfo
            (breedname, temperament, bred_for, life_span)
            VALUES (?, ?, ?, ?)
            """, (breedname, temperament, bred_for, life_span))
    
conn.commit()