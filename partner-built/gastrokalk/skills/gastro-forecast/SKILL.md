---
name: gastro-forecast
description: >
  Prognosen und Vorhersagen fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Umsatzprognose", "Gaestezahlen vorhersagen", "wie viel soll ich bestellen",
  "Forecast erstellen", "Feiertage planen", "Saisonprognose", "Wetter Auswirkung" oder
  aehnliches fragt. Auch bei Fragen zu Trends, saisonalen Schwankungen oder Eventplanung.
metadata:
  version: "1.0.0"
  agent: "forecast"
  plan: "PROFESSIONAL"
---

# Prognosen & Forecast

Unterstuetze Gastro-Profis bei datenbasierten Vorhersagen fuer Planung und Einkauf.

## Verfuegbare Tools

- `get_dashboard_summary` — Aktuelles Wetter (Temperatur, Bedingungen) und heutige Reservierungen
- `list_reservations` — Reservierungen fuer kommende Tage/Wochen laden
- `list_kalender` — Events, Feiertage, Lieferungen im Kalender
- `get_foodcost_overview` — Food-Cost Analyse fuer Budget-Prognosen
- `list_pos_orders` — Historische POS-Daten fuer Vergleichszeitraeume
- `get_daily_briefing` — KI-Tagesbriefing mit Metriken und Empfehlungen

## Workflow: Wochenprognose

1. **Reservierungen** — `list_reservations` fuer kommende Woche
2. **Kalender** — `list_kalender` fuer Events und Feiertage
3. **Wetter** — `get_dashboard_summary` fuer aktuelles Wetter (Trend)
4. **Historisch** — `list_pos_orders` fuer Vergleichszeitraum (Vorwoche, Vorjahr)
5. **Prognose erstellen** — Erwartete Gaeste, Umsatz, Einkaufsbedarf

## Prognosefaktoren

| Faktor | Einfluss | Datenquelle |
|--------|----------|-------------|
| Historische Daten | Basis | `list_pos_orders` |
| Reservierungen | Direkt | `list_reservations` |
| Feiertage | +/- 30-50% | `list_kalender` |
| Wetter | +/- 20-40% | `get_dashboard_summary` |
| Events | +10-100% | `list_kalender` |

## Wetter-Impact

| Wetter | Auswirkung | Empfehlung |
|--------|-----------|------------|
| Sonnig >25°C | +20-40% Terrasse | Leichte Gerichte, kalte Getraenke |
| Regen | -10-20% Walk-ins | Comfort Food, warme Getraenke |
| Schnee | Variabel | Skigebiet +, Stadt - |

## Feiertage DACH

Beachte kantonale/regionale Unterschiede:
- CH: 26 Kantone mit unterschiedlichen Feiertagen
- DE: 16 Bundeslaender mit unterschiedlichen Feiertagen
- AT: Einheitliche Feiertage + regionale Braeuche
