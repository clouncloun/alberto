import matplotlib.pyplot as plt
import csv

# Step 1: Read the data from the CSV file
breeds = []
pf_scores = []
api_scores = []

def read_cat_scores(filename="cat_scores.csv"):
    breeds = []
    pf_scores = []
    api_scores = []
    data_counts = []

    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                pf = int(row["pfscore"])
                api = int(row["apiscore"])
                count = int(row["datapoints"])
                breed = row["breed"]

                # Append values with fudge factor
                breeds.append(breed)
                pf_scores.append(pf if pf > 0 else 0.5)
                api_scores.append(api if api > 0 else 0.5)
                data_counts.append(count)
            except ValueError:
                continue

    return breeds, pf_scores, api_scores, data_counts

def create_cat_vis(breeds, pf_scores, api_scores, data_counts):
    if not breeds:
        print("No valid data to plot.")
        return
    x = range(len(breeds))  # x-axis positions

# Plotting the stacked bars for Petfinder scores and API scores
    fig, ax = plt.subplots(figsize=(10, 6))

# Create the bars for Petfinder scores (in blue)
    bars1 = ax.bar(x, pf_scores, label="Petfinder", color='blue')

# Create the bars for API scores (in orange), stacked on top of Petfinder scores
    bars2 = ax.bar(x, api_scores, bottom=pf_scores, label="API", color='orange')

# Step 3: Label the axes and the title
    ax.set_xlabel('Cat Breeds')
    ax.set_ylabel('Maintenance Scores')
    ax.set_title('Cat Maintenance Scores: Petfinder vs API')
    ax.set_xticks(x)
    ax.set_xticklabels(breeds, rotation=45, ha='right')

# Step 4: Add a legend
    ax.legend()

# Step 5: Show the plot
    plt.tight_layout()
    plt.show()

def main():
    breeds, pf_scores, api_scores, data_counts = read_cat_scores()
    create_cat_vis(breeds, pf_scores, api_scores, data_counts)

if __name__ == "__main__":
    main()