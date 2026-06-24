import pandas as pd
import numpy as np

# ANALYSE DER RAUCHBEDINGTEN STERBLICHKEIT IN DEUTSCHLAND
# Kombination beider Skripte in einem vollständigen Workflow

print("ANALYSE DER RAUCHBEDINGTEN STERBLICHKEIT IN DEUTSCHLAND")
print("Deutschland, 2024")


# 1. KONFIGURATION & PFADE

from pathlib import Path

# Findung des aktuellen Skriptverzeichnisses
script_dir = Path(__file__).resolve().parent
file_path = script_dir / 'data' / 'statistischer-bericht-todesursachen-2120400247005.xlsx'


# Smoking Attributable Fractions (WHO / CDC / Literatur)
SAF = {
    'C34': 0.88,      # Lungenkrebs
    'J44': 0.80,      # COPD
    'I20-I25': 0.25,  # Ischämische Herzkrankheiten
    'I60-I69': 0.18,  # Schlaganfall
    'C15': 0.70,      # Speiseröhrenkrebs
    'C25': 0.25,      # Bauchspeicheldrüsenkrebs
}

# ICD-Codes und Bezeichnungen
causes = {
    'C34': 'Lungenkrebs',
    'J44': 'COPD (chronische Bronchitis/Emphysem)',
    'I21': 'Akuter Myokardinfarkt',
    'I20-I25': 'Ischämische Herzkrankheiten',
    'I60-I69': 'Schlaganfall',
    'C15': 'Speiseröhrenkrebs',
    'C25': 'Bauchspeicheldrüsenkrebs',
}

# 2. DATEN LADEN

# Теперь передаем объект Path вместо обычной строки
df_total = pd.read_excel(file_path, sheet_name='23211-b09', header=0)
df_male = pd.read_excel(file_path, sheet_name='23211-b10', header=0)
df_female = pd.read_excel(file_path, sheet_name='23211-b11', header=0)
df_time = pd.read_excel(file_path, sheet_name='23211-b01', header=0)

print(f"\nDaten erfolgreich geladen aus: {file_path.name}")

# 3. HILFSFUNKTIONEN

def find_row_by_icd(df, code):
    """
    Sucht Zeile anhand eines ICD-Codes oder Präfixes.
    """
    for idx, row in df.iterrows():
        cell = str(row.iloc[0]).strip()

        if (
            cell.startswith(code)
            or cell.startswith(f"{code}:")
        ):
            return row

    return None


def get_deaths_by_icd(df, code):
    """
    Gibt die Todesfälle für einen ICD-Code zurück.
    """
    row = find_row_by_icd(df, code)

    if row is not None:
        return pd.to_numeric(row.iloc[1], errors='coerce')

    return 0


# 4. GESAMTWERTE

total_deaths = get_deaths_by_icd(df_total, 'A00-U85')
total_cancer = get_deaths_by_icd(df_total, 'C00-C97')

print(f"\nGesamtzahl aller Todesfälle: {total_deaths:,.0f}")
print(f"Gesamtzahl Krebstodesfälle:  {total_cancer:,.0f}")

# 5. DETAILANALYSE DER TODESURSACHEN

results = []

for code, name in causes.items():

    deaths_total = get_deaths_by_icd(df_total, code)
    deaths_male = get_deaths_by_icd(df_male, code)
    deaths_female = get_deaths_by_icd(df_female, code)

    saf = SAF.get(code, 0.0)

    attributable = deaths_total * saf

    results.append({
        'ICD': code,
        'Ursache': name,
        'Todesfälle_Gesamt': deaths_total,
        'Todesfälle_Männer': deaths_male,
        'Todesfälle_Frauen': deaths_female,
        'SAF': saf,
        'Zugeschriebene_Todesfälle': round(attributable),
        'Anteil_Gesamt_%': round((deaths_total / total_deaths) * 100, 2)
        if total_deaths else 0,
        'Anteil_Krebs_%': round((deaths_total / total_cancer) * 100, 2)
        if (
            total_cancer
            and 'krebs' in name.lower()
        ) else np.nan
    })

df_results = pd.DataFrame(results)

# Sortieren
df_results = df_results.sort_values(
    by='Todesfälle_Gesamt',
    ascending=False
)

# 6. TABELLENAUSGABE

print("\n" + "=" * 110)
print("DETAILLIERTE ANALYSE DER RAUCHBEDINGTEN TODESURSACHEN")
print("=" * 110)

print(
    f"{'Ursache':35} | "
    f"{'Gesamt':>12} | "
    f"{'Männer':>10} | "
    f"{'Frauen':>10} | "
    f"{'SAF':>6} | "
    f"{'Rauchen zurechenbar':>20}"
)

print("-" * 110)

for _, row in df_results.iterrows():

    print(
        f"{row['Ursache']:35} | "
        f"{row['Todesfälle_Gesamt']:>12,.0f} | "
        f"{row['Todesfälle_Männer']:>10,.0f} | "
        f"{row['Todesfälle_Frauen']:>10,.0f} | "
        f"{row['SAF']:>6.2f} | "
        f"{row['Zugeschriebene_Todesfälle']:>20,.0f}"
    )

print("-" * 110)

print( f"{'ALLE TODESFÄLLE':35} | " f"{total_deaths:>12,.0f}")

print( f"{'ALLE KREBSTODESFÄLLE':35} | " f"{total_cancer:>12,.0f}")

print("=" * 110)

# 7. KURZANALYSE / WICHTIGSTE FAKTEN

print("\n" + "=" * 90)
print("WICHTIGSTE FAKTEN AUF EINEN BLICK")
print("=" * 90)

# Einzelwerte
lung_cancer = get_deaths_by_icd(df_total, 'C34')
copd = get_deaths_by_icd(df_total, 'J44')
esophageal_cancer = get_deaths_by_icd(df_total, 'C15')
pancreatic_cancer = get_deaths_by_icd(df_total, 'C25')

ihd = get_deaths_by_icd(df_total, 'I20-I25')
stroke = get_deaths_by_icd(df_total, 'I60-I69')
ami = get_deaths_by_icd(df_total, 'I21')

# Direkte Folgen
direct_smoking = (lung_cancer+ copd + esophageal_cancer + pancreatic_cancer)

print("\n 1 DIREKT MIT RAUCHEN VERBUNDENE ERKRANKUNGEN")
print(f"   • Lungenkrebs:                 {lung_cancer:>10,.0f}")
print(f"   • COPD:                        {copd:>10,.0f}")
print(f"   • Speiseröhrenkrebs:           {esophageal_cancer:>10,.0f}")
print(f"   • Bauchspeicheldrüsenkrebs:    {pancreatic_cancer:>10,.0f}")

print("   ─────────────────────────────────────────────")
print(
    f"   GESAMT:                       {direct_smoking:>10,.0f} "
    f"({direct_smoking / total_deaths * 100:.1f}% aller Todesfälle)"
)

# Herz-Kreislauf
print("\n 2 HERZ-KREISLAUF-ERKRANKUNGEN")
print(f"   • Ischämische Herzkrankheiten: {ihd:>10,.0f}")
print(f"   • Akuter Myokardinfarkt:       {ami:>10,.0f}")
print(f"   • Schlaganfall:                {stroke:>10,.0f}")

print("   ─────────────────────────────────────────────")
print(
    f"   GESAMT:                       {ihd + stroke:>10,.0f} "
    f"({(ihd + stroke) / total_deaths * 100:.1f}% aller Todesfälle)"
)

# Gesamt
total_smoking_related = direct_smoking + ihd + stroke

print("\n 3 GESAMTERGEBNIS")
print(
    f"   Mit Rauchen direkt oder indirekt verbundene Todesfälle:"
)

print(f"   {total_smoking_related:,.0f} Menschen")

print(
    f"   Das entspricht "
    f"{total_smoking_related / total_deaths * 100:.1f}% "
    f"aller Todesfälle in Deutschland."
)

# Kontext
print("\n 4 KONTEXT")
print(
    f"   • Alle Krebstodesfälle:           {total_cancer:,.0f}"
)

print(f"   • Anteil Lungenkrebs an Krebs:    "
    f"{lung_cancer / total_cancer * 100:.1f}%"
)

print(
    f"   • Ischämische Herzkrankheiten > "
    f"alle Krebsarten zusammen: "
    f"{'JA' if ihd > total_cancer else 'NEIN'}"
)

print(
    f"   • Ischämische Herzkrankheiten > "
    f"Lungenkrebs + COPD: "
    f"{'JA' if ihd > lung_cancer + copd else 'NEIN'}"
)

# 8. RAUCHEN ZURECHENBARE TODESFÄLLE (SAF-MODELL)

total_attributable = df_results[
    'Zugeschriebene_Todesfälle'
].sum()

print("\n" + "=" * 90)
print("RAUCHEN ZURECHENBARE TODESFÄLLE (SAF-MODELL)")
print("=" * 90)

print(
    f"\nGeschätzte Todesfälle direkt durch Rauchen "
    f"(epidemiologische Attribution):"
)

print(f"{total_attributable:,.0f} Todesfälle")

print(
    f"Das entspricht "
    f"{total_attributable / total_deaths * 100:.1f}% "
    f"aller Todesfälle."
)