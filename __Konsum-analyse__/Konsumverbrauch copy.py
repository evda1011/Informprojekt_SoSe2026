import pandas as pd
import matplotlib.pyplot as plt

# Download CSV
df = pd.read_csv("konsumverbrauch_zigaretten_clean.csv")

# График
plt.figure(figsize=(14, 7))

plt.plot(
    df["jahr"],
    df["verbrauch_pro_einwohner"],
    linewidth=3,
    marker="o"
)

plt.title("Pro-Kopf-Verbrauch von Zigaretten in Deutschland")
plt.xlabel("Jahr")
plt.ylabel("Zigaretten pro Einwohner")

plt.grid(True)
plt.show()