import sqlite3
import csv

# ---------------------- DATABASE UTILS ----------------------

def get_data_from_table_as_dict(table_name, db="petfinder_pets.db"):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_doginfo_with_temperament(db="petfinder_pets.db"):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT di.*, dt.dog_temperament
        FROM doginfo di
        LEFT JOIN dog_temperaments dt ON di.dog_temperament_id = dt.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------------------- DATA PROCESSING ----------------------

def split_animals_by_species(pfinder_data, species_data):
    speciesdict = {item["id"]: item["specie"] for item in species_data}
    catlist, doglist = [], []
    for pet in pfinder_data:
        #print(pfinder_data)
        species_name = speciesdict.get(pet["species"], "Unknown").lower()
        if species_name == "cat":
            catlist.append(pet)
        elif species_name == "dog":
            doglist.append(pet)
    return catlist, doglist

def enrich_with_breed_names(petlist, breeds_data):
    breeddict = {b["id"]: b["breed"] for b in breeds_data}
    for pet in petlist:
        pet["breed_name"] = breeddict.get(pet.get("breed"), "Unknown")
    return petlist

def standardize_dog_breeds(doglist):
    replacements = {
        "Pit Bull Terrier": "American Pit Bull Terrier",
        "English Bulldog": "Olde English Bulldogge",
        "Bulldog": "Olde English Bulldogge",
        "Shar-Pei": "Chinese Shar-Pei",
        "Hound": "Basset Hound",
        "Cattle Dog": "Australian Cattle Dog",
        "Husky": "Siberian Husky",
        "Australian Cattle Dog / Blue Heeler": "Australian Cattle Dog",
        "Schnauzer": "Giant Schnauzer",
        "Collie": "Border Collie",
    }
    for dog in doglist:
        name = dog["breed_name"]
        if "Labrador Retriever" in name:
            dog["breed_name"] = "Labrador Retriever"
        elif "German Shepherd" in name:
            dog["breed_name"] = "German Shepherd Dog"
        elif name in replacements:
            dog["breed_name"] = replacements[name]
    return doglist

def match_breeds_with_info(petlist, breeddata, breed_key):
    matched, unmatched = [], []
    for pet in petlist:
        breed_name = pet["breed_name"]
        if any(breed[breed_key] == breed_name for breed in breeddata):
            matched.append(pet)
        else:
            unmatched.append(breed_name)
    return matched, unmatched

# ---------------------- DOG SCORING ----------------------

def calculate_nice_dog_scores(dogbreeddata):
    nicedogs = {}
    for breed in dogbreeddata:
        temperament = breed.get("dog_temperament", "")
        temperament = temperament.split(", ") if temperament else []
        score = sum([
            temperament.count("Gentle") * 2,
            temperament.count("Calm") * 2,
            temperament.count("Friendly"),
            temperament.count("Trainable"),
            temperament.count("Patient"),
            temperament.count("Sociable")
        ])
        nicedogs[breed["dog_breedname"]] = round((score / 5) * 100)
    return nicedogs

def calculate_petfinder_dog_scores(dogs_with_breed_data):
    scores = {}
    counts = {}
    if not scores:
        print("Warning: No cat scores to calculate.")
        return {}, {}
    for dog in dogs_with_breed_data:
        breed = dog["breed_name"]
        score = dog["good_with_children"]
        scores.setdefault(breed, []).append(score)
    normalized_scores = {}
    raw_averages = {k: sum(v)/len(v) for k, v in scores.items()}
    min_score, max_score = min(raw_averages.values()), max(raw_averages.values())
    for breed, avg in raw_averages.items():
        normalized = 0 if max_score == min_score else (avg - min_score) / (max_score - min_score)
        normalized_scores[breed] = round(normalized * 100)
        counts[breed] = len(scores[breed])
    return normalized_scores, counts

def write_dog_scores_to_csv(filename, pf_scores, api_scores, counts):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["breed", "pfscore", "apiscore", "datapoints"])
        writer.writeheader()
        for breed in pf_scores:
            if breed in api_scores:
                writer.writerow({
                    "breed": breed,
                    "pfscore": pf_scores[breed],
                    "apiscore": api_scores[breed],
                    "datapoints": counts.get(breed, 0)
                })

# ---------------------- CAT SCORING ----------------------

def calculate_cat_maintenance_scores(catbreeddata):
    scores = {}
    for breed in catbreeddata:
        name = breed["cat_breedname"]
        shedding = breed["cat_shedding_level"]
        health = breed["cat_health_issues"]
        if shedding and health:
            score = (
                (1 if shedding <= 2 else 2 if shedding == 3 else 3 if shedding == 4 else 4) +
                (1 if health <= 2 else 2 if health == 3 else 3)
            )
            scores[name] = round((score / 5) * 100)
    return scores

def calculate_petfinder_cat_scores(cats_with_breed_data):
    scores = {}
    if not scores:
        print("Warning: No cat scores to calculate.")
        return {}, {}
    for cat in cats_with_breed_data:
        breed = cat["breed_name"]
        score = cat["house_trained"]
        scores.setdefault(breed, []).append(score)
    averages = {k: sum(v)/len(v) for k, v in scores.items()}
    min_score, max_score = min(averages.values()), max(averages.values())
    normalized = {}
    for breed, avg in averages.items():
        normalized[breed] = 0 if max_score == min_score else round(((avg - min_score) / (max_score - min_score)) * 100)
    return normalized

def write_cat_scores_to_csv(filename, pf_scores, api_scores):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["breed", "pfscore", "apiscore"])
        writer.writeheader()
        for breed in pf_scores:
            if breed in api_scores:
                writer.writerow({
                    "breed": breed,
                    "pfscore": pf_scores[breed],
                    "apiscore": api_scores[breed]
                })

# ---------------------- MAIN FUNCTION ----------------------
def main():
    # Load Petfinder data
    pfinder_data = get_data_from_table_as_dict("petfinder_pets")    
    species_data = get_data_from_table_as_dict("petfinder_species")
    breed_data = get_data_from_table_as_dict("petfinder_breeds")

    # Load normalized breed data from your own API
    dogbreeddata = get_doginfo_with_temperament()
    catinfo = get_data_from_table_as_dict("catinfo")  # cats don't use JOIN yet

    # Split and enrich petfinder data
    catlist, doglist = split_animals_by_species(pfinder_data, species_data)
    catlist = enrich_with_breed_names(catlist, breed_data)
    doglist = enrich_with_breed_names(doglist, breed_data)
    #print("Sample dog with breed name:", doglist[0] if doglist else "No dogs")
    doglist = standardize_dog_breeds(doglist)
    #print("Number of dogs after species split:", len(doglist))
    #print("Standardized breed names:", [d["breed_name"] for d in doglist[:5]])

    # Dog scoring
    #print("Doginfo breeds:", sorted(set(b["dog_breedname"] for b in dogbreeddata)))
    #print("Doglist breeds:", sorted(set(d["breed_name"] for d in doglist)))
    dogs_with_breed_data, _ = match_breeds_with_info(doglist, dogbreeddata, "dog_breedname")
    #print("dogs_with_breed_data sample:", dogs_with_breed_data[:2])
    nicedogs = calculate_nice_dog_scores(dogbreeddata)
    pf_dog_scores, dog_counts = calculate_petfinder_dog_scores(dogs_with_breed_data)
    write_dog_scores_to_csv("dog_scores.csv", pf_dog_scores, nicedogs, dog_counts)

    # Cat scoring
    cats_with_breed_data, _ = match_breeds_with_info(catlist, catinfo, "cat_breedname")
    maintenancecats = calculate_cat_maintenance_scores(catinfo)
    pf_cat_scores = calculate_petfinder_cat_scores(cats_with_breed_data)
    write_cat_scores_to_csv("cat_scores.csv", pf_cat_scores, maintenancecats)

# ---------------------- RUN SCRIPT ----------------------

if __name__ == "__main__":
    main()