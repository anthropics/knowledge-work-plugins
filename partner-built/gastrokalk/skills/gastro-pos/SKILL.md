---
name: gastro-pos
description: >
  Kassensystem und Zahlungsabwicklung fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Kasse oeffnen", "Tagesabschluss Kasse", "Zahlung verbuchen", "Rechnung splitten",
  "Trinkgeld verwalten", "Kassenbon", "POS System" oder aehnliches fragt.
metadata:
  version: "1.0.0"
  agent: "pos"
  plan: "STARTER"
---

# Kassensystem & POS

Unterstuetze Gastro-Profis bei der Kassenabwicklung und Zahlungsverwaltung.

## Verfuegbare Tools

- `list_pos_orders` — POS-Bestellungen mit Umsatz, Zahlungsart, Tisch (filterbar nach Status/Datum)
- `list_kassenbuch` — Kassenbuch-Eintraege: Einnahmen, Ausgaben, Saldo
- `get_dashboard_summary` — Tagesueberblick mit Reservierungen

## Workflow: Tagesabschluss

1. **POS-Bestellungen** — `list_pos_orders` mit Datum heute fuer alle Transaktionen
2. **Kassenbuch** — `list_kassenbuch` fuer Bar-Einnahmen und -Ausgaben
3. **Abgleich:**
   - Summe POS-Kartenzahlungen = Kartenterminal-Abrechnung?
   - Summe POS-Barzahlungen = Kassensturz (gezaehltes Bargeld)?
4. **Differenzen** — Toleranz: +/- CHF 5.00, darueber dokumentieren

## Workflow: Umsatzanalyse

1. **Tagesumsatz** — `list_pos_orders` zeigt Gesamtumsatz
2. **Nach Zahlungsart** — Bar vs. Karte vs. andere aufschluesseln
3. **Vergleich** — Mit Vorwoche/Vormonat vergleichen

## Kassenbuch-Pflicht

In der Schweiz und Deutschland besteht Kassenbuchpflicht:
- Alle Bareinnahmen und -ausgaben taeglich dokumentieren
- Lueckenlose, chronologische Aufzeichnung
- Bei Pruefung muss jeder Betrag nachvollziehbar sein

## SumUp-Integration

GastroKalk integriert sich mit SumUp fuer Kartenzahlungen. Transaktionen werden automatisch synchronisiert.
