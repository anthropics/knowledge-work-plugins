---
name: gastro-allergene
description: >
  Allergenerkennung und Deklaration fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Allergene pruefen", "Allergen-Deklaration", "Unvertraeglichkeiten checken",
  "ist das glutenfrei", "enthaelt das Laktose", "Allergene kennzeichnen" oder aehnliches fragt.
  Auch bei Fragen zu HACCP, Lebensmittelsicherheit oder gesetzlicher Kennzeichnungspflicht.
metadata:
  version: "0.1.0"
  author: "Marcel Gaertner"
  region: "DACH"
---

# Allergenerkennung & Deklaration

Unterstuetze Gastro-Profis bei der korrekten Identifikation und Deklaration von Allergenen.

## Verfuegbares Tool

Nutze das `detect-allergens` Tool des gastrokalk MCP-Servers fuer die Allergenanalyse.

## Die 14 EU-Hauptallergene

Diese 14 Allergene muessen in der DACH-Region deklariert werden:

1. Glutenhaltiges Getreide (Weizen, Roggen, Gerste, Hafer, Dinkel)
2. Krebstiere
3. Eier
4. Fisch
5. Erdnuesse
6. Sojabohnen
7. Milch (einschl. Laktose)
8. Schalenfruchte (Mandeln, Haselnuesse, Walnuesse, etc.)
9. Sellerie
10. Senf
11. Sesamsamen
12. Schwefeldioxid und Sulphite (>10mg/kg)
13. Lupinen
14. Weichtiere

## Workflow

1. **Rezept/Gericht erfassen** — Alle Zutaten inklusive Gewuerze und Saucen
2. **Allergenanalyse** — Verwende `detect-allergens` mit der Zutatenliste
3. **Ergebnisse praesentieren** — Klar strukturiert mit Allergen-Codes (A-N)
4. **Kreuzkontamination** — Weise auf moegliche Risiken hin

## Gesetzliche Grundlagen

- **Schweiz:** Lebensmittelverordnung (LMV), Art. 11 — schriftliche Deklaration Pflicht
- **Deutschland:** LMIV (EU) 1169/2011 — muendliche Auskunft genuegt, schriftlich empfohlen
- **Oesterreich:** LMIV (EU) 1169/2011 — gleiche Regelung wie DE

## Darstellung

Verwende die Standard-Allergenkennzeichnung:
- A = Gluten, B = Krebstiere, C = Eier, D = Fisch
- E = Erdnuesse, F = Soja, G = Milch, H = Schalenfruchte
- I = Sellerie, J = Senf, K = Sesam, L = Sulphite
- M = Lupinen, N = Weichtiere

Markiere erkannte Allergene deutlich und weise auf versteckte Allergene hin (z.B. Soja in Saucen, Gluten in Gewuerzmischungen).
