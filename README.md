# Tabak und Nikotin in Deutschland – Zahlen, Daten, Fakten

**Informprojekt SoSe 2026**

| Gruppe | Studierende 1 | Studierende 2 |
|--------|---------------|---------------|
| `Echo` | `Samantha Abt` | `Daria Evdokimova` |

---

## Projektübersicht

Das Repository enthält eine vollständige Analyse des Zigarettenkonsums in Deutschland. Das Projekt gliedert sich in fünf Teilanalysen:

- **Konsum** – Rauchverhalten nach Alter und Geschlecht
- **Bundesländer** – regionale Unterschiede im Rauchverhalten
- **Marktanalyse** – Preisentwicklung, Steuerbelastung und Konsumtrends
- **Preisprognose** – zukünftige Entwicklung von Preis und Konsum
- **Sterblichkeit** – tabakassoziierte Todesfälle und Erkrankungen

---

## Zielsetzung

Ziel des Projekts ist es, den Zigarettenkonsum in Deutschland anhand verschiedener Datensätze zu analysieren und Zusammenhänge zwischen Konsumverhalten, Preisentwicklung und gesundheitlichen Folgen zu identifizieren.

Die zentralen Forschungsfragen lauten:

1. Wie unterscheidet sich der Tabakkonsum in Deutschland nach Altersgruppen, Geschlecht und regionaler Verteilung?
2. Inwiefern beeinflussen Preisentwicklung, Marktveränderungen und steuerliche Belastungen den Zigarettenkonsum?
3. Welche gesundheitlichen Auswirkungen des Rauchens werden in den Daten sichtbar, insbesondere im Zusammenhang mit Sterblichkeit?

---

## Projektstruktur

```
Informprojekt_SoSe2026/
│
├── grafiken/                           # Zentrale Grafiken
├── src/                                # Hilfsfunktionen und Utilities
├── Konsum_nach_Geschlecht_und_Alter/   # Analyse nach Alter und Geschlecht
├── Rauchverhalten_nach_Bundeslaendern/ # Regionale Unterschiede
├── Marktanalyse/                       # Preis-, Steuer- und Konsumdaten
├── Preisprognose/                      # Prognosen zu Preis und Konsum
├── Sterblichkeit/                      # Gesundheitliche Folgen
│
├── Performance_Final.ipynb             # Hauptnotebook mit allen Analysen
├── pyproject.toml
├── poetry.lock
├── README.md
└── .gitignore
```

---

## Datengrundlage

Die Analyse basiert auf mehreren Datensätzen zum Tabakkonsum in Deutschland:

- Rauchverhalten nach Alter, Geschlecht und Bundesländern
- Preisentwicklung und Tabaksteuer
- Pro-Kopf-Verbrauch von Zigaretten
- Tabakassoziierte Sterblichkeit und Erkrankungen

Die Datenaufbereitung erfolgte mit **pandas** und umfasste:
- Einlesen und Bereinigen der Datensätze
- Vereinheitlichung der Spaltennamen
- Entfernen fehlender Werte
- Zusammenführung von Preis- und Konsumdaten über das Merkmal *Jahr*

---

## Beispielgrafiken

Nachfolgend ein erster Eindruck der Visualisierungen:

![Preisentwicklung](grafiken/Preis_und_Steuern.png)
![Sterblichkeit](grafiken/Sterblichkeit.png)

---

## Installation und Ausführung

### Voraussetzungen

- Python 3.10 oder höher
- Poetry (empfohlen)

### Installation

```bash
git clone <Repository-URL>
cd Informprojekt_SoSe2026
poetry install
```

### Ausführung

```bash
jupyter notebook
```

Öffnen Sie anschließend die Datei `Performance_Final.ipynb`.

---

## Ergebnisse im Überblick

### 1. Konsumverhalten
- Männer rauchen häufiger als Frauen (2024)
- Junge Erwachsene (18–24) zeigen die höchste Raucherquote

### 2. Regionale Unterschiede
- Höchster Raucheranteil in Mecklenburg-Vorpommern
- Niedrigster Raucheranteil im Saarland

### 3. Markt und Preisentwicklung
- Kontinuierlicher Rückgang des Pro-Kopf-Konsums seit den 1960er Jahren
- Steigende Zigarettenpreise durch Tabaksteuererhöhungen
- Zwischen Preisentwicklung und Konsum zeigt sich ein negativer Zusammenhang

### 4. Gesundheitliche Folgen
- Tabakassoziierte Sterblichkeit betrifft überwiegend Erkrankungen der Atemwege und des Herz-Kreislauf-Systems
- Deutliche geschlechtsspezifische Unterschiede in der Sterblichkeit

---

## Verwendete Technologien

- **Python** – Datenverarbeitung und Analyse
- **Jupyter Notebook** – interaktive Entwicklung
- **pandas** – Datenaufbereitung
- **numpy** – numerische Berechnungen
- **matplotlib** – Visualisierung
- **seaborn** – statistische Grafiken
- **Poetry** – Abhängigkeitsmanagement

---

## Autorinnen

- Samantha Abt
- Daria Evdokimova

*Gruppe Echo – Informprojekt SoSe 2026*

---

## Lizenz

Dieses Repository wurde im Rahmen des Informprojekts (SoSe 2026) erstellt und dient ausschließlich zu Lehr- und Studienzwecken. Die verwendeten Datensätze unterliegen den jeweiligen Lizenzbedingungen der Quellen.