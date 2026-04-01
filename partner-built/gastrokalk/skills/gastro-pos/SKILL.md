---
name: gastro-pos
description: >
  Kassensystem und Zahlungsabwicklung fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Kasse oeffnen", "Tagesabschluss Kasse", "Zahlung verbuchen", "Rechnung splitten",
  "Trinkgeld verwalten", "Kassenbon", "POS System" oder aehnliches fragt.
  Auch bei Fragen zu Zahlungsmethoden, Kassendifferenzen oder SumUp-Integration.
metadata:
  version: "0.1.0"
  agent: "pos"
  plan: "STARTER"
---

# Kassensystem & POS

Unterstuetze Gastro-Profis bei der Kassenabwicklung und Zahlungsverwaltung.

## Kernaufgaben

- **Bestellungen erfassen** — Tisch-basiert oder direkt
- **Zahlungen abwickeln** — Bar, Karte, Split, Gutscheine
- **Tagesabschluss** — Z-Bericht, Kassensturz, Differenzen
- **Trinkgeld-Verwaltung** — Verteilung nach Schicht oder Pool

## Tagesabschluss-Workflow

1. Letzte Bestellungen abschliessen
2. Kassensturz: Bargeld zaehlen
3. Kartenzahlungen abstimmen
4. Z-Bericht generieren
5. Differenzen dokumentieren (Toleranz: +/- CHF 5.00)

## Kassenbuch-Pflicht

In der Schweiz und Deutschland besteht Kassenbuchpflicht. Alle Bareinnahmen und -ausgaben muessen taeglich dokumentiert werden. Lueckenlose, chronologische Aufzeichnung.

## SumUp-Integration

GastroKalk integriert sich mit SumUp fuer Kartenzahlungen. Transaktionen werden automatisch synchronisiert.
