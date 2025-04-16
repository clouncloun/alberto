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

# adding breeds manually that don't match
for dog in doglist:
    if dog["breed_name"] == "Pit Bull Terrier":
        dog["breed_name"] = "American Pit Bull Terrier"
    if dog["breed_name"] == "English Bulldog":
        dog["breed_name"] = "Olde English Bulldogge"
    if dog["breed_name"] == "Bulldog":
        dog["breed_name"] = "Olde English Bulldogge"
    if dog["breed_name"] == "Shar-Pei":
        dog["breed_name"] = "Chinese Shar-Pei"
    if dog["breed_name"] == "Hound":
        dog["breed_name"] = "Basset Hound"
    if "Labrador Retriever" in dog["breed_name"]:
        dog["breed_name"] = "Labrador Retriever"
    if "German Shepherd" in dog["breed_name"]:
        dog["breed_name"] = "German Shepherd Dog"
    if dog["breed_name"] == "Cattle Dog":
        dog["breed_name"] = "Australian Cattle Dog"
    if dog["breed_name"] == "Husky":
        dog["breed_name"] = "Siberian Husky"
    if dog["breed_name"] == "Australian Cattle Dog / Blue Heeler":
        dog["breed_name"] = "Australian Cattle Dog"
    if dog["breed_name"] == "Schnauzer":
        dog["breed_name"] = "Giant Schnauzer"
    if dog["breed_name"] == "Collie":
        dog["breed_name"] = "Border Collie"

    
# makes a list of all the dogs that we have the breeds for in doginfo
dogs_with_breed_data = []
dogs_no_breed_data = []
dogbreeddata = get_data_from_table_as_dict("doginfo")
for dog in doglist:
    dogbreed = dog["breed_name"]
    found = False
    for breed in dogbreeddata:
        if breed["dog_breedname"] == dogbreed:
            dogs_with_breed_data.append(dog)
            found = True
            break
    if not found:
        dogs_no_breed_data.append(dogbreed)
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

sorted_breeddict = sorted(breed_counts.items(), key=lambda item: item[1], reverse=True)
# most common breeds of dogs: 
# print(sorted_breeddict)



# time to work with the temperaments!


########### nicedogs is a dictionary of scores (0-100 scale) describing how
########### nice breeds in the dog api are.  
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
        nicescore = niceness / 5
        nicedogs[breedname] = round(nicescore * 100)
#print(nicedogs)



########### nicepetfinderdogs is a dictionary of scores (0-100 scale) describing
########### how child friendly breeds in petfinder are.   
nicepetfinderdogs = {}
petfinderscores = {}
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
    petfinderscores[name] = dogbreedscore

min_score = min(petfinderscores.values())
max_score = max(petfinderscores.values())

for breed, score in petfinderscores.items():
    if max_score - min_score == 0:
        petfinderscores[breed] = 0
    else:
        normalized = (score - min_score) / (max_score - min_score)
        petfinderscores[breed] = round(normalized * 100)
#print(petfinderscores)

'''
# comparing the two!! 
count = 1
for realdog, pfscore in petfinderscores.items():
    for datadog, apiscore in nicedogs.items(): 
        if realdog == datadog:
            print(f"dog: {realdog}")
            print(f"petfinder score: {pfscore}")
            print(f"dog api score: {apiscore}")
'''


# okayyyy now it's cat time

# i'm doing cat hair length
for cat in catlist:
    print(cat["breed_name"])
    if cat["breed_name"] == "Domestic Short Hair":
        dog["breed_name"] = "American Shorthair"