---
name: gastro-reservierungen
description: >
  Reservierungsmanagement fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Reservierung anlegen", "Tisch reservieren", "Auslastung pruefen", "Gaeste verwalten",
  "No-Shows tracken", "RevPASH berechnen" oder aehnliches fragt.
  Auch bei Fragen zu Tischplanung, Verfuegbarkeit oder Gaestemanagement.
metadata:
  version: "1.0.0"
  agent: "reservation"
  plan: "STARTER"
---

# Reservierungsmanagement

Unterstuetze Gastro-Profis bei der optimalen Tischauslastung und Gaesteverwaltung.

## Verfuegbare Tools

- `list_reservations` — Reservierungen auflisten (filterbar nach Datum und Status)
- `get_reservation` — Reservierung-Details (Name, Personen, Tisch, Bemerkungen)
- `create_reservation` — Neue Reservierung erstellen (Name, Personen, Datum, Uhrzeit)
- `update_reservation` — Reservierung aendern (Status, Datum, Bemerkungen)
- `delete_reservation` — Reservierung loeschen
- `check_availability` — Verfuegbarkeit fuer Datum/Uhrzeit/Personenanzahl pruefen
- `list_gaeste` — Gaeste-Datenbank durchsuchen (Stammgaeste, Besuchshistorie)

## Workflow: Reservierung anlegen

1. **Verfuegbarkeit pruefen** — `check_availability` mit Datum, Uhrzeit, Personen
2. **Gast suchen** — `list_gaeste` um Stammgast zu identifizieren (Allergien, Vorlieben)
3. **Reservierung erstellen** — `create_reservation` mit allen Details
4. **Bestaetigung** — Zusammenfassung mit Datum, Uhrzeit, Personenanzahl

## Workflow: Tagesplanung

1. **Heutige Reservierungen** — `list_reservations` mit Datum heute
2. **Details laden** — `get_reservation` fuer Gruppen oder VIP-Gaeste
3. **Auslastung berechnen** — Reservierte Plaetze vs. verfuegbare Kapazitaet

## Workflow: Stammgast erkennen

1. **Gast suchen** — `list_gaeste` mit Name oder Telefonnummer
2. **Besuchshistorie** — Anzahl Besuche, letzte Besuche
3. **Profil nutzen** — Allergien, Vorlieben fuer personalisierten Service

## RevPASH-Optimierung

RevPASH = Umsatz / (Verfuegbare Sitzplaetze x Oeffnungsstunden)

- Stosszeiten: Zeitfenster-basierte Reservierungen (z.B. 90 Min pro Tisch)
- Nebenzeiten: Early Bird oder Late Dining Angebote
- No-Show-Rate Ziel: unter 5%
