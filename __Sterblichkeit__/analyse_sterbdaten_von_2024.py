import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict

# ANALYSE DER RAUCHBEDINGTEN STERBLICHKEIT IN DEUTSCHLAND
print("ANALYSE DER RAUCHBEDINGTEN STERBLICHKEIT IN DEUTSCHLAND")
print("Deutschland, 2024")


# 1. KONFIGURATION & PFADE
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


# Hilfsfunktion

def get_deaths_by_icd(df: pd.DataFrame, code: str) -> int:
    for _, row in df.iterrows():
        cell = str(row.iloc[0]).strip()
        if cell.split(":")[0].strip() == code:
            value = pd.to_numeric(row.iloc[1], errors='coerce')
            return int(value) if pd.notna(value) else 0
    return 0


def calculate_key_metrics(
    df: pd.DataFrame,
    total_deaths: int,
    total_cancer: int
) -> Dict:
    """Berechnet die Schlüsselmetriken für die Kurzzusammenfassung (Abschnitte 1-4)."""
    return {
        'lung_cancer': get_deaths_by_icd(df, 'C34'),
        'copd': get_deaths_by_icd(df, 'J44'),
        'esophageal': get_deaths_by_icd(df, 'C15'),
        'pancreatic': get_deaths_by_icd(df, 'C25'),
        'ihd': get_deaths_by_icd(df, 'I20-I25'),
        'stroke': get_deaths_by_icd(df, 'I60-I69'),
        'ami': get_deaths_by_icd(df, 'I21'),
        'total_deaths': total_deaths,
        'total_cancer': total_cancer,
    }


def print_key_facts(metrics: Dict, title: str = ""):
    """Ausgabe der wichtigsten Faktoren"""
    td = metrics['total_deaths']
    total_cancer = metrics['total_cancer']

    lung_cancer = metrics['lung_cancer']
    copd = metrics['copd']
    esophageal_cancer = metrics['esophageal']
    pancreatic_cancer = metrics['pancreatic']

    ihd = metrics['ihd']
    stroke = metrics['stroke']
    ami = metrics['ami']

    direct_smoking = lung_cancer + copd + esophageal_cancer + pancreatic_cancer

    print(f"WICHTIGSTE FAKTEN AUF EINEN BLICK{title}")

    # 1. Direkte Folgen
    print(f"\n 1 DIREKT MIT RAUCHEN VERBUNDENE ERKRANKUNGEN{title}")
    print(f"   • Lungenkrebs:                 {lung_cancer:>10,.0f}")
    print(f"   • COPD:                        {copd:>10,.0f}")
    print(f"   • Speiseröhrenkrebs:           {esophageal_cancer:>10,.0f}")
    print(f"   • Bauchspeicheldrüsenkrebs:    {pancreatic_cancer:>10,.0f}")

    print("   ─────────────────────────────────────────────")
    print(f"   GESAMT:                       {direct_smoking:>10,.0f} "
          f"({direct_smoking / td * 100:.1f}% aller Todesfälle)")

    # 2. Herz-Kreislauf
    print("\n 2 HERZ-KREISLAUF-ERKRANKUNGEN")
    print(f"   • Ischämische Herzkrankheiten: {ihd:>10,.0f}")
    print(f"   • Akuter Myokardinfarkt:       {ami:>10,.0f}")
    print(f"   • Schlaganfall:                {stroke:>10,.0f}")

    print("   ─────────────────────────────────────────────")
    print(f"   GESAMT:                       {ihd + stroke:>10,.0f} "
          f"({(ihd + stroke) / td * 100:.1f}% aller Todesfälle)")

    # 3. Gesamt
    total_smoking_related = direct_smoking + ihd + stroke

    print("\n 3 GESAMTERGEBNIS")
    print("   Mit Rauchen direkt oder indirekt verbundene Todesfälle:")
    print(f"   {total_smoking_related:,.0f} Menschen")
    print(f"   Das entspricht {total_smoking_related / td * 100:.1f}% "
          f"aller Todesfälle in Deutschland.")

    # 4. Kontext
    print("\n 4 KONTEXT")
    

    if total_cancer > 0:
        print(f"   • Alle Krebstodesfälle:   {total_cancer:,.0f}")
        print(f"   • Anteil Lungenkrebs an Krebs: {lung_cancer / total_cancer * 100:.1f}%")
        print(f"   • Ischämische Herzkrankheiten > alle Krebsarten zusammen: {'JA' if ihd > total_cancer else 'NEIN'}")
        print(f"   • Ischämische Herzkrankheiten > Lungenkrebs + COPD: {'JA' if ihd > (lung_cancer + copd) else 'NEIN'}")


# Hauptausgabe

# 2. DATEN LADEN
df_total = pd.read_excel(file_path, sheet_name='23211-b09', header=2)
df_male = pd.read_excel(file_path, sheet_name='23211-b10', header=2)
df_female = pd.read_excel(file_path, sheet_name='23211-b11', header=2)
df_time = pd.read_excel(file_path, sheet_name='23211-b01', header=2)

print(f"\nDaten erfolgreich geladen aus: {file_path.name}")

# 3. GESAMTWERTE
total_deaths = get_deaths_by_icd(df_total, 'A00-U85')
total_cancer = get_deaths_by_icd(df_total, 'C00-C97')

print(f"\nGesamtzahl aller Todesfälle: {total_deaths:,.0f}")
print(f"Gesamtzahl Krebstodesfälle:  {total_cancer:,.0f}")

# 4. DETAILANALYSE
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
        'Anteil_Gesamt_%': round((deaths_total / total_deaths) * 100, 2) if total_deaths else 0,
        'Anteil_Krebs_%': round((deaths_total / total_cancer) * 100, 2)
        if (total_cancer and 'krebs' in name.lower()) else np.nan
    })

df_results = pd.DataFrame(results).sort_values(by='Todesfälle_Gesamt', ascending=False)

#  5. TABELLENAUSGABE

print("\n" + "=" * 110)
print("DETAILLIERTE ANALYSE DER RAUCHBEDINGTEN TODESURSACHEN")
print("=" * 110)

print(f"{'Ursache':35} | {'Gesamt':>12} | {'Männer':>10} | {'Frauen':>10} | {'SAF':>6} | {'Rauchen zurechenbar':>20}")
print("-" * 110)

for _, row in df_results.iterrows():
    print(f"{row['Ursache']:35} | "
          f"{row['Todesfälle_Gesamt']:>12,.0f} | "
          f"{row['Todesfälle_Männer']:>10,.0f} | "
          f"{row['Todesfälle_Frauen']:>10,.0f} | "
          f"{row['SAF']:>6.2f} | "
          f"{row['Zugeschriebene_Todesfälle']:>20,.0f}")

print("-" * 110)
print(f"{'ALLE TODESFÄLLE':35} | {total_deaths:>12,.0f}")
print(f"{'ALLE KREBSTODESFÄLLE':35} | {total_cancer:>12,.0f}")
print("=" * 110)

# 6. WICHTIGSTE FAKTEN
metrics_total = calculate_key_metrics(df_total, total_deaths, total_cancer)
print_key_facts(metrics_total)

# 7. RAUCHEN ZURECHENBARE TODESFÄLLE (SAF-MODELL)
total_attributable = df_results['Zugeschriebene_Todesfälle'].sum()

print("\n" + "=" * 90)
print("RAUCHEN ZURECHENBARE TODESFÄLLE (SAF-MODELL)")
print("=" * 90)
print(f"\nGeschätzte Todesfälle direkt durch Rauchen (epidemiologische Attribution):")
print(f"{total_attributable:,.0f} Todesfälle")
print(f"Das entspricht {total_attributable / total_deaths * 100:.1f}% aller Todesfälle.")