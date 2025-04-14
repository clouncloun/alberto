import sqlite3

def get_data_from_table_as_dict(table_name):
    conn = sqlite3.connect("petfinder_pets.db")
    conn.row_factory = sqlite3.Row  # to access columns by name
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    return [dict(row) for row in rows]


petswithbreeddata = []

catbreeddata = get_data_from_table_as_dict("catinfo")
for cat in catbreeddata:
    catbreed = (cat["cat_breedname"])
    allbreeddata = get_data_from_table_as_dict("breeds")
    for creature in allbreeddata:
        creaturebreed = (creature['breed'])
        if catbreed == creaturebreed:
            petswithbreeddata.append(creature)


print(petswithbreeddata)