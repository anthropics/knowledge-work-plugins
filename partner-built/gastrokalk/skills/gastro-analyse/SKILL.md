---
name: gastro-analyse
description: >
  Menu Engineering und Datenanalyse fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Menu Engineering", "BCG Matrix", "Renner Penner Analyse", "Bestseller analysieren",
  "welche Gerichte laufen gut", "Menuekarte optimieren", "Deckungsbeitrag Analyse" oder
  aehnliches fragt. Auch bei Fragen zu Verkaufsdaten, Trends oder Angebotsoptimierung.
metadata:
  version: "1.0.0"
  agent: "analysis"
  plan: "STARTER"
---

# Menu Engineering & Analyse

Unterstuetze Gastro-Profis bei der datenbasierten Optimierung des Angebots.

## Verfuegbare Tools

- `get_foodcost_overview` — Food-Cost Analyse: Durchschnitt, Top Profitable, Top Food-Cost, Kategoriestatistik
- `get_profitabilitaet` — Profitabilitaets-Analyse: Gewinn und Food-Cost pro Rezept und Kategorie
- `list_recipes` — Rezepte auflisten mit Kosten und Food-Cost %
- `get_recipe` — Rezept-Details: Zutaten, Kosten, Gewinn pro Portion
- `list_menus` — Menuekarten auflisten (aktiv/inaktiv, Gerichteanzahl)
- `get_menu` — Menuekarte mit Kategorien und Gerichten inkl. Preise
- `get_preiswarnungen` — Aktive Preiswarnungen bei Zutaten

## Workflow: Menu Engineering Matrix

1. **Profitabilitaet laden** — `get_profitabilitaet` fuer alle Rezepte
2. **Food-Cost pruefen** — `get_foodcost_overview` fuer Durchschnittswerte
3. **Klassifizierung:**
   - **Stars** (Hoch beliebt + Hoher DB) → Beibehalten, prominent platzieren
   - **Puzzles** (Niedrig beliebt + Hoher DB) → Marketing verbessern, Beschreibung aendern
   - **Plowhorse** (Hoch beliebt + Niedriger DB) → Preis erhoehen oder Kosten senken
   - **Dogs** (Niedrig beliebt + Niedriger DB) → Ersetzen oder streichen
4. **Massnahmen** — Max. 3-5 konkrete Empfehlungen, priorisiert nach Impact

## Workflow: Menuekarte optimieren

1. **Aktuelle Karte** — `list_menus` und `get_menu` fuer aktive Menuekarte
2. **Analyse** — `get_profitabilitaet` fuer Gewinn pro Gericht
3. **Preiswarnungen** — `get_preiswarnungen` fuer gestiegene Zutatenkosten
4. **Empfehlungen** — Gerichte austauschen, Preise anpassen, Kategorien umstrukturieren

## Richtwerte

| Kennzahl | Optimaler Bereich |
|----------|-------------------|
| Durchschnittlicher Food-Cost | 25-32% |
| Anteil Stars auf der Karte | 30-40% |
| Anteil Dogs auf der Karte | max. 10% |
| Preis-Spread (teuerste vs. guenstigste) | max. Faktor 3x |
