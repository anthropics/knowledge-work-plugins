---
name: gastro-waste
description: >
  Lebensmittelverschwendung und Nachhaltigkeit fuer die Gastronomie. Verwende diesen Skill
  wenn der Nutzer "Food Waste reduzieren", "Verschwendung messen", "Abfall tracken",
  "Nachhaltigkeit verbessern", "Reste verwerten", "Too Good To Go" oder aehnliches fragt.
metadata:
  version: "1.0.0"
  agent: "waste"
  plan: "PROFESSIONAL"
---

# Food Waste & Nachhaltigkeit

Unterstuetze Gastro-Profis bei der Reduktion von Lebensmittelverschwendung.

## Verfuegbare Tools

- `get_mhd_kritisch` — Kritische/abgelaufene MHD-Warnungen (sofortiger Handlungsbedarf)
- `list_bestand` — Lagerbestand mit MHD-Daten und Werten
- `list_recipes` — Rezepte fuer kreative Resteverwertung
- `get_recipe` — Rezept-Details: welche Zutaten werden gebraucht?
- `get_foodcost_overview` — Food-Cost fuer Waste-Auswirkung auf Marge

## Workflow: Taeglicher Waste-Check

1. **MHD pruefen** — `get_mhd_kritisch` fuer sofort zu verarbeitende Ware
2. **Bestand laden** — `list_bestand` fuer Ueberbestaende identifizieren
3. **Verwertung planen:**
   - Kurzes MHD → Als Tagesgericht/Suppe verwerten
   - Ueberbestand → Portionsgroessen anpassen oder einfrieren
   - Abgelaufen → Entsorgen und dokumentieren (HACCP)
4. **Rezept suchen** — `list_recipes` fuer Gerichte mit den betroffenen Zutaten

## Waste-Kategorien

| Kategorie | Ursache | Massnahme |
|-----------|---------|-----------|
| Zubereitungsabfall | Ruestabfall, Schalen | Nose-to-Tail, Bruehe kochen |
| Ueberproduktion | Zu viel vorbereitet | Kleinere Batches, oefter nachproduzieren |
| Tellerruecklauf | Zu grosse Portionen | Portionsgroessen reduzieren |
| MHD-Verluste | Falsche Lagerung/FIFO | `get_mhd_kritisch` taeglich |
| Lagerungs-Verluste | Temperatur, Feuchtigkeit | Lagerkontrollen |

## Zielwerte

| Kennzahl | Ziel | Branchenschnitt |
|----------|------|----------------|
| Food Waste % vom Einkauf | <5% | 8-12% |
| Tellerruecklauf | <3% | 5-8% |
| MHD-Verluste | <1% | 2-4% |

## Finanzieller Impact

Jedes Prozent weniger Food Waste = ca. 1% mehr Gewinn.
Bei CHF 500k Wareneinsatz: 1% = CHF 5.000/Jahr Ersparnis.
