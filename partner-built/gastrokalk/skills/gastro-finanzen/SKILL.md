---
name: gastro-finanzen
description: >
  Buchhaltung und Finanzmanagement fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Kassenbuch fuehren", "Tagesabschluss machen", "MwSt berechnen", "Umsatz auswerten",
  "Kosten analysieren", "Budget planen", "Gewinn berechnen" oder aehnliches fragt.
  Auch bei Fragen zu Mehrwertsteuer, Buchhaltung oder Finanzplanung.
metadata:
  version: "1.0.0"
  agent: "finance"
  plan: "STARTER"
---

# Buchhaltung & Finanzmanagement

Unterstuetze Gastro-Profis bei der Finanzverwaltung und Buchhaltung.

## Verfuegbare Tools

- `list_kassenbuch` — Kassenbuch-Eintraege mit Einnahmen, Ausgaben und Saldo (filterbar nach Zeitraum)
- `get_dashboard_summary` — Tages-KPIs und aktuelle Reservierungen
- `get_foodcost_overview` — Food-Cost Analyse: Durchschnitt, Top Profitable, Kategorien
- `get_profitabilitaet` — Profitabilitaets-Analyse: Gewinn nach Rezept und Kategorie
- `list_pos_orders` — POS-Bestellungen mit Umsatz und Zahlungsart

## Workflow: Tagesabschluss

1. **POS-Bestellungen pruefen** — `list_pos_orders` mit Datum heute
2. **Kassenbuch abrufen** — `list_kassenbuch` fuer heutige Ein-/Ausgaben
3. **Soll/Ist vergleichen** — POS-Umsatz vs. Kassenbuch-Einnahmen
4. **Differenzen dokumentieren** — Toleranz: +/- CHF 5.00

## Workflow: Monatsauswertung

1. **Kassenbuch laden** — `list_kassenbuch` mit `von`/`bis` auf Monatszeitraum
2. **Food-Cost pruefen** — `get_foodcost_overview` fuer Durchschnitt und Problemrezepte
3. **Profitabilitaet** — `get_profitabilitaet` fuer Gewinn pro Gericht und Kategorie
4. **Kennzahlen berechnen** — Prime Cost, Betriebsergebnis, RevPASH

## MwSt-Saetze DACH

| Land | Normal | Reduziert | Gastro-Besonderheit |
|------|--------|-----------|---------------------|
| CH | 8.1% | 2.6% | Take-away 2.6%, Vor-Ort 8.1% |
| DE | 19% | 7% | Speisen vor Ort 19%, Take-away 7% |
| AT | 20% | 10% | Speisen/Getraenke 10% (Gastro-Satz) |

## Kennzahlen

| Kennzahl | Zielwert |
|----------|----------|
| Food Cost | 25-35% vom Umsatz |
| Personalkosten | 30-35% vom Umsatz |
| Prime Cost (Food + Personal) | max. 65% |
| Betriebsergebnis | min. 10-15% |
