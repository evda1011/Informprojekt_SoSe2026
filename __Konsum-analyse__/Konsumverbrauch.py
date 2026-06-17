import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ==================== ЗАГРУЗКА ДАННЫХ ====================
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "konsumverbrauch_zigaretten_deutschland.csv")

df = pd.read_csv(
    csv_path,
    sep=";",
    decimal=",",      # важно для немецких чисел
    encoding="utf-8",
    engine="python"
)

print("Колонки:", df.columns.tolist())
print("\nПервые 10 строк:")
print(df.head(10))

# ===================== ОЧИСТКА ДАННЫХ =====================
# Преобразуем строки в числа (на всякий случай)
numeric_cols = ["verbrauch_pro_einwohner_quelle1", 
                "verbrauch_pro_einwohner_quelle2",
                "zigarettenverbrauch_mrd",
                "praevalenz_gesamt_pct",
                "praevalenz_maenner_pct",
                "praevalenz_frauen_pct"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print("\nПосле очистки:")
print(df[["jahr", "verbrauch_pro_einwohner_quelle2"]].head(15))

# ===================== ГРАФИК =====================
plot_df = df[["jahr", "verbrauch_pro_einwohner_quelle2"]].dropna()

if len(plot_df) > 1:
    plt.figure(figsize=(13, 7))
    
    plt.plot(plot_df["jahr"], plot_df["verbrauch_pro_einwohner_quelle2"], 
             marker="o", linestyle="-", color="tab:blue", linewidth=2.8, 
             label="Verbrauch pro Einwohner")

    # Тренд
    z = np.polyfit(plot_df["jahr"], plot_df["verbrauch_pro_einwohner_quelle2"], 1)
    p = np.poly1d(z)
    plt.plot(plot_df["jahr"], p(plot_df["jahr"]), "r--", linewidth=2, label="Линейный тренд")

    plt.title("Pro-Kopf-Verbrauch von Zigaretten in Deutschland\n(1965–2025)", fontsize=15, pad=20)
    plt.xlabel("Jahr", fontsize=12)
    plt.ylabel("Zigaretten pro Einwohner", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=11)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Недостаточно данных для графика")