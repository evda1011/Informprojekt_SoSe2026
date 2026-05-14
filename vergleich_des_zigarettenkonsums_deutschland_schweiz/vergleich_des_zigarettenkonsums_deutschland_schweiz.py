import sys
from pathlib import Path

projekt_ordner = Path(__file__).resolve().parents[1]
sys.path.append(str(projekt_ordner))

import pandas as pd

from src.plot_utils import plot_balken_gruppiert


deu_datei = r"vergleich_des_zigarettenkonsums_deutschland_schweiz\DEU.xlsx"
schw_datei = r"vergleich_des_zigarettenkonsums_deutschland_schweiz\SCHW.xlsx"

output_ordner = Path("vergleich_des_zigarettenkonsums_deutschland_schweiz") / "grafiken"
output_ordner.mkdir(parents=True, exist_ok=True)


deu = pd.read_excel(deu_datei)
schw = pd.read_excel(schw_datei)


comparison = pd.DataFrame({
    "Altersgruppe": deu["Altersgruppe"],
    "Deutschland": deu["DE_Insgesamt"],
    "Schweiz": schw["CH_Insgesamt"]
})




print(comparison)


#ANALYSE DE DATEN WICHTIG-JEDE THEMAS MUSS ETWAS SO HABEN UNSERE ARBEIT IST DATEN ANALYSIEREN NICHT NUR GRAFIKEN MACHEN
# Die Daten werden mit einer Schleife analysiert. Dabei vergleicht eine if-else-Bedingung den
#Zigarettenkonsum zwischen Deutschland und der Schweiz für jede Altersgruppe.
#IST EIN bisschen unnötig ich weiss, aber Matthias will schleife, if else, def, classen sehen 

for index, row in comparison.iterrows():

    if row["Deutschland"] > row["Schweiz"]:

        print(
            f"{row['Altersgruppe']}: "
            "Deutschland hat höheren Konsum."
        )

    else:

        print(
            f"{row['Altersgruppe']}: "
            "Schweiz hat höheren Konsum."
        )



plot_balken_gruppiert(
    comparison,
    "Altersgruppe",
    ["Deutschland", "Schweiz"],
    "Zigarettenkonsum nach Altersgruppen: Deutschland vs. Schweiz",
    "Altersgruppe",
    "Anteil [%]",
    output_ordner / "deutschland_schweiz_altersgruppen.png"
)







#grafik 2: kreisdiagram ingesamt


from src.plot_utils import plot_kreis

# Durchschnitt berechnen
de_mean = comparison["Deutschland"].mean()
ch_mean = comparison["Schweiz"].mean()

# Daten für Kreisdiagramm
labels = ["Deutschland", "Schweiz"]

werte = [de_mean, ch_mean]

# Farben das ist nur design
farben = ["#0E6A64", "#5DC6D0"]

# Kreisdiagramm erstellen
plot_kreis(
    labels,
    werte,
    "Vergleich Deutschland vs. Schweiz insgesamt",
    farben,
    output_ordner / "kreisdiagramm_insgesamt.png"
)


