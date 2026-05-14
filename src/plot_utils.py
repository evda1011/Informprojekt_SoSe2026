import matplotlib.pyplot as plt


def plot_linie(df, x_spalte, y_spalte, titel, x_label, y_label):
    plt.figure(figsize=(10, 5))
    plt.plot(df[x_spalte], df[y_spalte], marker="o")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(titel)
    plt.tight_layout()
    plt.show()


###art grafik--------------

def plot_balken(df, x_spalte, y_spalte, titel, x_label, y_label):
    plt.figure(figsize=(10, 5))
    plt.bar(df[x_spalte], df[y_spalte])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(titel)
    plt.tight_layout()
    plt.show()




###art grafik--------------

def plot_zwei_achsen(df, x_spalte, y1_spalte, y2_spalte, titel, x_label, y1_label, y2_label, speichern_unter=None):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    linie1 = ax1.plot(
        df[x_spalte],
        df[y1_spalte],
        marker="o",
        color="tab:red",
        label=y1_label
    )

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color="tab:red")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    ax2 = ax1.twinx()

    linie2 = ax2.plot(
        df[x_spalte],
        df[y2_spalte],
        marker="o",
        color="tab:blue",
        label=y2_label
    )

    ax2.set_ylabel(y2_label, color="tab:blue")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    linien = linie1 + linie2
    labels = [linie.get_label() for linie in linien]
    ax1.legend(linien, labels, loc="upper right")

    plt.title(titel)
    fig.tight_layout()

    if speichern_unter is not None:
        plt.savefig(speichern_unter, dpi=300)

    plt.show()


###art grafik--------------

def plot_scatter_trend(df, x_spalte, y_spalte, titel, x_label, y_label, speichern_unter=None):
    import numpy as np

    plt.figure(figsize=(8, 5))

    plt.scatter(
        df[x_spalte],
        df[y_spalte],
        label="Datenpunkte"
    )

    m, b = np.polyfit(df[x_spalte], df[y_spalte], 1)

    plt.plot(
        df[x_spalte],
        m * df[x_spalte] + b,
        linestyle="--",
        color="red",
        label="Trendlinie"
    )

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(titel)
    plt.legend()
    plt.tight_layout()

    if speichern_unter is not None:
        plt.savefig(speichern_unter, dpi=300)

    plt.show()

    return m, b


###art grafik--------------

def plot_kreis(
    labels,
    werte,
    titel,
    farben=None,
    speichern_unter=None
):

    plt.figure(figsize=(7, 7))

    plt.pie(
        werte,
        labels=labels,
        autopct="%1.1f%%",
        colors=farben
    )

    plt.title(titel)

    plt.tight_layout()

    if speichern_unter is not None:
        plt.savefig(speichern_unter, dpi=300)

    plt.show()



###art grafik--------------

def plot_balken_gruppiert(df, x_spalte, y_spalten, titel, x_label, y_label, speichern_unter=None):
    ax = df.plot(
        x=x_spalte,
        y=y_spalten,
        kind="bar",
        figsize=(10, 5)
    )

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(titel)

    plt.xticks(rotation=0)
    plt.tight_layout()

    if speichern_unter is not None:
        plt.savefig(speichern_unter, dpi=300)

    plt.show()
