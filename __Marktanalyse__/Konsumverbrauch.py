import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ============================================
# Weg zu Datei
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "data", "konsumverbrauch_zigaretten.csv")
df = pd.read_csv(csv_path)

# ============================================
# Graf 
plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(df["jahr"], df["verbrauch_pro_einwohner"], linewidth=3.5, marker="o", 
        markersize=7, label="Zigarettenkonsum pro Einwohner")

ax.fill_between(df["jahr"], df["verbrauch_pro_einwohner"], alpha=0.15)

# Trendlinie
z = np.polyfit(df["jahr"], df["verbrauch_pro_einwohner"], 1)
p = np.poly1d(z)

ax.plot(df["jahr"], p(df["jahr"]), linestyle="--", linewidth=2.5, label="Trendlinie")

# Max & Min Value
max_idx = df["verbrauch_pro_einwohner"].idxmax()
min_idx = df["verbrauch_pro_einwohner"].idxmin()

ax.scatter(df.loc[max_idx, "jahr"], df.loc[max_idx, "verbrauch_pro_einwohner"], s=140, color="red", zorder=5)
ax.scatter(df.loc[min_idx, "jahr"], df.loc[min_idx, "verbrauch_pro_einwohner"], s=140, color="darkblue", zorder=5)


max_year = df.loc[max_idx, "jahr"]
max_value = df.loc[max_idx, "verbrauch_pro_einwohner"]
ax.annotate(
    f"Historisches Hoch\n{max_year}: {max_value}",
    xy=(max_year, max_value),
    xytext=(1973, 2830),
    arrowprops=dict(arrowstyle="->",lw=2),
    fontsize=12)


min_year = df.loc[min_idx, "jahr"]
min_value = df.loc[min_idx, "verbrauch_pro_einwohner"]
ax.annotate(
    f"Historisches Tief\n{min_year}: {min_value}",
    xy=(min_year, min_value),
    xytext=(2020, 1200),
    arrowprops=dict(arrowstyle="->", lw=2),
    fontsize=12)

ax.set_title("Konsumverbrauch von Zigaretten in Deutschland\n1965–2025", 
             fontsize=22, pad=30, weight="bold")
ax.set_xlabel("Jahr", fontsize=14)
ax.set_ylabel("Zigaretten pro Einwohner", fontsize=14)

ax.legend(fontsize=12, loc="upper right")
plt.xticks(rotation=45)
plt.tight_layout()

# Speicher
grafiken_ordner = os.path.join(script_dir, "Grafiken")
os.makedirs(grafiken_ordner, exist_ok=True)

output_path = os.path.join(grafiken_ordner, "zigaretten_trend.png")

plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"{output_path}")
plt.close()