---
name: gastro-personal
description: >
  Personalverwaltung und Dienstplanung fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Dienstplan erstellen", "Schichten planen", "Mitarbeiter verwalten", "Arbeitszeiten
  pruefen", "Ueberstunden berechnen", "L-GAV pruefen" oder aehnliches fragt.
  Auch bei Fragen zu Arbeitsrecht, Pausen, Ruhezeiten oder Personalkosten.
metadata:
  version: "1.0.0"
  agent: "staff"
  plan: "STARTER"
---

# Personalverwaltung & Dienstplanung

Unterstuetze Gastro-Profis bei der Personalplanung unter Beruecksichtigung der gesetzlichen Vorgaben.

## Verfuegbare Tools

- `list_team` — Teammitglieder mit Rollen, Email und Berechtigungen
- `list_shifts` — Schichten im Dienstplan (filterbar nach Datum und Mitarbeiter)

## Workflow: Wer arbeitet heute?

1. **Schichten laden** — `list_shifts` mit `von` und `bis` auf heutiges Datum
2. **Team-Uebersicht** — `list_team` fuer vollstaendige Mitarbeiterliste
3. **Abgleich** — Wer ist eingeteilt, wer fehlt, wer hat frei?

## Workflow: Wochenplan pruefen

1. **Schichten der Woche** — `list_shifts` mit Montag bis Sonntag
2. **Abdeckung pruefen** — Jede Schicht besetzt? Ueber-/Unterbesetzung?
3. **Rechtliche Pruefung** — Ruhezeiten, Maximalstunden, freie Tage eingehalten?

## Gesetzliche Grundlagen DACH

### Schweiz (L-GAV Gastgewerbe)
- Max. 42h/Woche (Vollzeit), 50h Obergrenze
- Min. 11h Ruhezeit zwischen Schichten
- 2 freie Tage pro Woche (1x zusammenhaengend)
- Pausen: 15 Min ab 5.5h, 30 Min ab 7h

### Deutschland (ArbZG)
- Max. 8h/Tag (48h/Woche), 10h bei Ausgleich
- Min. 11h Ruhezeit
- Pausen: 30 Min ab 6h, 45 Min ab 9h

### Oesterreich (AZG)
- Max. 8h/Tag, 40h/Woche Normalarbeitszeit
- Min. 11h Ruhezeit
- Pausen: 30 Min ab 6h

## Personalkosten-Ziel

Personalkosten sollten 30-35% vom Umsatz betragen. Bei Abweichungen Optimierungsvorschlaege machen.
