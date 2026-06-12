---
name: gastro-compliance
description: >
  HACCP, Lebensmittelsicherheit und Compliance fuer die Gastronomie. Verwende diesen Skill
  wenn der Nutzer "HACCP Plan", "Hygiene pruefen", "Temperaturkontrolle", "Reinigungsplan",
  "Lebensmittelsicherheit", "Kontrolle vorbereiten", "Dokumentation HACCP" oder aehnliches
  fragt. Auch bei Fragen zu gesetzlichen Vorschriften, Kennzeichnungspflichten oder Audits.
metadata:
  version: "1.0.0"
  agent: "compliance"
  plan: "STARTER"
---

# HACCP & Lebensmittelsicherheit

Unterstuetze Gastro-Profis bei der Einhaltung aller Hygiene- und Sicherheitsvorschriften.

## Verfuegbare Tools

- `list_checklisten_heute` — Heutige Checklisten mit Fortschritt und Eintraegen
- `get_mhd_kritisch` — Kritische MHD-Warnungen (Lebensmittelsicherheit)
- `detect_allergens` — 14 EU-Hauptallergene in Zutatenlisten erkennen
- `list_bestand` — Lagerbestand mit MHD-Daten pruefen

## Workflow: Taeglicher HACCP-Check

1. **Checklisten pruefen** — `list_checklisten_heute` fuer den Tagesfortschritt
2. **MHD-Kontrolle** — `get_mhd_kritisch` fuer abgelaufene/kritische Ware
3. **Massnahmen** — Abgelaufene Ware entsorgen und dokumentieren

## Workflow: Kontrolle vorbereiten

1. **Checklisten-Status** — `list_checklisten_heute` — alle erledigt?
2. **MHD pruefen** — `get_mhd_kritisch` — keine abgelaufene Ware im Lager?
3. **Allergene** — `detect_allergens` fuer alle aktiven Menuegerichte
4. **Bestand pruefen** — `list_bestand` — Lagerorganisation korrekt?

## HACCP 7 Grundsaetze

1. **Gefahrenanalyse** — Biologische, chemische, physikalische Gefahren
2. **CCPs bestimmen** — Kritische Kontrollpunkte festlegen
3. **Grenzwerte festlegen** — Temperatur, Zeit, pH-Wert
4. **Ueberwachung** — Monitoring-System einrichten
5. **Korrekturmassnahmen** — Bei Abweichungen sofort handeln
6. **Verifizierung** — Regelmaessige Ueberpruefung
7. **Dokumentation** — Lueckenlose Aufzeichnung

## Temperaturgrenzwerte

| Bereich | Temperatur | Bemerkung |
|---------|-----------|-----------|
| Tiefkuehl | -18°C oder kaelter | Nie unterbrechen |
| Kuehlung | 0-5°C | Taeglich pruefen |
| Heisshalten | min. 65°C | Max. 3h |
| Kerntemperatur Gefluegel | min. 75°C | Pflicht |
| Gefahrenzone | 5-65°C | Max. 2h total |

## Gesetzliche Grundlagen DACH

- **Schweiz:** LMV (Lebensmittelverordnung), Art. 11 Deklarationspflicht
- **Deutschland:** LMIV (EU) 1169/2011 + nationale Hygieneverordnung
- **Oesterreich:** LMIV (EU) 1169/2011 + Lebensmittelsicherheits-VO
