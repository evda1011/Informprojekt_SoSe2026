import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv("konsumverbrauch_zigaretten_deutschland.csv")

# Берём данные потребления на душу населения
plot_df = df[["jahr", "verbrauch_pro_einwohner_quelle2"]].dropna()

# Построение графика
plt.figure(figsize=(12, 6))

plt.plot(
    plot_df["jahr"],
    plot_df["verbrauch_pro_einwohner_quelle2"],
    marker="o"
)

# Подписи
plt.title("Pro-Kopf-Verbrauch von Zigaretten in Deutschland")
plt.xlabel("Jahr")
plt.ylabel("Zigaretten pro Einwohner")

# Сетка
plt.grid(True)

# Показать график
plt.show()