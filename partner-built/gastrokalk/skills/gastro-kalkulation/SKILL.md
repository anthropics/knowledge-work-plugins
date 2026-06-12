---
name: gastro-kalkulation
description: >
  Rezeptkalkulation und Food-Cost-Analyse fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Rezept kalkulieren", "Food Cost berechnen", "Wareneinsatz berechnen", "Was kostet
  das Gericht", "Kalkulation erstellen", "Deckungsbeitrag berechnen" oder aehnliches fragt.
  Auch bei Fragen zu Preisgestaltung, Verkaufspreis oder Marge eines Gerichts.
metadata:
  version: "0.1.0"
  author: "Marcel Gaertner"
  region: "DACH"
---

# Rezeptkalkulation & Food-Cost-Analyse

Unterstuetze Gastro-Profis bei der praezisen Kalkulation von Rezepten und Gerichten.

## Verfuegbare Tools

Nutze das `calculate-recipe` Tool des gastrokalk MCP-Servers fuer alle Kalkulationsaufgaben.

## Workflow

1. **Zutaten klaren** — Frage nach dem Gericht oder den Zutaten, falls nicht angegeben
2. **Zutaten suchen** — Verwende `search-ingredients` um aktuelle Preise und Einheiten zu finden
3. **Kalkulation durchfuehren** — Verwende `calculate-recipe` mit allen Zutaten und Mengen
4. **Ergebnisse praesentieren** — Zeige Wareneinsatz, Food Cost %, empfohlenen VK-Preis

## Darstellung der Ergebnisse

Praesentiere Kalkulationen uebersichtlich:
- Wareneinsatz pro Portion in CHF/EUR
- Food Cost Prozent (Ziel: 28-35% fuer Hauptgerichte)
- Empfohlener Verkaufspreis (Faktor 3.0-3.5)
- Deckungsbeitrag I und II

## DACH-spezifische Hinweise

- Preise standardmaessig in CHF (Schweiz), alternativ EUR (DE/AT)
- MwSt-Saetze beachten: CH 8.1%, DE 19%/7%, AT 20%/10%
- Branchenstandards fuer Food Cost: 25-35% je nach Segment
- Bei Fine Dining: 28-32%, bei Quick Service: 30-35%

## Tipps fuer den Nutzer

Wenn der Food Cost ueber dem Zielwert liegt, schlage Optimierungen vor:
- Guenstigere Zutaten-Alternativen
- Portionsgroessen anpassen
- Saisonale Zutaten nutzen
- Mise-en-place Optimierung (weniger Abfall)
