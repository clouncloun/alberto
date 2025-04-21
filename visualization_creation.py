import matplotlib.pyplot as plt
import csv

breeds = []
pf_scores = []
api_scores = []
data_counts = []

# Read data from CSV
with open("dog_scores.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            pf = int(row["pfscore"])
            api = int(row["apiscore"])
            count = int(row["datapoints"])

            breed = row["breed"]
            breeds.append(breed)

            # Apply fudge factor to zeros if needed
            pf_scores.append(pf if pf > 0 else 0.5)
            api_scores.append(api if api > 0 else 0.5)
            data_counts.append(count)
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
    middle_positions = [(x + x + bar_width) / 2 for x in x_positions]

    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Bar plots
    ax1.bar(x_positions, pf_scores, width=bar_width, label="Petfinder Score", color="skyblue")
    ax1.bar(api_positions, api_scores, width=bar_width, label="API Score", color="salmon")

    ax1.set_xlabel("Dog Breed")
    ax1.set_ylabel("Niceness Score (0–100)")
    ax1.set_ylim(0, 105)
    ax1.set_xticks(middle_positions)
    ax1.set_xticklabels(breeds, rotation=90)
    ax1.legend(loc="upper left")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Line plot overlay (data volume)
    ax2 = ax1.twinx()
    ax2.plot(middle_positions, data_counts, color='black', marker='o', linestyle='-', label='Data Points')
    ax2.set_ylabel("Number of Data Points")
    ax2.legend(loc="upper right")

    plt.title("Niceness Comparison: Petfinder vs API with Data Volume Overlay")
    plt.tight_layout()
    plt.show()
