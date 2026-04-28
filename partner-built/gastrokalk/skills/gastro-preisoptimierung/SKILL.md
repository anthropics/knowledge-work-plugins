---
name: gastro-preisoptimierung
description: >
  Preisgestaltung und Preisoptimierung fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Preise optimieren", "Verkaufspreis berechnen", "Deckungsbeitrag I II", "Aufschlag
  berechnen", "Preisvergleich", "Marge verbessern" oder aehnliches fragt.
  Auch bei Fragen zu Preispsychologie, Preiskalkulation oder Wettbewerbspreisen.
metadata:
  version: "1.0.0"
  agent: "pricing"
  plan: "STARTER"
---

# Preisgestaltung & Preisoptimierung

Unterstuetze Gastro-Profis bei der strategischen Preisgestaltung.

## Verfuegbare Tools

- `list_recipes` — Rezepte mit aktuellem Food-Cost % und Verkaufspreis
- `get_recipe` — Rezept-Details: Zutaten, Warenkosten, Gewinn pro Portion
- `calculate_recipe_cost` — Kalkulation mit Ruest-/Garverlust und empfohlenem VK
- `get_foodcost_overview` — Durchschnittlicher Food-Cost, Top 5 profitable, Top 5 teuerste
- `get_profitabilitaet` — Gewinn und Food-Cost nach Rezept und Kategorie
- `get_preiswarnungen` — Aktive Preiswarnungen bei Zutaten (Preiserhoehungen)
- `list_ingredients` — Zutatenpreise fuer Alternativ-Kalkulation

## Workflow: Verkaufspreis optimieren

1. **Rezept laden** — `get_recipe` fuer aktuelle Kosten und VK
2. **Food-Cost bewerten** — Liegt er im Zielbereich fuer das Segment?
3. **Kalkulation** — `calculate_recipe_cost` mit aktuellem `targetFoodCostPercent`
4. **Empfohlenen VK** — Aus der Kalkulation ableiten
5. **Preispsychologie** — Schwellenpreise, Ankereffekte beruecksichtigen

## Workflow: Preiswarnungen bearbeiten

1. **Warnungen abrufen** — `get_preiswarnungen` fuer gestiegene Einkaufspreise
2. **Betroffene Rezepte** — `list_recipes` filtern
3. **Auswirkung berechnen** — `calculate_recipe_cost` mit neuen Preisen
4. **Massnahmen:** VK anpassen, guenstigere Zutat suchen, oder Marge akzeptieren

## Kalkulationsschema

1. Wareneinsatz (Netto-Einkaufspreis aller Zutaten)
2. \+ Zuschlag Gemeinkosten (Energie, Miete, Versicherung)
3. = Selbstkosten
4. \+ Gewinnzuschlag
5. = Netto-Verkaufspreis
6. \+ MwSt
7. = Brutto-Verkaufspreis

## Deckungsbeitrag

- **DB I** = Verkaufspreis (netto) - Wareneinsatz
- **DB II** = DB I - anteilige Personalkosten

## Aufschlagsfaktoren nach Segment

| Segment | Faktor | Food Cost Ziel |
|---------|--------|----------------|
| Quick Service | 2.5-3.0x | 33-40% |
| Casual Dining | 3.0-3.5x | 28-33% |
| Fine Dining | 3.5-4.5x | 22-28% |
| Bar/Getraenke | 4.0-6.0x | 17-25% |

## Preispsychologie

- Schwellenpreise nutzen (CHF 28.50 statt 29.00)
- Keine Waehrungszeichen auf der Karte (reduziert Preissensibilitaet)
- Teuerste Position nicht ganz oben (Ankereffekt)
