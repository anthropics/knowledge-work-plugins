---
name: gastro-onboarding
description: >
  Einrichtungshilfe und Quick-Start fuer GastroKalk. Verwende diesen Skill wenn der Nutzer
  "wie fange ich an", "GastroKalk einrichten", "Setup Guide", "Quick Start", "erste Schritte",
  "was kann GastroKalk", "Hilfe bei Einrichtung" oder aehnliches fragt.
metadata:
  version: "1.0.0"
  agent: "onboarding"
  plan: "STARTER"
---

# Onboarding & Quick Start

Fuehre neue Nutzer durch die Einrichtung von GastroKalk.

## Verfuegbare Tools

- `list_team` — Pruefen ob bereits Teammitglieder angelegt sind
- `list_ingredients` — Pruefen ob Lebensmittel vorhanden sind
- `list_recipes` — Pruefen ob Rezepte existieren
- `list_suppliers` — Pruefen ob Lieferanten angelegt sind
- `get_usage` — Aktueller Plan und Limits

## Workflow: Erste Schritte (Quick Wins in 30 Min)

1. **Status pruefen** — `list_ingredients`, `list_recipes`, `list_team` aufrufen
2. **Schritt 1: Lebensmittel** — Top 20 meistgenutzte Zutaten mit Preisen anlegen
3. **Schritt 2: Erstes Rezept** — Ein Gericht kalkulieren als Lernbeispiel
4. **Schritt 3: Team** — Mitarbeiter mit Rollen einladen (`list_team` zum Pruefen)
5. **Schritt 4: Lieferanten** — Hauptlieferanten anlegen (`list_suppliers` zum Pruefen)

## Empfehlung nach Betriebstyp

| Betriebstyp | Starte mit diesen Modulen |
|-------------|--------------------------|
| Kleines Restaurant | Rezepte, Kalkulation, Allergene, Einkauf |
| Grosser Betrieb | + Inventur, Dienstplan, Kassenbuch |
| Catering | + Bestelleingang, Takeaway, Lieferscheine |
| Mehrere Standorte | + Multi-Standort (ENTERPRISE) |

## Workflow: Bestandsaufnahme

1. **Zutaten zaehlen** — `list_ingredients` — wie viele sind schon drin?
2. **Rezepte zaehlen** — `list_recipes` — schon kalkuliert?
3. **Lieferanten** — `list_suppliers` — Kontakte vollstaendig?
4. **Naechster Schritt** — Basierend auf Luecken die wichtigste Aktion empfehlen

## Hilfe-Stil

Erklaere einfach und ohne Fachjargon. Biete Schritt-fuer-Schritt Anleitungen. Feiere kleine Erfolge.
