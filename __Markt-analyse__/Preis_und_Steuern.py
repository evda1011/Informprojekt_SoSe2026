import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# Pfade
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")
output_dir = os.path.join(script_dir, "Grafiken")

os.makedirs(output_dir, exist_ok=True)


# CSV laden
csv_path = os.path.join(data_dir, "preis_und_steuer.csv")
df = pd.read_csv(csv_path, encoding="utf-8")

# Falls Leerzeichen in den Namen sind
df.columns = df.columns.str.strip()
print(df.head())

# Daten
jahre = df["jahr"].tolist()
preis = df["preis"].tolist()
steuer = df["steuer"].tolist()

# Steueranteil berechnen
steueranteil = [
    s / p * 100
    for s, p in zip(steuer, preis)]

# Style
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(16, 8))

# Linien
ax.plot(
    jahre,
    preis,
    marker="o",
    linewidth=3,
    markersize=7,
    label="Preis (Cent)")

ax.plot(
    jahre,
    steuer,
    marker="s",
    linewidth=3,
    markersize=7,
    label="Tabaksteuer (Cent)")

ax.plot(
    jahre,
    steueranteil,
    marker="^",
    linewidth=2.5,
    markersize=7,
    label="Steueranteil (%)")

# Mittelwerte / Median
mean_preis = np.mean(preis)
median_preis = np.median(preis)

ax.axhline(
    mean_preis,
    linestyle="--",
    alpha=0.5,
    color="blue",
    label=f"Preis Mean: {mean_preis:.2f}")

ax.axhline(
    median_preis,
    linestyle=":",
    alpha=0.5,
    color="blue",
    label=f"Preis Median: {median_preis:.2f}")

mean_steuer = np.mean(steuer)
median_steuer = np.median(steuer)

ax.axhline(
    mean_steuer,
    linestyle="--",
    alpha=0.5,
    color="orange",
    label=f"Steuer Mean: {mean_steuer:.2f}")

ax.axhline(
    median_steuer,
    linestyle=":",
    alpha=0.5,
    color="orange",
    label=f"Steuer Median: {median_steuer:.2f}")

mean_steueranteil = np.mean(steueranteil)
median_steueranteil = np.median(steueranteil)

ax.axhline(
    mean_steueranteil,
    linestyle="--",
    alpha=0.5,
    color="green",
    label=f"Steueranteil Mean: {mean_steueranteil:.2f}%")

ax.axhline(
    median_steueranteil,
    linestyle=":",
    alpha=0.5,
    color="green",
    label=f"Steueranteil Median: {median_steueranteil:.2f}%")


# Min / Max Preis
min_preis_index = np.argmin(preis)
max_preis_index = np.argmax(preis)

ax.scatter(
    jahre[min_preis_index],
    preis[min_preis_index],
    color="black",
    s=120,
    zorder=5,
    label="Preis Min")

ax.scatter(
    jahre[max_preis_index],
    preis[max_preis_index],
    color="red",
    s=120,
    zorder=5,
    label="Preis Max")


# Min / Max Steuer
min_steuer_index = np.argmin(steuer)
max_steuer_index = np.argmax(steuer)

ax.scatter(
    jahre[min_steuer_index],
    steuer[min_steuer_index],
    color="black",
    s=120,
    marker="s",
    zorder=5,
    label="Steuer Min")

ax.scatter(
    jahre[max_steuer_index],
    steuer[max_steuer_index],
    color="red",
    s=120,
    marker="s",
    zorder=5,
    label="Steuer Max")

# Min / Max Steueranteil
min_steueranteil_index = np.argmin(steueranteil)
max_steueranteil_index = np.argmax(steueranteil)

ax.scatter(
    jahre[min_steueranteil_index],
    steueranteil[min_steueranteil_index],
    color="black",
    s=120,
    marker="^",
    zorder=5,
    label="Steueranteil Min")

ax.scatter(
    jahre[max_steueranteil_index],
    steueranteil[max_steueranteil_index],
    color="red",
    s=120,
    marker="^",
    zorder=5,
    label="Steueranteil Max")


# Titel
ax.set_title(
    "Preis, Steuer und Steueranteil von Zigaretten\nDeutschland 1991–2025",
    fontsize=22,
    weight="bold",
    pad=20)

ax.set_xlabel("Jahr", fontsize=14)
ax.set_ylabel("Wert", fontsize=14)

ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=11)

ax.grid(True, linestyle="--", alpha=0.6)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.xticks(rotation=45)

plt.tight_layout()

# Pfade
speicher= os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(speicher, "data")
output_dir = os.path.join(speicher, "Grafiken")

os.makedirs(output_dir, exist_ok=True)

plt.show()