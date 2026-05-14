import sys 
from pathlib import Path ## grafiken anzeigen und save


projekt_ordner = Path(__file__).resolve().parents[1]
sys.path.append(str(projekt_ordner))



output_ordner = Path("Preis_vs_Konsum") / "grafiken"
output_ordner.mkdir(parents=True, exist_ok=True)




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from src.plot_utils import plot_linie, plot_zwei_achsen, plot_scatter_trend


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



#####---------------------GRAFIK 1-------------------

# Diagramm: Entwicklung im Zeitverlauf mit zwei y-Achsen
plot_zwei_achsen(
    df,
    "year",
    "price_cent",
    "consumption_per_capita",
    "Entwicklung von Zigarettenpreis und Pro-Kopf-Verbrauch bis 2025",
    "Jahr",
    "Preis pro Zigarette [Cent]",
    "Pro-Kopf-Verbrauch [Stück]",
    output_ordner / "entwicklung_preis_konsum.png"
)




##--------------GRAFIK2

# Scatterplot mit Trendlinie
m, b = plot_scatter_trend(
    df,
    "price_cent",
    "consumption_per_capita",
    "Zusammenhang zwischen Preis und Konsum bis 2025",
    "Preis pro Zigarette [Cent]",
    "Pro-Kopf-Verbrauch [Stück]",
    output_ordner / "zusammenhang_preis_konsum.png"
)






