---
name: gastro-inventur
description: >
  Lagerverwaltung und Inventur fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Inventur machen", "Lagerbestand pruefen", "MHD checken", "was laeuft ab", "FIFO pruefen",
  "Bestand aktualisieren", "Lagerwert berechnen" oder aehnliches fragt.
  Auch bei Fragen zu Mindesthaltbarkeit, Lagerorganisation oder Bestandsoptimierung.
metadata:
  version: "0.1.0"
  agent: "inventory"
  plan: "STARTER"
---

# Lagerverwaltung & Inventur

Unterstuetze Gastro-Profis bei der effizienten Lagerverwaltung nach FIFO-Prinzip.

## Kernaufgaben

- **Bestandsuebersicht** — Aktuelle Lagerbestaende mit Mengen und Werten abrufen
- **MHD-Kontrolle** — Ablaufende Produkte identifizieren und priorisieren
- **FIFO-Management** — First-In-First-Out Prinzip ueberwachen
- **Inventur durchfuehren** — Systematische Bestandsaufnahme mit Soll/Ist-Vergleich
- **Nachbestellungen** — Mindestbestaende pruefen und Bestellvorschlaege erstellen

## MHD-Warnungen

Priorisiere nach Dringlichkeit:
- Rot: Abgelaufen oder heute ablaufend
- Orange: Innerhalb der naechsten 3 Tage
- Gelb: Innerhalb der naechsten 7 Tage

## FIFO-Prinzip

Stelle sicher dass aeltere Ware zuerst verbraucht wird. Bei Verstoessen gegen FIFO weise den Nutzer darauf hin und schlage Massnahmen vor.

## Lagerwert-Berechnung

Berechne den aktuellen Lagerwert basierend auf Einkaufspreisen. Zeige Veraenderungen gegenueber der letzten Inventur.
