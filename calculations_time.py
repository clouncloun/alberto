import sqlite3

def get_data_from_table_as_dict(table_name):
    conn = sqlite3.connect("petfinder_pets.db")
    conn.row_factory = sqlite3.Row  # to access columns by name
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    return [dict(row) for row in rows]


# separate petfinder pets into catlist and doglist 
catlist = []
doglist = []
pfinderdata = get_data_from_table_as_dict("petfinder_pets")
specieslist = get_data_from_table_as_dict("petfinder_species")

speciesdict = {}
for item in specieslist:
    speciesdict[item["id"]] = item ["specie"]

for pet in pfinderdata:
    petspeciesid = pet["species"]
    petspeciesname = speciesdict.get(petspeciesid, "Unknown")
    if petspeciesname.lower() == "cat":
        catlist.append(pet)
    if petspeciesname.lower() == "dog":
        doglist.append(pet)


# get breed from the id table for each cat in the catlist, each dog in the doglist
breedslist = get_data_from_table_as_dict("petfinder_breeds")

breeddict = {b["id"]: b["breed"] for b in breedslist}
for cat in catlist:
    breed_id = cat.get("breed")
    breed_name = breeddict.get(breed_id, "Unknown")
    cat["breed_name"] = breed_name
for dog in doglist:
    breed_id = dog.get("breed")
    breed_name = breeddict.get(breed_id, "Unknown")
    dog["breed_name"] = breed_name

    
# makes a list of all the dogs that we have the breeds for in doginfo
dogs_with_breed_data = []
dogbreeddata = get_data_from_table_as_dict("doginfo")
for dog in doglist:
    dogbreed = dog["breed_name"]
    for breed in dogbreeddata:
        breedname = breed["dog_breedname"]
        if breedname == dogbreed:
            dogs_with_breed_data.append(dog)
            break

#print(dogs_with_breed_data)

# finding what the most common breed is
breed_counts = {}
for dog in dogs_with_breed_data:
    breed = dog["breed_name"]
    if breed in breed_counts:
        breed_counts[breed] += 1
    else:
        breed_counts[breed] = 1
most_common_breed = None
highest_breed_count = 0
for breed, count in breed_counts.items():
    if count > highest_breed_count:
        most_common_breed = breed
        highest_breed_count = count



# time to work with the temperaments!

nicedogs = {}
for breed in dogbreeddata:
    breedname = breed["dog_breedname"]
    temperament = breed["dog_temperament"]
    if temperament is not None:
        temperament = temperament.split(", ")
        niceness = 0
        if "Gentle" in temperament:
            niceness += 2
        if "Calm" in temperament:
            niceness += 2
        if "Friendly" in temperament:
            niceness += 1
        if "Trainable" in temperament:
            niceness += 1
        if "Patient" in temperament:
            niceness += 1
        if "Sociable" in temperament:
            niceness += 1
        nicedogs[breedname] = niceness

        
nicepetfinderdogs = {}
for dog in dogs_with_breed_data:
    dogbreed = (dog["breed_name"])
    nicescore = (dog["good_with_children"])
    if dogbreed not in nicepetfinderdogs:
        nicepetfinderdogs[dogbreed] = (nicescore,)
    if dogbreed in nicepetfinderdogs:
        nicepetfinderdogs[dogbreed] += (nicescore,)
for name, scorelist in nicepetfinderdogs.items():
    listlength = (len(scorelist))
    listsum = (sum(scorelist))
    dogbreedscore = listsum / listlength
    #print(name, dogbreedscore)
