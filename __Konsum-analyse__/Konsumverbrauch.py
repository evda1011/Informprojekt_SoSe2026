from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Путь к CSV-файлу рядом со скриптом
csv_file = Path(__file__).parent / "tabakkonsum_de.csv"

# Загрузка данных
df = pd.read_csv(csv_file)

print("Первые строки таблицы:")
print(df.head())

# Преобразуем числовые столбцы
numeric_columns = [
    "Jahr",
    "ProKopfVerbrauch_Stueck",
    "Raucherquote_Gesamt",
    "Raucherquote_Maenner",
    "Raucherquote_Frauen",
    "Gesamtverbrauch_Mrd"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# График потребления сигарет на душу населения
plt.figure(figsize=(12, 6))
plt.plot(
    df["Jahr"],
    df["ProKopfVerbrauch_Stueck"],
    marker="o",
    label="Pro-Kopf-Verbrauch"
)

plt.title("Pro-Kopf-Verbrauch von Zigaretten in Deutschland")
plt.xlabel("Jahr")
plt.ylabel("Zigaretten pro Einwohner")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()