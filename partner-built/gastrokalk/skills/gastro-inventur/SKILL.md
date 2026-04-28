---
name: gastro-inventur
description: >
  Lagerverwaltung und Inventur fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Inventur machen", "Lagerbestand pruefen", "MHD checken", "was laeuft ab", "FIFO pruefen",
  "Bestand aktualisieren", "Lagerwert berechnen" oder aehnliches fragt.
  Auch bei Fragen zu Mindesthaltbarkeit, Lagerorganisation oder Bestandsoptimierung.
metadata:
  version: "1.0.0"
  agent: "inventory"
  plan: "STARTER"
---

# Lagerverwaltung & Inventur

Unterstuetze Gastro-Profis bei der effizienten Lagerverwaltung nach FIFO-Prinzip.

## Verfuegbare Tools

- `list_bestand` — Aktueller Lagerbestand mit Mengen, Werten, Lagerort und MHD
- `get_mhd_kritisch` — Kritische und abgelaufene MHD-Warnungen (ABGELAUFEN/KRITISCH/Warnung)
- `list_inventories` — Alle Inventuren auflisten (Status, Datum, Positionenanzahl)
- `get_inventory_detail` — Inventur-Details mit Soll/Ist-Abweichungen und Gesamtwert

## Workflow: MHD-Check (taeglich empfohlen)

1. **Kritische Artikel pruefen** — `get_mhd_kritisch`
2. **Massnahmen nach Status:**
   - ABGELAUFEN → Sofort entsorgen, dokumentieren (HACCP-Pflicht)
   - KRITISCH (< 3 Tage) → Heute verarbeiten, als Tagesempfehlung einsetzen
   - Warnung (< 7 Tage) → In Menuplanung der naechsten Tage einbeziehen
3. **Gesamtbestand pruefen** — `list_bestand` fuer Lageruebersicht

## Workflow: Inventur durchfuehren

1. **Letzte Inventuren** — `list_inventories` um Historie und Status zu sehen
2. **Details vergleichen** — `get_inventory_detail` fuer Soll/Ist je Position
3. **Abweichungen bewerten:**
   - \> 10% → Schwund pruefen (Diebstahl, Fehlbuchungen, Verderb)
   - 5-10% → Portionskontrolle verschaerfen
   - < 5% → Im gruenen Bereich

## Workflow: Bestand pruefen

1. **Bestand abrufen** — `list_bestand` mit optionalem Suchbegriff oder Lagerort-Filter
2. **Lagerwert berechnen** — Aus den Werten (Menge × Preis) in der Antwort
3. **Nachbestellbedarf** — Niedrige Bestaende identifizieren → weiterleiten an gastro-einkauf

## Richtwerte

| Kennzahl | Zielwert |
|----------|----------|
| Umschlagshaeufigkeit | 12-24x/Jahr (Frischware hoeher) |
| Schwundquote | < 2% des Wareneinsatzes |
| MHD-Verluste | < 1% des Lagerwerts |
| Inventurdifferenz | < 5% Abweichung |
