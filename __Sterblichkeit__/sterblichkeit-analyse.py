import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================================================
# ПУТЬ К ФАЙЛУ И ПАПКЕ ДЛЯ СОХРАНЕНИЯ
# =========================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = 'statistischer-bericht-todesursachen-2120400247005.xlsx'
file_path = os.path.join(script_dir, file_name)

print(f"Suche Datei: {file_path}")
if not os.path.exists(file_path):
    print(f"FEHLER: Datei nicht gefunden!")
    exit(1)

# =========================================================
# НАСТРОЙКИ
# =========================================================
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

print("\n=== ANALYSE DER RAUCHBEDINGTEN STERBLICHKEIT IN DEUTSCHLAND ===\n")

# =========================================================
# SAF + Ursachen
# =========================================================
SAF = {'C34': 0.88, 'J44': 0.80, 'I20-I25': 0.25, 
       'I60-I69': 0.18, 'C15': 0.70, 'C25': 0.25}

causes_names = {
    'C34': 'Lungenkrebs', 'J44': 'COPD',
    'I20-I25': 'Ischämische Herzkrankheiten',
    'I60-I69': 'Schlaganfall',
    'C15': 'Speiseröhrenkrebs',
    'C25': 'Bauchspeicheldrüsenkrebs'
}

# =========================================================
# DATEN LADEN
# =========================================================
df_total = pd.read_excel(file_path, sheet_name='23211-b09', header=3)
df_male = pd.read_excel(file_path, sheet_name='23211-b10', header=3)
df_female = pd.read_excel(file_path, sheet_name='23211-b11', header=3)

def get_deaths_by_icd(df, icd_prefix):
    col0 = df.iloc[:, 0].astype(str).str.strip()
    mask = col0.str.startswith(icd_prefix)
    if mask.any():
        return int(df.loc[mask, df.columns[1]].iloc[0])
    return 0

total_deaths = get_deaths_by_icd(df_total, 'A00-U85')
print(f"Gesamte Sterbefälle 2024: {total_deaths:,}\n")

# =========================================================
# ANALYSE
# =========================================================
results = []
for code, name in causes_names.items():
    dt = get_deaths_by_icd(df_total, code)
    dm = get_deaths_by_icd(df_male, code)
    df_ = get_deaths_by_icd(df_female, code)
    saf = SAF.get(code, 0.0)
    results.append({
        'Ursache': name,
        'ICD': code,
        'Todesfälle_Gesamt': dt,
        'Todesfälle_Männer': dm,
        'Todesfälle_Frauen': df_,
        'SAF': saf,
        'Zugeschriebene_Todesfälle': round(dt * saf),
        'Anteil_Gesamt_%': round(dt / total_deaths * 100, 2) if total_deaths > 0 else 0,
    })

df_results = pd.DataFrame(results)
print(df_results.round(2).to_string(index=False))

# =========================================================
# FARBPALETTE
# =========================================================
colors = sns.color_palette("Reds_d", len(df_results))

# =========================================================
# ВИЗУАЛИЗАЦИЯ
# =========================================================
print("\nErstelle Diagramme...")

# 1. Bar Chart
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=df_results, x='Zugeschriebene_Todesfälle', y='Ursache', 
            palette=colors, ax=ax1)
ax1.set_title('Zugeschriebene Sterbefälle durch Rauchen (2024)')
for i, v in enumerate(df_results['Zugeschriebene_Todesfälle']):
    ax1.text(v + 200, i, f'{v:,}', va='center')
plt.tight_layout()
plt.savefig(os.path.join(script_dir, '01_Zugeschriebene_Sterblichkeit.png'), dpi=300)
plt.close(fig1)

# 2. Geschlecht
df_gender = df_results[['Ursache','Todesfälle_Männer','Todesfälle_Frauen']].melt(
    id_vars='Ursache', var_name='Geschlecht', value_name='Todesfälle')

fig2, ax2 = plt.subplots(figsize=(12, 7))
sns.barplot(data=df_gender, x='Ursache', y='Todesfälle', hue='Geschlecht', 
            palette=['#1f77b4', '#ff7f0e'], ax=ax2)
ax2.set_title('Rauchbedingte Sterbefälle nach Geschlecht (2024)')
ax2.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(script_dir, '02_Sterblichkeit_nach_Geschlecht.png'), dpi=300)
plt.close(fig2)

# 3. PIE CHART — максимально плотный
fig3, ax3 = plt.subplots(figsize=(11, 9))
wedges, texts, autotexts = ax3.pie(
    df_results['Zugeschriebene_Todesfälle'],
    labels=None,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    pctdistance=0.78,
    wedgeprops=dict(linewidth=0.3, edgecolor='white')
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

ax3.legend(wedges, df_results['Ursache'], title="Ursache", 
           loc="center left", bbox_to_anchor=(1.05, 0.5))

ax3.set_title('Struktur der rauchbedingten Sterblichkeit (2024)', fontsize=14)
ax3.set_aspect('equal')
plt.tight_layout()
plt.savefig(os.path.join(script_dir, '03_Struktur_Rauchbedingte_Sterblichkeit.png'), dpi=300, facecolor='white')
plt.close(fig3)

# 4. Gesamtanalyse
fig4, axes = plt.subplots(2, 2, figsize=(18, 14))
total_attributable = df_results['Zugeschriebene_Todesfälle'].sum()
percentage = total_attributable / total_deaths * 100

sns.barplot(data=df_results, x='Zugeschriebene_Todesfälle', y='Ursache', 
            palette=colors, ax=axes[0,0])

sns.barplot(data=df_gender, x='Ursache', y='Todesfälle', hue='Geschlecht', 
            palette=['#1f77b4', '#ff7f0e'], ax=axes[0,1])
axes[0,1].tick_params(axis='x', rotation=45)

w2, t2, at2 = axes[1,0].pie(
    df_results['Zugeschriebene_Todesfälle'],
    labels=None,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    pctdistance=0.78,
    wedgeprops=dict(linewidth=0.3, edgecolor='white')
)
for autotext in at2:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

axes[1,0].legend(w2, df_results['Ursache'], title="Ursache", 
                 loc="center left", bbox_to_anchor=(1.05, 0.5))

text = f'''Gesamtergebnis:\n{total_attributable:,} zugeschriebene Todesfälle\n({percentage:.1f}% aller Sterbefälle)\n\nGesamte Sterbefälle 2024: {total_deaths:,}'''
axes[1,1].text(0.5, 0.5, text, ha='center', va='center', fontsize=13,
               bbox=dict(boxstyle="round,pad=1.5", facecolor="lightblue"))
axes[1,1].axis('off')

plt.suptitle('Analyse der rauchbedingten Sterblichkeit in Deutschland 2024', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(script_dir, '04_Gesamtanalyse_Rauchbedingte_Sterblichkeit.png'), dpi=300, facecolor='white')
plt.show()

print("\nAlle Diagramme wurden gespeichert в папке __Sterblichkeit__!")
print("• 01_Zugeschriebene_Sterblichkeit.png")
print("• 02_Sterblichkeit_nach_Geschlecht.png")
print("• 03_Struktur_Rauchbedingte_Sterblichkeit.png")
print("• 04_Gesamtanalyse_Rauchbedingte_Sterblichkeit.png")
print("\n=== ANALYSE ERFOLGREICH ABGESCHLOSSEN ===")