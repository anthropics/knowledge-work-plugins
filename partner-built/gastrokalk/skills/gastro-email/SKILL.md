---
name: gastro-email
description: >
  Kommunikation und E-Mail-Vorlagen fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "E-Mail schreiben", "Lieferanten anschreiben", "Gaeste-Mail", "Newsletter",
  "Reservierungsbestaetigung", "Beschwerde beantworten", "Angebot schreiben" oder
  aehnliches fragt. Auch bei Fragen zu professioneller Kommunikation im Gastgewerbe.
metadata:
  version: "1.0.0"
  agent: "email"
  plan: "STARTER"
---

# Kommunikation & E-Mail

Unterstuetze Gastro-Profis bei der professionellen Kommunikation.

## Verfuegbare Tools

- `list_emails` — E-Mails auflisten (filterbar nach Ordner, nur ungelesene)
- `send_email` — E-Mail senden (an, betreff, inhalt, optional CC)
- `list_suppliers` — Lieferanten-Kontakte fuer E-Mail-Adresse
- `list_gaeste` — Gaeste-Kontakte fuer E-Mail-Adresse

## Workflow: E-Mail an Lieferant

1. **Kontakt finden** — `list_suppliers` fuer E-Mail-Adresse des Lieferanten
2. **E-Mail verfassen** — Professioneller Ton, klar und geschaeftlich
3. **Senden** — `send_email` mit Empfaenger, Betreff und Inhalt

## Workflow: E-Mail an Gast

1. **Kontakt finden** — `list_gaeste` fuer E-Mail-Adresse
2. **E-Mail verfassen** — Herzlich, persoenlich, einladend
3. **Senden** — `send_email`

## Workflow: Posteingang pruefen

1. **Ungelesene E-Mails** — `list_emails` mit `ungelesen: true`
2. **Priorisieren** — Gaeste > Lieferanten > allgemein
3. **Beantworten** — Antwort-Entwurf erstellen und `send_email`

## E-Mail-Vorlagen

### Lieferanten
- Preisanfrage / Angebotseinholung
- Reklamation (Qualitaet, Menge, Lieferverzug)
- Bestellbestaetigung

### Gaeste
- Reservierungsbestaetigung
- Dankes-Mail nach Besuch
- Antwort auf Online-Bewertung
- Einladung zu Events

### Team
- Dienstplanmitteilung
- Teambesprechung Einladung

## Tonalitaet

- **Lieferanten:** Professionell, klar, geschaeftlich
- **Gaeste:** Herzlich, persoenlich, einladend
- **Team:** Kollegial, motivierend, respektvoll

Schreibe in der Sprache des Empfaengers (DE/FR/EN je nach Region).
