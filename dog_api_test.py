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
conn = sqlite3.connect(path + "/" + "petfinder_pets.db")
cur = conn.cursor()


#cur.execute("""DROP TABLE lifespans""")

# id tables setup
cur.execute("""CREATE TABLE IF NOT EXISTS dog_bred_for (
    id INTEGER PRIMARY KEY, 
    dog_bred_for TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS dog_lifespans (
    id INTEGER PRIMARY KEY, 
    dog_lifespan TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS dog_temperament1 (
    id INTEGER PRIMARY KEY, 
    dog_temperament1 TEXT UNIQUE
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS dog_temperament2 (
    id INTEGER PRIMARY KEY, 
    dog_temperament2 TEXT UNIQUE
)""")

cur.execute("""
CREATE TABLE IF NOT EXISTS doginfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_breedname TEXT,
    dog_temperament1_id INTEGER DEFAULT 0,
    dog_temperament2_id INTEGER DEFAULT 0,
    dog_bred_for_id INTEGER DEFAULT 0,
    dog_lifespan_id INTEGER DEFAULT 0,
    FOREIGN KEY (dog_temperament1_id) REFERENCES dog_temperament1(id),
    FOREIGN KEY (dog_temperament2_id) REFERENCES dog_temperament2(id),
    FOREIGN KEY (dog_bred_for_id) REFERENCES dog_bred_for(id),
    FOREIGN KEY (dog_lifespan_id) REFERENCES dog_lifespans(id)
)
""")
# for dog in doglist:
#     print(dog)

# putting data in the id tables
# and ensure None values are replaced with 0 before inserting into the database
def insert_and_get_id(table, column, value):
    if value is None:
        return 0
    cur.execute(f"INSERT OR IGNORE INTO {table} ({column}) VALUES (?)", (value,))
    cur.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    result = cur.fetchone()
    return result[0] if result else 0

for dog in doglist:
    dog_breedname = dog['name']
    dog_temperament = dog.get('temperament', None)
    #print(dog_temperament)

    dog_temperament1 = None
    dog_temperament2 = None

    if dog_temperament is not None:
        dog_temp_split = dog_temperament.split(', ')
        if len(dog_temp_split) == 2:
            dog_temperament1 = dog_temp_split[0]
            dog_temperament2 = dog_temp_split[1]
        elif len(dog_temp_split) == 3:
            dog_temperament1 = dog_temp_split[1]
            dog_temperament2 = dog_temp_split[2]
        elif len(dog_temp_split) >= 4:
            dog_temperament1 = dog_temp_split[2]
            dog_temperament2 = dog_temp_split[3]

    dog_lifespan = dog['life_span']
    dog_bred_for = dog.get('dog_bred_for', None)

    dog_temperament1_id = insert_and_get_id('dog_temperament1', 'dog_temperament1', dog_temperament1)
    dog_temperament2_id = insert_and_get_id('dog_temperament2', 'dog_temperament2', dog_temperament2)
    dog_lifespan_id = insert_and_get_id('dog_lifespans', 'dog_lifespan', dog_lifespan)
    dog_bred_for_id = insert_and_get_id('dog_bred_for', 'dog_bred_for', dog_bred_for)

    cur.execute("""
        INSERT OR IGNORE INTO doginfo 
        (dog_breedname, dog_temperament1_id, dog_temperament2_id, dog_lifespan_id, dog_bred_for_id)
        VALUES (?, ?, ?, ?, ?)""",
        (dog_breedname, dog_temperament1_id, dog_temperament2_id, dog_lifespan_id, dog_bred_for_id)
    )


conn.commit()
conn.close()