import matplotlib.pyplot as plt
import csv


breeds = []
pf_scores = []
api_scores = []

with open("dog_scores.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        breeds.append(row["breed"])
        pf_scores.append(int(row["pfscore"]))
        api_scores.append(int(row["apiscore"]))

plt.figure(figsize=(12, 6))
plt.plot(breeds, pf_scores, label="Petfinder Score", marker="o")
plt.plot(breeds, api_scores, label="API Score", marker="x")
plt.xticks(rotation=90)
plt.xlabel("Dog Breed")
plt.ylabel("Niceness Score (0–100)")
plt.title("Comparison of Dog Breed Niceness Scores")
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()