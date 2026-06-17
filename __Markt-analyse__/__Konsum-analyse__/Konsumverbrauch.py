import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
# =====================================================
# PATH TO CSV
# =====================================================
script_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(
    script_dir,
    "konsumverbrauch_zigaretten.csv"
)

# =====================================================
# LOAD DATA
# =====================================================
df = pd.read_csv(csv_path)

# =====================================================
# STYLE
# =====================================================
plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(16, 8))

# =====================================================
# MAIN LINE
# =====================================================
ax.plot(
    df["jahr"],
    df["verbrauch_pro_einwohner"],
    linewidth=3.5,
    marker="o",
    markersize=7,
    label="Zigarettenkonsum"
)

# =====================================================
# AREA UNDER CURVE
# =====================================================
ax.fill_between(
    df["jahr"],
    df["verbrauch_pro_einwohner"],
    alpha=0.15
)

# =====================================================
# TREND LINE
# =====================================================
z = np.polyfit(
    df["jahr"],
    df["verbrauch_pro_einwohner"],
    1
)

p = np.poly1d(z)

ax.plot(
    df["jahr"],
    p(df["jahr"]),
    linestyle="--",
    linewidth=2.5,
    label="Trendlinie"
)

# =====================================================
# MAXIMUM VALUE
# =====================================================
max_idx = df["verbrauch_pro_einwohner"].idxmax()

max_year = df.loc[max_idx, "jahr"]
max_value = df.loc[max_idx, "verbrauch_pro_einwohner"]

ax.scatter(
    max_year,
    max_value,
    s=120,
    zorder=5
)

ax.annotate(
    f"Historisches Hoch\n{max_year}: {max_value}",
    xy=(max_year, max_value),
    xytext=(1973, 2830),
    arrowprops=dict(
        arrowstyle="->",
        lw=2
    ),
    fontsize=12
)

# =====================================================
# MINIMUM VALUE
# =====================================================
min_idx = df["verbrauch_pro_einwohner"].idxmin()

min_year = df.loc[min_idx, "jahr"]
min_value = df.loc[min_idx, "verbrauch_pro_einwohner"]

ax.scatter(
    min_year,
    min_value,
    s=120,
    zorder=5
)

ax.annotate(
    f"Historisches Tief\n{min_year}: {min_value}",
    xy=(min_year, min_value),
    xytext=(2020, 1200),
    arrowprops=dict(
        arrowstyle="->",
        lw=2
    ),
    fontsize=12
)

# =====================================================
# TITLES
# =====================================================
ax.set_title(
    "Konsumverbrauch von Zigaretten in Deutschland\n1965–2025",
    fontsize=22,
    pad=25,
    weight="bold"
)

ax.set_xlabel(
    "Jahr",
    fontsize=14
)

ax.set_ylabel(
    "Zigaretten pro Einwohner",
    fontsize=14
)

# =====================================================
# LEGEND
# =====================================================
ax.legend(
    fontsize=12,
    loc="upper right"
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
# SHOW
# =====================================================
plt.tight_layout()
output_path = os.path.join(script_dir, "zigaretten_trend.png")

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("Grafik gespeichert:", output_path)