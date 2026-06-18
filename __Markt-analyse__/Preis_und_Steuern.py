import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# =====================================================
# GET SCRIPT DIRECTORY
# =====================================================

script_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.join(
    script_dir,
    "data"
)

output_dir = os.path.join(
    script_dir,
    "Grafiken"
)

os.makedirs(
    output_dir,
    exist_ok=True
)

# =====================================================
# LOAD CSV DATA
# =====================================================

csv_path = os.path.join(
    data_dir,
    "preis_und_steuer.csv"
)

df = pd.read_csv(csv_path)

# =====================================================
# EXTRACT COLUMNS
# =====================================================

jahre = df["jahr"].tolist()
preis = df["preis"].tolist()
steuer = df["steuer"].tolist()

# =====================================================
# STEUERANTEIL
# =====================================================

steueranteil = [
    s / p * 100
    for s, p in zip(steuer, preis)
]

# =====================================================
# STYLE
# =====================================================

plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(
    figsize=(16, 8)
)

# =====================================================
# LINES
# =====================================================

ax.plot(
    jahre,
    preis,
    marker="o",
    linewidth=3,
    markersize=7,
    label="Preis (Cent)"
)

ax.plot(
    jahre,
    steuer,
    marker="s",
    linewidth=3,
    markersize=7,
    label="Tabaksteuer (Cent)"
)

ax.plot(
    jahre,
    steueranteil,
    marker="^",
    linewidth=2.5,
    markersize=7,
    label="Steueranteil (%)"
)

# =====================================================
# STATISTICS - MEAN & MEDIAN
# =====================================================

mean_preis = np.mean(preis)
median_preis = np.median(preis)

ax.axhline(
    mean_preis,
    linestyle="--",
    alpha=0.5,
    color="blue",
    label=f"Preis Mean: {mean_preis:.2f}"
)

ax.axhline(
    median_preis,
    linestyle=":",
    alpha=0.5,
    color="blue",
    label=f"Preis Median: {median_preis:.2f}"
)

mean_steuer = np.mean(steuer)
median_steuer = np.median(steuer)

ax.axhline(
    mean_steuer,
    linestyle="--",
    alpha=0.5,
    color="orange",
    label=f"Steuer Mean: {mean_steuer:.2f}"
)

ax.axhline(
    median_steuer,
    linestyle=":",
    alpha=0.5,
    color="orange",
    label=f"Steuer Median: {median_steuer:.2f}"
)

mean_steueranteil = np.mean(steueranteil)
median_steueranteil = np.median(steueranteil)

ax.axhline(
    mean_steueranteil,
    linestyle="--",
    alpha=0.5,
    color="green",
    label=f"Steueranteil Mean: {mean_steueranteil:.2f}%"
)

ax.axhline(
    median_steueranteil,
    linestyle=":",
    alpha=0.5,
    color="green",
    label=f"Steueranteil Median: {median_steueranteil:.2f}%"
)

# =====================================================
# MIN / MAX - PREIS
# =====================================================

min_preis_index = np.argmin(preis)
max_preis_index = np.argmax(preis)

ax.scatter(
    jahre[min_preis_index],
    preis[min_preis_index],
    color="black",
    s=120,
    zorder=5,
    label="Preis Min"
)

ax.scatter(
    jahre[max_preis_index],
    preis[max_preis_index],
    color="red",
    s=120,
    zorder=5,
    label="Preis Max"
)

# =====================================================
# MIN / MAX - STEUER
# =====================================================

min_steuer_index = np.argmin(steuer)
max_steuer_index = np.argmax(steuer)

ax.scatter(
    jahre[min_steuer_index],
    steuer[min_steuer_index],
    color="black",
    s=120,
    marker="s",
    zorder=5,
    label="Steuer Min"
)

ax.scatter(
    jahre[max_steuer_index],
    steuer[max_steuer_index],
    color="red",
    s=120,
    marker="s",
    zorder=5,
    label="Steuer Max"
)

# =====================================================
# MIN / MAX - STEUERANTEIL
# =====================================================

min_steueranteil_index = np.argmin(steueranteil)
max_steueranteil_index = np.argmax(steueranteil)

ax.scatter(
    jahre[min_steueranteil_index],
    steueranteil[min_steueranteil_index],
    color="black",
    s=120,
    marker="^",
    zorder=5,
    label="Steueranteil Min"
)

ax.scatter(
    jahre[max_steueranteil_index],
    steueranteil[max_steueranteil_index],
    color="red",
    s=120,
    marker="^",
    zorder=5,
    label="Steueranteil Max"
)

# =====================================================
# TITLES
# =====================================================

ax.set_title(
    "Preis, Steuer und Steueranteil von Zigaretten\nDeutschland 1991–2025",
    fontsize=22,
    weight="bold",
    pad=20
)

ax.set_xlabel(
    "Jahr",
    fontsize=14
)

ax.set_ylabel(
    "Wert",
    fontsize=14
)

# =====================================================
# LEGEND
# =====================================================

ax.legend(
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    fontsize=11
)

# =====================================================
# GRID
# =====================================================

ax.grid(
    True,
    linestyle="--",
    alpha=0.6
)

# =====================================================
# REMOVE EXTRA BORDERS
# =====================================================

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# =====================================================
# ROTATE YEARS
# =====================================================

plt.xticks(rotation=45)

# =====================================================
# SAVE GRAPH
# =====================================================

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "Preis_und_Steuern.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

print(
    f"Grafik gespeichert in:\n{output_dir}"
)

plt.show()