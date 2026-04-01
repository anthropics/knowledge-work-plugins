---
name: gastro-multi-standort
description: >
  Multi-Standort-Management fuer Gastro-Ketten und Franchise. Verwende diesen Skill wenn
  der Nutzer "Filialen vergleichen", "Standort-Vergleich", "Zentraleinkauf",
  "Filial-Performance", "alle Standorte", "Benchmark Filialen" oder aehnliches fragt.
metadata:
  version: "1.0.0"
  agent: "multi-standort"
  plan: "ENTERPRISE"
---

# Multi-Standort-Management

Unterstuetze Gastro-Profis mit mehreren Standorten bei der zentralen Steuerung.

## Verfuegbare Tools

- `get_dashboard_summary` — KPIs des aktuellen Standorts
- `get_foodcost_overview` — Food-Cost Vergleich pro Standort
- `get_profitabilitaet` — Profitabilitaet pro Rezept (standortuebergreifend vergleichbar)
- `list_recipes` — Rezepte: sind sie an allen Standorten identisch?
- `list_suppliers` — Lieferanten: zentral vs. lokal
- `get_supplier_performance` — Lieferanten-Performance standortuebergreifend
- `list_bestand` — Lagerbestand je Standort
- `get_daily_briefing` — KI-Briefing mit standortspezifischen Empfehlungen

## Workflow: Standort-Benchmark

1. **KPIs laden** — `get_foodcost_overview` und `get_profitabilitaet` pro Standort
2. **Vergleichen:**
   - Food-Cost % (Ziel: alle Standorte < 30%)
   - Durchschnittlicher Gewinn pro Gericht
   - Waste % (aus Lagerbestand-Analyse)
3. **Best Practice** — Top-Standort identifizieren, Massnahmen ableiten

## Workflow: Zentraleinkauf

1. **Lieferanten** — `list_suppliers` fuer alle Standorte
2. **Performance** — `get_supplier_performance` fuer Puenktlichkeit/Abweichungen
3. **Buendelung** — Gleiche Produkte, gleicher Lieferant, Mengenrabatt
4. **Lokale Ausnahmen** — Regionale Spezialitaeten erlauben (20-30% lokal)

## Vergleichs-KPIs

| KPI | Beschreibung | Ziel |
|-----|-------------|------|
| Food Cost % | Wareneinsatz pro Standort | <30% |
| Personalkosten % | Lohnkosten pro Standort | <35% |
| Gaestezufriedenheit | Bewertungsschnitt | >4.2/5 |
| Waste % | Verschwendung pro Standort | <5% |

## Standardisierung vs. Lokalisierung

Kernmenue standardisiert (70-80%), 20-30% lokale Spezialitaeten erlaubt. Rezepte und Portionsgroessen muessen identisch sein fuer vergleichbare KPIs.
