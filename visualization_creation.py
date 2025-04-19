import matplotlib.pyplot as plt
import csv

breeds = []
pf_scores = []
api_scores = []

# Read data from CSV and filter incomplete rows
with open("dog_scores.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["pfscore"] and row["apiscore"]:
            try:
                pf = int(row["pfscore"])
                api = int(row["apiscore"])
                breeds.append(row["breed"])

                # Apply visual fudge factor to zero values
                pf_scores.append(pf if pf > 0 else 0.5)
                api_scores.append(api if api > 0 else 0.5)
            except ValueError:
                continue

# Plotting
if not breeds:
    print("No valid data to plot.")
else:
    num_breeds = len(breeds)
    bar_width = 0.4
    x_positions = list(range(num_breeds))
    api_positions = [x + bar_width for x in x_positions]

    plt.figure(figsize=(14, 7))
    plt.bar(x_positions, pf_scores, width=bar_width, label="Petfinder Score", color="skyblue")
    plt.bar(api_positions, api_scores, width=bar_width, label="API Score", color="salmon")

    middle_positions = [(x + x + bar_width) / 2 for x in x_positions]
    plt.xticks(middle_positions, breeds, rotation=90)

    plt.ylim(0, 105)  # back to normal y-axis range

    plt.xlabel("Dog Breed")
    plt.ylabel("Niceness Score (0–100)")
    plt.title("Niceness Comparison: Petfinder vs API")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()