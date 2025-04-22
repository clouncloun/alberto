import matplotlib.pyplot as plt
import csv

# Read the data from the CSV file
def read_cat_data(filename="cat_scores.csv"):
    breeds = []
    pf_scores = []
    api_scores = []

    with open("cat_scores.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                pf = int(row["pfscore"])
                api = int(row["apiscore"])
                breed = row["breed"]
                
        # Append values with fudge factor
                breeds.append(breed)
                pf_scores.append(pf if pf > 0 else 0.5)
                api_scores.append(api if api > 0 else 0.5)
            except ValueError:
                continue

    return breeds, pf_scores, api_scores

def create_cat_vis(breeds, pf_scores, api_scores):
    if not breeds:
        print("No valid data to plot.")
        return
# Create the plot
    x = range(len(breeds))  # x-axis positions

# Plotting the stacked bars for Petfinder scores and API scores
    fig, ax = plt.subplots(figsize=(10, 6))

# Create the bars for Petfinder scores (in blue)
    bars1 = ax.bar(x, pf_scores, label="Petfinder", color='blue')

# Create the bars for API scores (in orange), stacked on top of Petfinder scores
    bars2 = ax.bar(x, api_scores, bottom=pf_scores, label="API", color='orange')

# Label the axes and the title
    ax.set_xlabel('Cat Breeds')
    ax.set_ylabel('Maintenance Scores')
    ax.set_title('Cat Maintenance Scores: Petfinder vs API')
    ax.set_xticks(x)
    ax.set_xticklabels(breeds, rotation=45, ha='right')

#  Add a legend
    ax.legend()

# Show the plot
    plt.tight_layout()
    plt.show()

def main():
    breeds, pf_scores, api_scores = read_cat_data()
    create_cat_vis(breeds, pf_scores, api_scores)

if __name__ == "__main__":
    main()