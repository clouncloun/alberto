import requests
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch_dog_data(api_key, limit=25):
    url = "https://api.thedogapi.com/v1/breeds"
    headers = {"Authorization": f"Bearer {api_key}"}
    doglist = []
    page = 0

    while True:
        params = {"limit": limit, "page": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, Message: {response.text}")
            break

        data = response.json()
        if not data:
            break

        doglist.extend(data)
        page += 1

    return doglist

def setup_database():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(path, "petfinder_pets.db"))
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS dog_bred_for (
        id INTEGER PRIMARY KEY, 
        dog_bred_for TEXT UNIQUE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS dog_breed_group (
        id INTEGER PRIMARY KEY, 
        dog_breed_group TEXT UNIQUE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS dog_lifespans (
        id INTEGER PRIMARY KEY, 
        dog_lifespan TEXT UNIQUE
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS doginfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dog_breedname TEXT,
        dog_temperament TEXT,
        dog_bred_for_id INTEGER DEFAULT 0,
        dog_breed_group_id INTEGER DEFAULT 0,
        dog_lifespan_id INTEGER DEFAULT 0,
        FOREIGN KEY (dog_bred_for_id) REFERENCES dog_bred_for(id),
        FOREIGN KEY (dog_breed_group_id) REFERENCES dog_breed_group(id),
        FOREIGN KEY (dog_lifespan_id) REFERENCES dog_lifespans(id)
    )""")

    return conn, cur

def insert_and_get_id(cur, table, column, value):
    if value is None:
        return 0
    cur.execute(f"INSERT OR IGNORE INTO {table} ({column}) VALUES (?)", (value,))
    cur.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    result = cur.fetchone()
    return result[0] if result else 0

def insert_dog_data(doglist, cur):
    for dog in doglist:
        dog_breedname = dog.get('name')
        dog_temperament = dog.get('temperament')
        dog_lifespan = dog.get('life_span')
        dog_bred_for = dog.get('bred_for')
        dog_breed_group = dog.get('breed_group')

        dog_lifespan_id = insert_and_get_id(cur, 'dog_lifespans', 'dog_lifespan', dog_lifespan)
        dog_bred_for_id = insert_and_get_id(cur, 'dog_bred_for', 'dog_bred_for', dog_bred_for)
        dog_breed_group_id = insert_and_get_id(cur, 'dog_breed_group', 'dog_breed_group', dog_breed_group)

        cur.execute("""
            INSERT OR IGNORE INTO doginfo 
            (dog_breedname, dog_temperament, dog_lifespan_id, dog_bred_for_id, dog_breed_group_id)
            VALUES (?, ?, ?, ?, ?)""",
            (dog_breedname, dog_temperament, dog_lifespan_id, dog_bred_for_id, dog_breed_group_id)
        )

def main():
    doglist = fetch_dog_data(API_KEY)
    conn, cur = setup_database()
    insert_dog_data(doglist, cur)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()