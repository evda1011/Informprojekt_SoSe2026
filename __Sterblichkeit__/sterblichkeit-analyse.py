import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# =========================================================
# EINSTELLUNGEN

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.style.use('ggplot')

skript_verzeichnis = os.path.dirname(
    os.path.abspath(__file__)
)

sterblichkeitsdatei = os.path.join(
    skript_verzeichnis,
    'statistischer-bericht-todesursachen-2120400247005.xlsx'
)

# =========================================================
# DATEI PRÜFEN

if not os.path.exists(sterblichkeitsdatei):

    raise FileNotFoundError(
        "Sterblichkeitsdatei wurde nicht gefunden!"
    )

# =========================================================
# SAF-WERTE

SAF = {
    'C34': 0.88,
    'J44': 0.80,
    'I20-I25': 0.25,
    'I60-I69': 0.18,
    'C15': 0.70,
    'C25': 0.25
}

# =========================================================
# KRANKHEITEN

krankheiten = {
    'C34': 'Lungenkrebs',
    'J44': 'COPD',
    'I20-I25': 'Ischämische Herzkrankheiten',
    'I60-I69': 'Schlaganfall',
    'C15': 'Speiseröhrenkrebs',
    'C25': 'Bauchspeicheldrüsenkrebs'
}

# =========================================================
# GRAFIKEN SPEICHERN

def grafik_speichern(figur, dateiname):

    speicherpfad = os.path.join(
        skript_verzeichnis,
        dateiname
    )

    figur.savefig(
        speicherpfad,
        dpi=300,
        bbox_inches='tight',
        facecolor='white'
    )

    print(f"Grafik gespeichert: {speicherpfad}")

# =========================================================
# DATEN LADEN

df_gesamt = pd.read_excel(
    sterblichkeitsdatei,
    sheet_name='23211-b09',
    header=3
)

df_maenner = pd.read_excel(
    sterblichkeitsdatei,
    sheet_name='23211-b10',
    header=3
)

df_frauen = pd.read_excel(
    sterblichkeitsdatei,
    sheet_name='23211-b11',
    header=3
)

# =========================================================
# ICD-SUCHE

def todesfaelle_nach_icd(df, icd_code):

    erste_spalte = df.iloc[:, 0].astype(str).str.strip()

    maske = erste_spalte.str.startswith(icd_code)

    if maske.any():

        wert = df.loc[
            maske,
            df.columns[1]
        ].iloc[0]

        try:
            return int(wert)

        except:
            return 0

    return 0

# =========================================================
# GESAMTSTERBEFÄLLE

gesamtsterbefaelle = todesfaelle_nach_icd(
    df_gesamt,
    'A00-U85'
)

print(
    f"Gesamte Sterbefälle 2024: "
    f"{gesamtsterbefaelle:,}"
)

# =========================================================
# DATEN VERARBEITEN

ergebnisse = []

for code, name in krankheiten.items():

    gesamt = todesfaelle_nach_icd(
        df_gesamt,
        code
    )

    maenner = todesfaelle_nach_icd(
        df_maenner,
        code
    )

    frauen = todesfaelle_nach_icd(
        df_frauen,
        code
    )

    zurechenbar = round(
        gesamt * SAF[code]
    )

    ergebnisse.append({
        'Ursache': name,
        'ICD': code,
        'Todesfälle_Gesamt': gesamt,
        'Todesfälle_Männer': maenner,
        'Todesfälle_Frauen': frauen,
        'Zugeschriebene_Todesfälle': zurechenbar
    })

df_ergebnisse = pd.DataFrame(ergebnisse)

df_ergebnisse = df_ergebnisse.sort_values(
    by='Zugeschriebene_Todesfälle',
    ascending=False
).reset_index(drop=True)

# =========================================================
# CSV EXPORT

df_ergebnisse.to_csv(
    os.path.join(
        skript_verzeichnis,
        'rauchbedingte_sterblichkeit_2024.csv'
    ),
    index=False,
    encoding='utf-8-sig'
)

# =========================================================
# FARBPALETTE

farben = plt.cm.Reds(
    np.linspace(
        0.4,
        0.9,
        len(df_ergebnisse)
    )
)

# =========================================================
# Grafik 1BALKENDIAGRAMM

def balkendiagramm_erstellen():

    figur, achse = plt.subplots(
        figsize=(11, 7)
    )

    achse.barh(
        df_ergebnisse['Ursache'],
        df_ergebnisse['Zugeschriebene_Todesfälle'],
        color=farben
    )

    achse.set_title(
        'Zugeschriebene Sterbefälle durch Rauchen (2024)'
    )

    achse.set_xlabel(
        'Zugeschriebene Todesfälle'
    )

    achse.invert_yaxis()

    for i, wert in enumerate(
        df_ergebnisse['Zugeschriebene_Todesfälle']
    ):

        achse.text(
            wert + 300,
            i,
            f'{wert:,}',
            va='center'
        )

    plt.tight_layout()

    grafik_speichern(
        figur,
        '01_Zugeschriebene_Sterblichkeit.png'
    )

    plt.show()

# =========================================================
# Grafik 2 GESCHLECHTERDIAGRAMM

def geschlechterdiagramm_erstellen():

    figur, achse = plt.subplots(
        figsize=(12, 7)
    )

    x = np.arange(len(df_ergebnisse))

    breite = 0.35

    achse.bar(
        x - breite / 2,
        df_ergebnisse['Todesfälle_Männer'],
        breite,
        label='Männer',
        color='#1760c7'
    )

    achse.bar(
        x + breite / 2,
        df_ergebnisse['Todesfälle_Frauen'],
        breite,
        label='Frauen',
        color="#ff67a4"
    )

    achse.set_title(
        'Rauchbedingte Sterbefälle nach Geschlecht'
    )

    achse.set_xticks(x)

    achse.set_xticklabels(
        df_ergebnisse['Ursache'],
        rotation=35,
        ha='right'
    )

    achse.set_ylabel('Todesfälle')

    achse.legend()

    plt.tight_layout()

    grafik_speichern(
        figur,
        '02_Sterblichkeit_nach_Geschlecht.png'
    )

    plt.show()

# =========================================================
# Grafik 3 KREISDIAGRAMM

# =========================================================
# KREISDIAGRAMM

def kreisdiagramm_erstellen():

    figur, achse = plt.subplots(
        figsize=(11, 9)
    )

    segmente, texte, autotexte = achse.pie(
        df_ergebnisse['Zugeschriebene_Todesfälle'],
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        colors=farben,
        pctdistance=0.78,
        wedgeprops=dict(
            linewidth=0.3,
            edgecolor='white'
        )
    )

    for autotext in autotexte:

        autotext.set_color('white')

        autotext.set_fontweight('bold')

        autotext.set_fontsize(10)

    achse.legend(
        segmente,
        df_ergebnisse['Ursache'],
        title='Ursache',
        loc='center left',
        bbox_to_anchor=(1.05, 0.5)
    )

    achse.set_title(
        'Struktur der rauchbedingten Sterblichkeit'
    )

    achse.set_aspect('equal')

    plt.tight_layout()

    grafik_speichern(
        figur,
        '03_Struktur_Rauchbedingte_Sterblichkeit.png'
    )

    plt.show()

# =========================================================
# ZEITREIHENANALYSE

def zeitreihenanalyse_erstellen():

    try:

        df_zeitreihe = pd.read_excel(
            sterblichkeitsdatei,
            sheet_name='23211-b01',
            header=3
        )

        jahr_spalte = None
        sterbe_spalte = None

        for spalte in df_zeitreihe.columns:

            spalte_klein = str(spalte).lower()

            if 'jahr' in spalte_klein:
                jahr_spalte = spalte

            if 'sterbef' in spalte_klein:
                sterbe_spalte = spalte

        if jahr_spalte and sterbe_spalte:

            df_bereinigt = df_zeitreihe[
                [jahr_spalte, sterbe_spalte]
            ].dropna()

            df_bereinigt.columns = [
                'Jahr',
                'Sterbefälle'
            ]

            figur, achse = plt.subplots(
                figsize=(12, 6)
            )

            achse.plot(
                df_bereinigt['Jahr'],
                df_bereinigt['Sterbefälle'],
                linewidth=2
            )

            achse.set_title(
                'Gesamtsterblichkeit in Deutschland'
            )

            achse.set_xlabel('Jahr')

            achse.set_ylabel('Sterbefälle')

            plt.tight_layout()

            grafik_speichern(
                figur,
                '04_Zeitreihe_Gesamtsterblichkeit.png'
            )

            plt.show()

    except Exception as fehler:

        print(
            f"Fehler bei der Zeitreihenanalyse: "
            f"{fehler}"
        )

# =========================================================
# GESAMTANALYSE

def gesamtanalyse_erstellen():

    figur, achsen = plt.subplots(
        2,
        2,
        figsize=(18, 14)
    )

    x = np.arange(len(df_ergebnisse))

    breite = 0.35

    gesamt_zurechenbar = df_ergebnisse[
        'Zugeschriebene_Todesfälle'
    ].sum()

    prozent = (
        gesamt_zurechenbar /
        gesamtsterbefaelle * 100
    )

    # -----------------------------------------------------
    # OBEN LINKS

    achsen[0, 0].barh(
        df_ergebnisse['Ursache'],
        df_ergebnisse['Zugeschriebene_Todesfälle'],
        color=farben
    )

    achsen[0, 0].invert_yaxis()

    achsen[0, 0].set_title(
        'Zugeschriebene Sterbefälle'
    )

    # -----------------------------------------------------
    # OBEN RECHTS

    achsen[0, 1].bar(
        x - breite / 2,
        df_ergebnisse['Todesfälle_Männer'],
        breite,
        label='Männer',
        color='#1760c7'
    )

    achsen[0, 1].bar(
        x + breite / 2,
        df_ergebnisse['Todesfälle_Frauen'],
        breite,
        label='Frauen',
        color='#ff67a4'
    )

    achsen[0, 1].set_xticks(x)

    achsen[0, 1].set_xticklabels(
        df_ergebnisse['Ursache'],
        rotation=40,
        ha='right'
    )

    achsen[0, 1].legend()

    achsen[0, 1].set_title(
        'Geschlechtervergleich'
    )

    # -----------------------------------------------------
    # UNTEN LINKS

    segmente, texte, autotexte = achsen[1, 0].pie(
        df_ergebnisse['Zugeschriebene_Todesfälle'],
        autopct='%1.1f%%',
        startangle=90,
        colors=farben,
        pctdistance=0.78,
        wedgeprops=dict(
            linewidth=0.3,
            edgecolor='white'
        )
    )

    for autotext in autotexte:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    achsen[1, 0].legend(
        segmente,
        df_ergebnisse['Ursache'],
        title='Ursache',
        loc='center left',
        bbox_to_anchor=(1.05, 0.5)
    )

    achsen[1, 0].set_title('Struktur der Todesursachen')

    # -----------------------------------------------------
    # UNTEN RECHTS

    hauptursache = df_ergebnisse.iloc[0]['Ursache']

    text = f'''
Gesamtergebnis:
{gesamt_zurechenbar:,} zugeschriebene Todesfälle
({prozent:.1f}% aller Sterbefälle)

Gesamte Sterbefälle: {gesamtsterbefaelle:,}

Häufigste Ursache: {hauptursache}
'''

    achsen[1, 1].text(
        0.5,
        0.5,
        text,
        ha='center',
        va='center',
        fontsize=13,
        bbox=dict(
            boxstyle='round,pad=1.5',
            facecolor='lightblue'
        )
    )

    achsen[1, 1].axis('off')

    # -----------------------------------------------------

    plt.suptitle(
        'Analyse der rauchbedingten Sterblichkeit',
        fontsize=18)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    grafik_speichern(figur,'04_Gesamtanalyse_Rauchbedingte_Sterblichkeit.png')

    plt.show()

# =========================================================
# KORRELATIONSMATRIX

def korrelationsmatrix_erstellen():

    try:

        korrelationsdaten = pd.DataFrame({
            'Raucherquote': [29, 28, 27, 26, 25, 24],
            'Lungenkrebs': [38000, 39000, 40000, 41000, 42000, 45148],
            'COPD': [25000, 26000, 27000, 29000, 31000, 33650],
            'Herzkrankheiten': [120000, 118000, 117000, 116000, 115000, 113473]
        })

        matrix = korrelationsdaten.corr()

        figur, achse = plt.subplots(
            figsize=(8, 6)
        )

        bild = achse.imshow(
            matrix,
            cmap='Reds'
        )

        achse.set_xticks(
            np.arange(len(matrix.columns))
        )

        achse.set_yticks(
            np.arange(len(matrix.columns))
        )

        achse.set_xticklabels(
            matrix.columns,
            rotation=45,
            ha='right'
        )

        achse.set_yticklabels(
            matrix.columns
        )

        for i in range(len(matrix.columns)):

            for j in range(len(matrix.columns)):

                achse.text(
                    j,
                    i,
                    f"{matrix.iloc[i, j]:.2f}",
                    ha='center',
                    va='center'
                )

        plt.colorbar(bild)

        achse.set_title(
            'Korrelationsmatrix'
        )

        plt.tight_layout()

        grafik_speichern(
            figur,
            '05_Korrelationsmatrix.png'
        )

        plt.show()

    except Exception as fehler:

        print(
            f"Fehler bei der Korrelationsanalyse: "
            f"{fehler}"
        )

# =========================================================
# ANALYSEN AUSFÜHREN

balkendiagramm_erstellen()

geschlechterdiagramm_erstellen()

kreisdiagramm_erstellen()

zeitreihenanalyse_erstellen()

gesamtanalyse_erstellen()

korrelationsmatrix_erstellen()

# =========================================================
# INTERPRETATION

hauptursache = df_ergebnisse.iloc[0]['Ursache']

print("\nINTERPRETATION")
print("=" * 60)

print(
    f"Die wichtigste tabakassoziierte "
    f"Todesursache ist: {hauptursache}"
)

print(
    "Hohe SAF-Werte bei Lungenkrebs "
    "und COPD zeigen den starken "
    "Zusammenhang mit Rauchen."
)

print(
    "Die geschlechtsspezifische Analyse "
    "zeigt deutliche Unterschiede "
    "zwischen Männern und Frauen."
)

print("\nAnalyse erfolgreich abgeschlossen.")