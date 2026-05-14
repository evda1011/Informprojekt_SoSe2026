import matplotlib.pyplot as plt


def plot_linie(df, x_spalte, y_spalte, titel, x_label, y_label):
    plt.figure(figsize=(10, 5))
    plt.plot(df[x_spalte], df[y_spalte], marker="o")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(titel)
    plt.tight_layout()
    plt.show()


def plot_balken(df, x_spalte, y_spalte, titel, x_label, y_label):
    plt.figure(figsize=(10, 5))
    plt.bar(df[x_spalte], df[y_spalte])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(titel)
    plt.tight_layout()
    plt.show()


def plot_kreis(labels, werte, titel):
    plt.figure(figsize=(7, 7))
    plt.pie(werte, labels=labels, autopct="%1.1f%%")
    plt.title(titel)
    plt.tight_layout()
    plt.show()
