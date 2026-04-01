---
name: gastro-forecast
description: >
  Prognosen und Vorhersagen fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Umsatzprognose", "Gaestezahlen vorhersagen", "wie viel soll ich bestellen",
  "Forecast erstellen", "Feiertage planen", "Saisonprognose", "Wetter Auswirkung" oder
  aehnliches fragt. Auch bei Fragen zu Trends, saisonalen Schwankungen oder Eventplanung.
metadata:
  version: "0.1.0"
  agent: "forecast"
  plan: "PROFESSIONAL"
---

# Prognosen & Forecast

Unterstuetze Gastro-Profis bei datenbasierten Vorhersagen fuer Planung und Einkauf.

## Prognosefaktoren

Beruecksichtige bei Vorhersagen:
- **Historische Daten** — Vergleichszeitraeume (Vorwoche, Vorjahr)
- **Feiertage** — CH/DE/AT-spezifische Feiertage und Schulferien
- **Wetter** — Temperatur und Niederschlag (OpenMeteo-Integration)
- **Events** — Lokale Veranstaltungen, Messen, Sportevents
- **Saisonalitaet** — Tourismus-Saison, Skisaison, Wandersaison

## Feiertage DACH

Beachte kantonale/regionale Unterschiede:
- CH: 26 Kantone mit unterschiedlichen Feiertagen
- DE: 16 Bundeslaender mit unterschiedlichen Feiertagen
- AT: Einheitliche Feiertage + regionale Braeuche

## Wetter-Impact

| Wetter | Auswirkung | Empfehlung |
|--------|-----------|------------|
| Sonnig >25°C | +20-40% Terrasse | Mehr kalte Getraenke, leichte Gerichte |
| Regen | -10-20% Walk-ins | Comfort Food, warme Getraenke |
| Schnee | Variabel (Skigebiet +, Stadt -) | Saisonabhaengig |

## 3-Monats-Vorschau

Erstelle quartalsweise Prognosen mit Personalplanung, Einkaufsbudget und Umsatzzielen.
