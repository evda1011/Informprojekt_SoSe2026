# Daten zur Tabakprävention in Deutschland (2000-2023 + Plan bis 2026)
# chronologische Ordnung

tabak_daten = [
    # 2000
    (2000, "Werbeverbot", "Verbot des Sponsorings von Rundfunksendungen"),
    
    # 2002
    (2002, "Steuererhöhung", "deutliche Tabaksteuererhöhungen"),
    (2002, "Warnhinweise", "Vergrößerung des Warnhinweises auf Rauchtabakerzeugnissen"),
    
    # 2003
    (2003, "Steuererhöhung", "deutliche Tabaksteuererhöhungen (2003–2005)"),
    (2003, "Jugendschutz", "Verkaufsverbot an und Rauchverbot für unter 16-Jährige"),
    (2003, "Werbeverbot", "Verbot der Kinowerbung vor 18 Uhr"),
    
    # 2004
    (2004, "Nichtraucherschutz", "Nichtraucherschutz am Arbeitsplatz"),
    (2004, "Jugendschutz", "Verbot von Gratisproben, Mindestgröße 17 Zigaretten pro Packung"),
    
    # 2006
    (2006, "Werbeverbot", "Werbeverbot in Print und Internet sowie Sponsoringverbote"),
    
    # 2007
    (2007, "Nichtraucherschutz", "Bundes- und Landesnichtraucherschutzgesetze (2007/2008)"),
    (2007, "Jugendschutz", "Verkaufsverbot an und Rauchverbot für unter 18-Jährige"),
    
    # 2009
    (2009, "Jugendschutz", "Verkaufsverbot an Automaten für unter 18-Jährige"),
    (2009, "Werbeverbot", "Verbot von Produktplatzierung im Fernsehen"),
    
    # 2010
    (2010, "Nichtraucherschutz", "Bayern: umfassendes Nichtraucherschutzgesetz"),
    
    # 2011
    (2011, "Steuererhöhung", "geringfügige Tabaksteuererhöhungen (2011–2015)"),
    (2011, "Nichtraucherschutz", "Saarland: umfassendes Nichtraucherschutzgesetz"),
    
    # 2013
    (2013, "Nichtraucherschutz", "Nordrhein-Westfalen: umfassendes Nichtraucherschutzgesetz"),
    
    # 2016
    (2016, "Produktregulierung", "Bildliche Warnhinweise; Regelung von Inhaltsstoffen und Emissionswerten; Regulierung von E-Zigaretten"),
    (2016, "Jugendschutz", "Verkaufsverbot an und Nutzungsverbot für E-Zigaretten für unter 18-Jährige; Verkaufsverbot über Versandhandel an unter 18-Jährige"),
    
    # 2019
    (2019, "Produktregulierung", "Rückverfolgungssystem für Tabakerzeugnisse"),
    
    # 2021
    (2021, "Werbeverbot", "schrittweises Verbot der Außenwerbung für Tabak (2022), Tabakerhitzer (2023) und E-Zigaretten (2024)"),
    
    # 2022 (Rückblick und Ausblick)
    (2022, "Steuererhöhung", "moderate Tabaksteuererhöhungen und Einführung einer neuen spezifischen Steuer auf Tabakerhitzer und E-Zigaretten-Liquids (2022–2026)"),
    
    # 2023
    (2023, "Produktregulierung", "Aromenverbot für tabakhaltige Sticks für Tabakerhitzer"),
]

# Ausgabe in chronologischer Reihenfolge
for jahr, kategorie, beschreibung in tabak_daten:
    print(f"{jahr}: {kategorie} – {beschreibung}")