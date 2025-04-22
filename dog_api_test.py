import requests
import sqlite3
import os

API_KEY = "live_5hy8HGezYufdDjX10cnmJbLLgp34L52f7ZUEv0BeIQU9T69hmdFjtCshS2RZ672v"
COUNTER_FILE = 'dog_counter.txt'

def get_current_index():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def save_current_index(index):
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(index))

def fetch_dog_data(api_key, limit=25):
    url = "https://api.thedogapi.com/v1/breeds"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        print('Error Fetching Dog Data')
    return []

def get_next_batch(data, current_index, batch_size=25):
    end_index = min(current_index + batch_size, len(data))
    return data[current_index:end_index], end_index

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

    cur.execute("""CREATE TABLE IF NOT EXISTS dog_temperaments (
        id INTEGER PRIMARY KEY,
        dog_temperament TEXT UNIQUE
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS doginfo (
        dog_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dog_breedname TEXT,
        dog_temperament_id INTEGER,
        dog_bred_for_id INTEGER,
        dog_breed_group_id INTEGER,
        dog_lifespan_id INTEGER,
        dog_child_friendly INTEGER,
        dog_health_issues INTEGER,
        dog_intelligence INTEGER,
        FOREIGN KEY (dog_temperament_id) REFERENCES dog_temperaments(id),
        FOREIGN KEY (dog_bred_for_id) REFERENCES dog_bred_for(id),
        FOREIGN KEY (dog_breed_group_id) REFERENCES dog_breed_group(id),
        FOREIGN KEY (dog_lifespan_id) REFERENCES dog_lifespans(id)
    )""")
    
    return conn, cur

def insert_and_get_id(cur, table, column, value):
    if not value:
        return 0
    cur.execute(f"INSERT OR IGNORE INTO {table} ({column}) VALUES (?)", (value,))
    cur.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    result = cur.fetchone()
    return result[0] if result else 0

def insert_dog_data(doglist, cur):
    for dog in doglist:
        dog_breedname = dog.get('name')
        dog_temperament = dog.get('temperament')
        dog_origin = dog.get('origin')  # Optional field
        dog_lifespan = dog.get('life_span')
        dog_bred_for = dog.get('bred_for')
        dog_breed_group = dog.get('breed_group')
        dog_child_friendly = dog.get('child_friendly', 0)
        dog_health_issues = dog.get('health_issues', 0)
        dog_intelligence = dog.get('intelligence', 0)

        dog_temperament_id = insert_and_get_id(cur, 'dog_temperaments', 'dog_temperament', dog_temperament)
        dog_lifespan_id = insert_and_get_id(cur, 'dog_lifespans', 'dog_lifespan', dog_lifespan)
        dog_bred_for_id = insert_and_get_id(cur, 'dog_bred_for', 'dog_bred_for', dog_bred_for)
        dog_breed_group_id = insert_and_get_id(cur, 'dog_breed_group', 'dog_breed_group', dog_breed_group)

        cur.execute("""
        INSERT OR IGNORE INTO doginfo 
        (dog_breedname, dog_temperament_id, dog_bred_for_id, dog_breed_group_id, dog_lifespan_id,
         dog_child_friendly, dog_health_issues, dog_intelligence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (dog_breedname, dog_temperament_id, dog_bred_for_id, dog_breed_group_id, dog_lifespan_id,
         dog_child_friendly, dog_health_issues, dog_intelligence))

def main():
    doglist = fetch_dog_data(API_KEY)
    current_index = get_current_index()
    batch, new_index = get_next_batch(doglist, current_index)
    conn, cur = setup_database()
    insert_dog_data(batch, cur)
    conn.commit()
    if len(batch) == 25:
        save_current_index(new_index)
    else:
        save_current_index(0)
    conn.close()

if __name__ == "__main__":
    main()