---
name: gastro-rezepte
description: >
  Rezeptgenerierung und Zutatensuche fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Rezept erstellen", "Rezept generieren", "Zutat suchen", "Lebensmittel finden",
  "Was kann ich kochen mit", "Rezeptvorschlag", "Menuekarte erstellen" oder aehnliches fragt.
  Auch bei Fragen zu Zutaten, Naehrwerten oder Rezeptideen.
metadata:
  version: "0.1.0"
  author: "Marcel Gaertner"
  region: "DACH"
---

# Rezeptgenerierung & Zutatensuche

Unterstuetze Gastro-Profis bei der Erstellung und Optimierung von Rezepten.

## Verfuegbare Tools

- `generate-recipe` — Generiere vollstaendige Rezepte mit Zutaten, Mengen und Zubereitung
- `search-ingredients` — Durchsuche die Lebensmittel-Datenbank nach Zutaten, Preisen und Einheiten

## Workflow fuer Rezeptgenerierung

1. **Anforderungen klaren** — Art des Gerichts, Kueche, Portionen, Einschraenkungen
2. **Zutaten recherchieren** — Verwende `search-ingredients` fuer verfuegbare Zutaten
3. **Rezept generieren** — Verwende `generate-recipe` mit den Parametern
4. **Optimieren** — Auf Wunsch Kalkulation mit `calculate-recipe` ergaenzen

## Workflow fuer Zutatensuche

1. Verwende `search-ingredients` mit dem Suchbegriff
2. Praesentiere Ergebnisse mit Name, Einheit, Preis und Lieferant
3. Bei mehreren Treffern: filtere nach Relevanz oder frage nach

## Regionale Zutaten

Bevorzuge regionale Zutaten aus der DACH-Region:
- Schweiz: Berner Oberland, Graubuenden, Wallis
- Deutschland: Regionale Erzeuger, saisonale Ware
- Oesterreich: Alpenregion, lokale Spezialitaeten

## Saisonalitaet beachten

Empfehle Zutaten passend zur Jahreszeit:
- Fruehling: Spargel, Baerlauch, Rhabarber
- Sommer: Beeren, Tomaten, Zucchini
- Herbst: Kuerbis, Pilze, Wild
- Winter: Wurzelgemuese, Kohl, Zitrusfruechte
