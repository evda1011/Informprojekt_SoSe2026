import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# =====================================================
# PATHS
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
# LOAD DATA
# =====================================================

konsum_df = pd.read_csv(
    os.path.join(
        data_dir,
        "konsumverbrauch_zigaretten.csv"
    )
)

from data.preis_zigaretten import jahre, preis_cent

preis_df = pd.DataFrame({
    "jahr": jahre,
    "preis": preis_cent
})

# =====================================================
# MERGE DATA
# =====================================================

df = pd.merge(
    preis_df,
    konsum_df,
    on="jahr",
    how="inner"
)

# =====================================================
# STYLE
# =====================================================

plt.style.use("seaborn-v0_8-whitegrid")

# =====================================================
# GRAPH 1
# Preisentwicklung und Konsumverhalten
# =====================================================

fig, ax1 = plt.subplots(
    figsize=(16, 8)
)

ax_price = ax1.twinx()

# -----------------------------------------------------
# KONSUM
# -----------------------------------------------------

ax1.plot(
    df["jahr"],
    df["verbrauch_pro_einwohner"],
    color="tab:blue",
    linewidth=3.5,
    marker="o",
    markersize=7,
    label="Konsum"
)

ax1.fill_between(
    df["jahr"],
    df["verbrauch_pro_einwohner"],
    color="tab:blue",
    alpha=0.15
)

# -----------------------------------------------------
# PREIS
# -----------------------------------------------------

ax_price.plot(
    df["jahr"],
    df["preis"],
    color="tab:red",
    linewidth=3.5,
    marker="s",
    markersize=6,
    label="Preis"
)

# -----------------------------------------------------
# TREND KONSUM
# -----------------------------------------------------

z_konsum = np.polyfit(
    df["jahr"],
    df["verbrauch_pro_einwohner"],
    1
)

p_konsum = np.poly1d(z_konsum)

ax1.plot(
    df["jahr"],
    p_konsum(df["jahr"]),
    color="tab:blue",
    linestyle="--",
    linewidth=2.5,
    label="Konsum Trend"
)

# -----------------------------------------------------
# TREND PREIS
# -----------------------------------------------------

z_preis = np.polyfit(
    df["jahr"],
    df["preis"],
    1
)

p_preis = np.poly1d(z_preis)

ax_price.plot(
    df["jahr"],
    p_preis(df["jahr"]),
    color="darkred",
    linestyle="--",
    linewidth=2.5,
    label="Preis Trend"
)

# -----------------------------------------------------
# TITLES
# -----------------------------------------------------

ax1.set_title(
    "Preisentwicklung und Konsumverhalten von Zigaretten\nDeutschland 1965–2025",
    fontsize=22,
    weight="bold",
    pad=20
)

ax1.set_xlabel(
    "Jahr",
    fontsize=14
)

ax1.set_ylabel(
    "Zigaretten pro Einwohner",
    fontsize=14,
    color="tab:blue"
)

ax_price.set_ylabel(
    "Preis pro Packung (Cent)",
    fontsize=14,
    color="tab:red"
)

# -----------------------------------------------------
# COLORED TICKS
# -----------------------------------------------------

ax1.tick_params(
    axis="y",
    colors="tab:blue"
)

ax_price.tick_params(
    axis="y",
    colors="tab:red"
)

ax1.tick_params(
    axis="x",
    rotation=45
)

# -----------------------------------------------------
# LEGEND
# -----------------------------------------------------

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax_price.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    fontsize=11,
    loc="upper right"
)

# -----------------------------------------------------
# GRID
# -----------------------------------------------------

ax1.grid(
    True,
    linestyle="--",
    alpha=0.6
)

ax_price.grid(False)

# -----------------------------------------------------
# BORDERS
# -----------------------------------------------------

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax_price.spines["top"].set_visible(False)

# -----------------------------------------------------
# SAVE GRAPH 1
# -----------------------------------------------------

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "Preis_vs_Konsum_Zeitverlauf.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# GRAPH 2
# KORRELATION
# =====================================================

fig, ax2 = plt.subplots(
    figsize=(14, 8)
)

# -----------------------------------------------------
# SCATTER
# -----------------------------------------------------

ax2.scatter(
    df["preis"],
    df["verbrauch_pro_einwohner"],
    s=90,
    color="tab:purple",
    alpha=0.8,
    label="Datenpunkte"
)

# -----------------------------------------------------
# REGRESSION
# -----------------------------------------------------

z = np.polyfit(
    df["preis"],
    df["verbrauch_pro_einwohner"],
    1
)

p = np.poly1d(z)

ax2.plot(
    df["preis"],
    p(df["preis"]),
    linestyle="--",
    linewidth=2.5,
    color="black",
    label="Regression"
)

# -----------------------------------------------------
# KORRELATION
# -----------------------------------------------------

corr = np.corrcoef(
    df["preis"],
    df["verbrauch_pro_einwohner"]
)[0, 1]

ax2.text(
    0.05,
    0.95,
    f"r = {corr:.2f}",
    transform=ax2.transAxes,
    fontsize=12,
    verticalalignment="top",
    bbox=dict(
        boxstyle="round",
        alpha=0.2
    )
)

# -----------------------------------------------------
# TITLES
# -----------------------------------------------------

ax2.set_title(
    "Zusammenhang zwischen Preis und Konsum",
    fontsize=18,
    weight="bold"
)

ax2.set_xlabel(
    "Preis pro Packung (Cent)",
    fontsize=14
)

ax2.set_ylabel(
    "Zigaretten pro Einwohner",
    fontsize=14
)

# -----------------------------------------------------
# LEGEND
# -----------------------------------------------------

ax2.legend(
    fontsize=11,
    loc="upper right"
)

# -----------------------------------------------------
# GRID
# -----------------------------------------------------

ax2.grid(
    True,
    linestyle="--",
    alpha=0.6
)

# -----------------------------------------------------
# BORDERS
# -----------------------------------------------------

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# -----------------------------------------------------
# SAVE GRAPH 2
# -----------------------------------------------------

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "Preis_vs_Konsum_Korrelation.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(
    f"Grafiken gespeichert in:\n{output_dir}"
)