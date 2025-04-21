import matplotlib.pyplot as plt
import csv

# Read the data from the CSV file
breeds = []
pf_scores = []
api_scores = []

with open("cat_scores.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        breeds.append(row["breed"])
        pf_scores.append(int(row["pfscore"]))
        api_scores.append(int(row["apiscore"]))

print(breeds)
print(pf_scores)
print(api_scores)

'''

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
'''