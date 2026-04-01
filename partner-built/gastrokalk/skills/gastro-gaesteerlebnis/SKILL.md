---
name: gastro-gaesteerlebnis
description: >
  Gaesteerlebnis und CRM fuer die Gastronomie. Verwende diesen Skill wenn der Nutzer
  "Gastprofil anlegen", "VIP Gast", "Stammgast verwalten", "Feedback auswerten",
  "Gaestewuensche notieren", "Allergien eines Gastes", "Bewertungen analysieren" oder
  aehnliches fragt. Auch bei Fragen zu Gaestebindung, Beschwerdemanagement oder Upselling.
metadata:
  version: "1.0.0"
  agent: "gaesteerlebnis"
  plan: "STARTER"
---

# Gaesteerlebnis & CRM

Unterstuetze Gastro-Profis bei der Pflege von Gaesteprofilen und Gaestebindung.

## Verfuegbare Tools

- `list_gaeste` — Gaeste-Datenbank durchsuchen (Name, Besuchsanzahl, Kontakt)
- `list_reservations` — Reservierungen mit Gastinformationen
- `get_reservation` — Reservierung-Details: Bemerkungen, Allergien, Vorlieben
- `create_reservation` — Neue Reservierung fuer Stammgast anlegen
- `send_email` — Persoenliche E-Mail an Gast senden (Danke, Einladung, Angebot)
- `list_emails` — Bisherige E-Mail-Kommunikation pruefen

## Workflow: Stammgast erkennen

1. **Gast suchen** — `list_gaeste` mit Name oder Telefonnummer
2. **Besuchshistorie** — Anzahl Besuche, letzte Besuche
3. **Reservierungen** — `list_reservations` fuer bisherige Buchungen und Bemerkungen
4. **Service personalisieren** — Allergien, Vorlieben, Sitzplatzpraeferenzen beruecksichtigen

## Workflow: VIP-Betreuung

1. **Gast identifizieren** — `list_gaeste` — wer hat die meisten Besuche?
2. **Profil laden** — Vorlieben, Allergien, besondere Anlaesse
3. **Persoenliche Nachricht** — `send_email` fuer Geburtstag, Jubilaeum, Einladung

## Upselling-Strategien

- Personalisierte Empfehlungen basierend auf Gastprofil
- Weinbegleitung zum gewaehlten Menue
- Aperitif bei Ankunft vorschlagen
- Dessert-Empfehlung nach Hauptgang

## Beschwerdemanagement

1. Zuhoeren und Ernst nehmen
2. Entschuldigen (auch wenn nicht schuld)
3. Sofort-Loesung anbieten (Rabatt, Ersatzgericht, Gratis-Dessert)
4. Nachfassen per E-Mail — `send_email`
5. Intern dokumentieren und Ursache beseitigen
