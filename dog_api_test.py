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


# id tables setup
cur.execute("""CREATE TABLE IF NOT EXISTS bred_for (
    id INTEGER PRIMARY KEY, 
    bred_for TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS lifespans (
    id INTEGER PRIMARY KEY, 
    dog_lifespan TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS temperament1 (
    id INTEGER PRIMARY KEY, 
    temperament1 TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS temperament2 (
    id INTEGER PRIMARY KEY, 
    temperament2 TEXT UNIQUE
)""")

cur.execute("""
CREATE TABLE IF NOT EXISTS doginfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_breedname TEXT,
    temperament1_id INTEGER,
    temperament2_id INTEGER,
    bred_for_id INTEGER,
    dog_lifespan_id INTEGER,
    FOREIGN KEY (temperament1_id) REFERENCES temperament1(id),
    FOREIGN KEY (temperament2_id) REFERENCES temperament2(id),
    FOREIGN KEY (bred_for) REFERENCES dog_bred_for(id),
    FOREIGN KEY (lifespan) REFERENCES lifespans(id)
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
