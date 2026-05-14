import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from src.plot_utils import plot_linie


# Dateien einlesen
preis_datei = r"Preis_vs_Konsum\_durchschnittlicher-zigarettenpreis-in-deutschland.xlsx"
konsum_datei = r"Preis_vs_Konsum\_pro-kopf-verbrauch-von-zigaretten-in-deutschland.xlsx"


def lade_daten(datei, spaltenname):
    df = pd.read_excel(datei, sheet_name="Daten", header=None)

    df = df[[1, 2]].dropna()
    df.columns = ["year", spaltenname]

    df = df[pd.to_numeric(df["year"], errors="coerce").notna()].copy()
    df["year"] = df["year"].astype(int)
    df[spaltenname] = pd.to_numeric(df[spaltenname], errors="coerce")

    return df.dropna().sort_values("year")


preis_df = lade_daten(preis_datei, "price_cent")
konsum_df = lade_daten(konsum_datei, "consumption_per_capita")

df = pd.merge(preis_df, konsum_df, on="year", how="inner")

print(df)


# Wiederverwendbare Funktion aus src/plot_utils.py
plot_linie(
    df,
    "year",
    "price_cent",
    "Entwicklung des Zigarettenpreises",
    "Jahr",
    "Preis pro Zigarette [Cent]"
)


# Dictionary mit Erklärungen/Einheiten
einheiten = {
    "price_cent": "Preis pro Zigarette in Cent",
    "consumption_per_capita": "Pro-Kopf-Verbrauch in Stück"
}

for spalte, beschreibung in einheiten.items():
    print(spalte, "=", beschreibung)


# Daten filtern mit df[df["year"] == jahr]
jahr = 2025
daten_jahr = df[df["year"] == jahr]

if not daten_jahr.empty:
    preis = daten_jahr["price_cent"].iloc[0]
    konsum = daten_jahr["consumption_per_capita"].iloc[0]

    print(f"Im Jahr {jahr} lag der Preis bei {preis} Cent.")
    print(f"Der Pro-Kopf-Verbrauch lag bei {konsum} Zigaretten.")
else:
    print("Für dieses Jahr liegen keine Daten vor.")


# Vergleich mit Schleife: Entwicklung über die Jahre
for spalte in ["price_cent", "consumption_per_capita"]:
    erster_wert = df[spalte].iloc[0]
    letzter_wert = df[spalte].iloc[-1]

    veraenderung = ((letzter_wert / erster_wert) - 1) * 100

    print(f"{einheiten[spalte]}: Veränderung von {veraenderung:.1f} %")


# Korrelation berechnen
korrelation = df["price_cent"].corr(df["consumption_per_capita"])

if korrelation < 0:
    print(f"Die Korrelation beträgt {korrelation:.3f}.")
    print("Es besteht ein negativer Zusammenhang: Wenn der Preis steigt, sinkt der Konsum tendenziell.")
else:
    print(f"Die Korrelation beträgt {korrelation:.3f}.")
    print("Es besteht kein negativer Zusammenhang.")


# Diagramm: Entwicklung im Zeitverlauf mit zwei y-Achsen
fig, ax1 = plt.subplots(figsize=(10, 5))

linie1 = ax1.plot(
    df["year"],
    df["price_cent"],
    marker="o",
    color="tab:red",
    label="Preis pro Zigarette [Cent]"
)

ax1.set_xlabel("Jahr")
ax1.set_ylabel("Preis pro Zigarette [Cent]", color="tab:red")
ax1.tick_params(axis="y", labelcolor="tab:red")

ax2 = ax1.twinx()

linie2 = ax2.plot(
    df["year"],
    df["consumption_per_capita"],
    marker="o",
    color="tab:blue",
    label="Pro-Kopf-Verbrauch [Stück]"
)

ax2.set_ylabel("Pro-Kopf-Verbrauch [Stück]", color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")

linien = linie1 + linie2
labels = [linie.get_label() for linie in linien]
ax1.legend(linien, labels, loc="upper right")

plt.title("Entwicklung von Zigarettenpreis und Pro-Kopf-Verbrauch")
fig.tight_layout()
plt.show()


# Scatterplot mit Trendlinie
plt.figure(figsize=(8, 5))

plt.scatter(
    df["price_cent"],
    df["consumption_per_capita"],
    label="Datenpunkte"
)

m, b = np.polyfit(df["price_cent"], df["consumption_per_capita"], 1)

plt.plot(
    df["price_cent"],
    m * df["price_cent"] + b,
    linestyle="--",
    color="red",
    label="Trendlinie"
)

plt.xlabel("Preis pro Zigarette [Cent]")
plt.ylabel("Pro-Kopf-Verbrauch [Stück]")
plt.title("Zusammenhang zwischen Preis und Konsum")
plt.legend()
plt.tight_layout()
plt.show()


# Einfache Prognose als zusätzliche Analyse
zukunft_preise = [40, 45, 50]

for preis in zukunft_preise:
    prognose_konsum = m * preis + b

    if prognose_konsum < 0:
        prognose_konsum = 0

    print(f"Bei einem Preis von {preis} Cent wird ein Konsum von ca. {prognose_konsum:.0f} Zigaretten pro Kopf prognostiziert.")
