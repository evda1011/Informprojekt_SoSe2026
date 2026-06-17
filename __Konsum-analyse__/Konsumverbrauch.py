import pandas as pd

df = pd.read_csv("tabakkonsum_de.csv")

print(df.head())

# График потребления сигарет на душу населения
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.plot(df["Jahr"], df["ProKopfVerbrauch_Stueck"], marker="o")
plt.title("Pro-Kopf-Verbrauch von Zigaretten in Deutschland")
plt.xlabel("Jahr")
plt.ylabel("Zigaretten pro Einwohner")
plt.grid(True)
plt.show()