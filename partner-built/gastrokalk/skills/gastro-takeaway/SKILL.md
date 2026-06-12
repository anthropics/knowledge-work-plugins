---
name: gastro-takeaway
description: >
  Takeaway und Bestelleingang fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Takeaway Bestellung", "Bestelleingang", "Lieferung verwalten", "Takeaway Menuekarte",
  "Abholbestellung", "Online-Bestellungen" oder aehnliches fragt.
metadata:
  version: "1.0.0"
  agent: "takeaway"
  plan: "STARTER"
---

# Takeaway & Bestelleingang

Unterstuetze Gastro-Profis beim Management von Takeaway- und Lieferbestellungen.

## Verfuegbare Tools

- `list_takeaway_items` — Takeaway-Artikel mit Preisen und Verfuegbarkeit (aktiv/inaktiv)
- `list_takeaway_orders` — Takeaway-Bestellungen (filterbar nach Status)
- `get_takeaway_stats` — Takeaway-Statistiken (Umsatz, Bestellungen, Trends)

## Workflow: Bestellungen verwalten

1. **Offene Bestellungen** — `list_takeaway_orders` mit Status-Filter
2. **Priorisieren** — Nach Abholzeit sortieren
3. **Statistik** — `get_takeaway_stats` fuer Tages-/Wochenuebersicht

## Workflow: Takeaway-Angebot pruefen

1. **Artikel laden** — `list_takeaway_items` fuer alle verfuegbaren Artikel
2. **Verfuegbarkeit** — Inaktive Artikel identifizieren
3. **Preise pruefen** — Verpackungskosten und MwSt-Unterschied beruecksichtigen

## Takeaway-spezifische Kalkulation

Zusaetzliche Kosten einrechnen:
- Verpackungsmaterial: CHF 0.50-2.00 pro Bestellung
- Lieferkosten: bei eigener Lieferung
- Plattformgebuehren: 15-30% bei Drittanbietern
- Reduzierter MwSt-Satz: CH 2.6%, DE 7% (Take-away statt Vor-Ort)

## Menueoptimierung fuer Takeaway

Nur Gerichte die transportfaehig sind:
- Keine empfindlichen Saucen oder zeitkritische Praesentation
- Verpackungsfreundliche Portionsgroessen
- Haltbarkeit waehrend Transport (min. 20 Min)
