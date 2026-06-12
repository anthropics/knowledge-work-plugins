---
name: gastro-einkauf
description: >
  Einkauf und Lieferantenmanagement fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Einkaufsliste erstellen", "Lieferanten vergleichen", "Preisvergleich",
  "Bestellung aufgeben", "guenstigsten Anbieter finden", "Einkauf planen" oder aehnliches
  fragt. Auch bei Fragen zu Lieferantenauswahl, Bestellrhythmus oder Preisverhandlung.
metadata:
  version: "1.0.0"
  agent: "shopping"
  plan: "STARTER"
---

# Einkauf & Lieferantenmanagement

Unterstuetze Gastro-Profis beim strategischen Einkauf und Lieferantenvergleich.

## Verfuegbare Tools

- `get_einkaufsliste` — Aktuelle Einkaufsliste (Menge, Einheit, Name, Lieferant, Status)
- `list_suppliers` — Lieferanten mit Kontakt, Liefertagen und Artikelanzahl
- `get_supplier` — Lieferant-Details: Kontakt, Kategorien, Mindestbestellwert
- `get_supplier_performance` — Lieferanten-Performance: Puenktlichkeit, Abweichungen
- `list_orders` — Bestellungen auflisten (Status: ENTWURF/GESENDET/BESTAETIGT/GELIEFERT)
- `create_order` — Neue Bestellung bei Lieferant erstellen
- `list_bestelllisten` — Bestelllisten auflisten
- `list_bestellvorlagen` — Bestellvorlagen fuer wiederkehrende Bestellungen
- `get_preiswarnungen` — Aktive Preiswarnungen bei Zutaten
- `list_wareneingaenge` — Wareneingaenge pruefen
- `list_lieferscheine` — Lieferscheine auflisten

## Workflow: Einkauf planen

1. **Einkaufsliste** — `get_einkaufsliste` fuer aktuelle Bedarfe
2. **Lieferanten pruefen** — `list_suppliers` fuer verfuegbare Anbieter
3. **Bestellung erstellen** — `create_order` mit Positionen und Liefertermin
4. **Bestellung tracken** — `list_orders` fuer Status-Updates

## Workflow: Lieferantenbewertung

1. **Performance laden** — `get_supplier_performance` fuer alle Lieferanten
2. **Puenktlichkeit** — Lieferanten mit < 90% Puenktlichkeit markieren
3. **Abweichungen** — Hohe Mengenabweichungen ansprechen
4. **Alternativ-Lieferant** — `list_suppliers` fuer andere Anbieter

## Workflow: Preischeck

1. **Preiswarnungen** — `get_preiswarnungen` fuer gestiegene Preise
2. **Vergleich** — Gleiche Produkte bei verschiedenen Lieferanten
3. **Massnahmen:** Nachverhandeln, Lieferant wechseln, oder Zutat ersetzen

## Einkaufsoptimierung

- Saisonale Ware bevorzugen (guenstiger + frischer)
- Bestellbuendelung (weniger Lieferungen = weniger Kosten)
- Rahmenvertraege fuer Hauptprodukte
- Mindestbestellwerte beachten (aus `get_supplier`)
