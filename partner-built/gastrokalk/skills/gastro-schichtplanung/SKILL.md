---
name: gastro-schichtplanung
description: >
  Schichtoptimierung und Personalplanung fuer die Gastronomie. Verwende diesen Skill wenn
  der Nutzer "Schichten optimieren", "Personalplanung", "Ueber-/Unterbesetzung",
  "Schichttausch", "Personalkosten pro Schicht", "Konflikte im Dienstplan" oder aehnliches
  fragt. Auch bei Fragen zu optimaler Besetzung basierend auf Gaestezahlen.
metadata:
  version: "1.0.0"
  agent: "schichtplanung"
  plan: "STARTER"
---

# Schichtoptimierung

Unterstuetze Gastro-Profis bei der optimalen Schichtbesetzung.

## Verfuegbare Tools

- `list_shifts` — Schichten im Dienstplan (filterbar nach Datum und Mitarbeiter)
- `list_team` — Teammitglieder mit Rollen und Berechtigungen
- `list_reservations` — Reservierungen fuer erwartete Gaestezahl
- `get_dashboard_summary` — Wetter und Tagesueberblick (Auslastungsfaktor)
- `list_kalender` — Kalender-Events (Feiertage, Veranstaltungen, Lieferungen)

## Workflow: Schichtplanung fuer naechste Woche

1. **Reservierungen laden** — `list_reservations` fuer naechste Woche
2. **Events pruefen** — `list_kalender` fuer Feiertage, Veranstaltungen
3. **Bedarf berechnen** — Erwartete Gaeste / Richtwert = benoetigte Mitarbeiter
4. **Schichten laden** — `list_shifts` fuer aktuelle Planung
5. **Team pruefen** — `list_team` fuer verfuegbare Mitarbeiter
6. **Optimieren** — Ueber-/Unterbesetzung korrigieren

## Workflow: Tages-Check

1. **Wetter** — `get_dashboard_summary` — beeinflusst Walk-in-Gaeste
2. **Reservierungen** — `list_reservations` mit Datum heute
3. **Schichten** — `list_shifts` mit Datum heute
4. **Bewerten** — Genuegend Personal fuer die erwartete Auslastung?

## Richtwerte Personalbesetzung

| Bereich | Gaeste pro Mitarbeiter |
|---------|----------------------|
| Service (Casual) | 15-20 |
| Service (Fine Dining) | 8-12 |
| Kueche | 30-40 Covers/Koch |
| Bar | 20-30 |

## Konfliktloesung

Prioritaet bei Schichtkonflikten:
1. Gesetzliche Vorgaben (Ruhezeit, Maximalstunden)
2. Fairness (gleichmaessige Verteilung)
3. Betriebsbeduerfnisse
4. Mitarbeiterwuensche
