import pandas as pd
import matplotlib.pyplot as plt

# Load data with error handling
try:
    # Use relative path - make sure the CSV is in the same folder
    df = pd.read_csv("konsumverbrauch_zigaretten_deutschland.csv")
except FileNotFoundError:
    print("Error: CSV file not found! Make sure 'konsumverbrauch_zigaretten_deutschland.csv' is in the same folder as the script.")
    exit()

# Select relevant columns and drop missing values
plot_df = df[["jahr", "verbrauch_pro_einwohner_quelle2"]].dropna()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(
    plot_df["jahr"],
    plot_df["verbrauch_pro_einwohner_quelle2"],
    marker="o",
    linestyle="-",
    color="b"
)

plt.title("Pro-Kopf-Verbrauch von Zigaretten in Deutschland")
plt.xlabel("Jahr")
plt.ylabel("Zigaretten pro Einwohner")
plt.grid(True)
plt.xticks(rotation=45)  # Better readability for years

# Optional: Add trend line (simple linear regression)
import numpy as np
z = np.polyfit(plot_df["jahr"], plot_df["verbrauch_pro_einwohner_quelle2"], 1)
p = np.poly1d(z)
plt.plot(plot_df["jahr"], p(plot_df["jahr"]), "r--", label="Trend")
plt.legend()

plt.tight_layout()
plt.show()