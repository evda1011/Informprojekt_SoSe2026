import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# =========================================================
# DATEIPFAD

script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    script_dir,
    'statistischer-bericht-todesursachen-2120400247005.xlsx'
)

if not os.path.exists(file_path):
    print("Datei nicht gefunden!")
    exit()

# =========================================================
# STYLE

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.style.use('ggplot')

print("\nANALYSE DER RAUCHBEDINGTEN STERBLICHKEIT\n")

# =========================================================
# SAF + KRANKHEITEN

SAF = {
    'C34': 0.88,
    'J44': 0.80,
    'I20-I25': 0.25,
    'I60-I69': 0.18,
    'C15': 0.70,
    'C25': 0.25
}

causes = {
    'C34': 'Lungenkrebs',
    'J44': 'COPD',
    'I20-I25': 'Ischämische Herzkrankheiten',
    'I60-I69': 'Schlaganfall',
    'C15': 'Speiseröhrenkrebs',
    'C25': 'Bauchspeicheldrüsenkrebs'
}

# =========================================================
# DATEN LADEN

df_total = pd.read_excel(file_path, sheet_name='23211-b09', header=3)
df_male = pd.read_excel(file_path, sheet_name='23211-b10', header=3)
df_female = pd.read_excel(file_path, sheet_name='23211-b11', header=3)

# =========================================================
# FUNKTION

def get_deaths(df, icd):

    col = df.iloc[:, 0].astype(str).str.strip()

    mask = col.str.startswith(icd)

    if mask.any():

        value = df.loc[mask, df.columns[1]].iloc[0]

        try:
            return int(value)
        except:
            return 0

    return 0

# =========================================================
# GESAMTSTERBEFÄLLE

total_deaths = get_deaths(df_total, 'A00-U85')

print(f"Gesamte Sterbefälle: {total_deaths:,}")

# =========================================================
# ZEITREIHE

try:

    df_time = pd.read_excel(
        file_path,
        sheet_name='23211-b01',
        header=3
    )

    year_col = None
    death_col = None

    for col in df_time.columns:

        name = str(col).lower()

        if 'jahr' in name:
            year_col = col

        if 'sterbef' in name:
            death_col = col

    if year_col and death_col:

        df_time = df_time[[year_col, death_col]].dropna()

        fig, ax = plt.subplots(figsize=(11, 5))

        ax.plot(
            df_time[year_col],
            df_time[death_col],
            linewidth=2
        )

        ax.set_title('Gesamtsterblichkeit in Deutschland')
        ax.set_xlabel('Jahr')
        ax.set_ylabel('Sterbefälle')

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                script_dir,
                '05_Zeitreihe_Gesamtsterblichkeit.png'
            ),
            dpi=300
        )

        plt.close(fig)

except Exception as e:

    print(f"Zeitreihenfehler: {e}")

# =========================================================
# ANALYSE

results = []

for code, name in causes.items():

    total = get_deaths(df_total, code)
    male = get_deaths(df_male, code)
    female = get_deaths(df_female, code)

    attributable = round(total * SAF[code])

    results.append({
        'Ursache': name,
        'ICD': code,
        'Gesamt': total,
        'Männer': male,
        'Frauen': female,
        'SAF': SAF[code],
        'Rauchbedingt': attributable
    })

df_results = pd.DataFrame(results)

df_results = df_results.sort_values(
    by='Rauchbedingt',
    ascending=False
).reset_index(drop=True)

print("\nDETAILLIERTE ANALYSE\n")

print(df_results.to_string(index=False))

# =========================================================
# CSV EXPORT

df_results.to_csv(
    os.path.join(
        script_dir,
        'rauchbedingte_sterblichkeit_2024.csv'
    ),
    index=False,
    encoding='utf-8-sig'
)

# =========================================================
# FARBEN

colors = plt.cm.Reds(
    np.linspace(0.4, 0.9, len(df_results))
)

# =========================================================
# GRAFIK 1

fig1, ax1 = plt.subplots(figsize=(11, 6))

ax1.barh(
    df_results['Ursache'],
    df_results['Rauchbedingt'],
    color=colors
)

ax1.invert_yaxis()

ax1.set_title(
    'Zugeschriebene Sterbefälle durch Rauchen'
)

for i, v in enumerate(df_results['Rauchbedingt']):

    ax1.text(
        v + 300,
        i,
        f'{v:,}',
        va='center'
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        script_dir,
        '01_Zugeschriebene_Sterblichkeit.png'
    ),
    dpi=300
)

plt.close(fig1)

# =========================================================
# GRAFIK 2

fig2, ax2 = plt.subplots(figsize=(12, 6))

x = np.arange(len(df_results))
width = 0.35

ax2.bar(
    x - width / 2,
    df_results['Männer'],
    width,
    label='Männer',
    color='#1f77b4'
)

ax2.bar(
    x + width / 2,
    df_results['Frauen'],
    width,
    label='Frauen',
    color='#ff7f0e'
)

ax2.set_xticks(x)

ax2.set_xticklabels(
    df_results['Ursache'],
    rotation=35,
    ha='right'
)

ax2.set_title(
    'Sterbefälle nach Geschlecht'
)

ax2.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        script_dir,
        '02_Sterblichkeit_nach_Geschlecht.png'
    ),
    dpi=300
)

plt.close(fig2)

# =========================================================
# GRAFIK 3

fig3, ax3 = plt.subplots(figsize=(11, 9))

wedges, texts, autotexts = ax3.pie(
    df_results['Rauchbedingt'],
    labels=None,
    autopct=lambda p: f'{p:.1f}%' if p > 6 else '',
    startangle=90,
    colors=colors,
    pctdistance=0.78,
    wedgeprops=dict(
        linewidth=0.3,
        edgecolor='white'
    )
)

for autotext in autotexts:

    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

ax3.legend(
    wedges,
    df_results['Ursache'],
    title="Ursache",
    loc="center left",
    bbox_to_anchor=(1.05, 0.5)
)

ax3.set_title(
    'Struktur der Todesursachen'
)

ax3.set_aspect('equal')

plt.tight_layout()

plt.savefig(
    os.path.join(
        script_dir,
        '03_Struktur_Rauchbedingte_Sterblichkeit.png'
    ),
    dpi=300,
    facecolor='white'
)

plt.close(fig3)

# =========================================================
# GESAMTANALYSE

fig4, axes = plt.subplots(
    2,
    2,
    figsize=(18, 14)
)

total_attr = df_results['Rauchbedingt'].sum()

percentage = total_attr / total_deaths * 100

# ---------------------------------------------------------

axes[0, 0].barh(
    df_results['Ursache'],
    df_results['Rauchbedingt'],
    color=colors
)

axes[0, 0].invert_yaxis()

axes[0, 0].set_title(
    'Zugeschriebene Sterbefälle'
)

# ---------------------------------------------------------

axes[0, 1].bar(
    x - width / 2,
    df_results['Männer'],
    width,
    label='Männer',
    color='#1f77b4'
)

axes[0, 1].bar(
    x + width / 2,
    df_results['Frauen'],
    width,
    label='Frauen',
    color='#ff7f0e'
)

axes[0, 1].set_xticks(x)

axes[0, 1].set_xticklabels(
    df_results['Ursache'],
    rotation=35,
    ha='right'
)

axes[0, 1].legend()

axes[0, 1].set_title(
    'Geschlechtervergleich'
)

# ---------------------------------------------------------

w2, t2, at2 = axes[1, 0].pie(
    df_results['Rauchbedingt'],
    labels=None,
    autopct=lambda p: f'{p:.1f}%' if p > 6 else '',
    startangle=90,
    colors=colors,
    pctdistance=0.82,
    wedgeprops=dict(
        linewidth=0.3,
        edgecolor='white'
    )
)

for autotext in at2:

    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

axes[1, 0].legend(
    w2,
    df_results['Ursache'],
    title="Ursache",
    loc="center left",
    bbox_to_anchor=(1.1, 0.5)
)

axes[1, 0].set_title(
    'Struktur der Todesursachen'
)

# ---------------------------------------------------------

top_cause = df_results.iloc[0]['Ursache']

text = f'''
Gesamtergebnis:

{total_attr:,} zugeschriebene Todesfälle

({percentage:.1f}% aller Sterbefälle)

Gesamte Sterbefälle:
{total_deaths:,}

Häufigste Ursache:
{top_cause}
'''

axes[1, 1].text(
    0.5,
    0.42,
    text,
    ha='center',
    va='center',
    fontsize=13,
    bbox=dict(
        boxstyle="round,pad=1.5",
        facecolor="lightblue"
    )
)

axes[1, 1].axis('off')

# =========================================================

plt.suptitle(
    'Analyse der rauchbedingten Sterblichkeit in Deutschland 2024',
    fontsize=18
)

plt.subplots_adjust(
    hspace=0.35,
    wspace=0.35
)

plt.savefig(
    os.path.join(
        script_dir,
        '04_Gesamtanalyse_Rauchbedingte_Sterblichkeit.png'
    ),
    dpi=300,
    facecolor='white'
)

# =========================================================
# INTERPRETATION

print("\nINTERPRETATION\n")

print(
    f"Häufigste Ursache: {top_cause}"
)

print(
    "Lungenkrebs und COPD zeigen "
    "eine starke Verbindung zum Rauchen."
)

print(
    "Zwischen Männern und Frauen "
    "bestehen deutliche Unterschiede."
)

# =========================================================

plt.show()

print("\n=== ANALYSE ABGESCHLOSSEN ===")