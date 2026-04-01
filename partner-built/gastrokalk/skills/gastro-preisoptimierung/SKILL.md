---
name: gastro-preisoptimierung
description: >
  Preisgestaltung und Preisoptimierung fuer die Gastronomie. Verwende diesen Skill wenn der
  Nutzer "Preise optimieren", "Verkaufspreis berechnen", "Deckungsbeitrag I II", "Aufschlag
  berechnen", "Preisvergleich", "Marge verbessern" oder aehnliches fragt.
  Auch bei Fragen zu Preispsychologie, Preiskalkulation oder Wettbewerbspreisen.
metadata:
  version: "0.1.0"
  agent: "pricing"
  plan: "STARTER"
---

# Preisgestaltung & Preisoptimierung

Unterstuetze Gastro-Profis bei der strategischen Preisgestaltung.

## Kalkulationsschema

1. **Wareneinsatz** (Netto-Einkaufspreis aller Zutaten)
2. **+ Zuschlag Gemeinkosten** (Energie, Miete, Versicherung)
3. **= Selbstkosten**
4. **+ Gewinnzuschlag**
5. **= Netto-Verkaufspreis**
6. **+ MwSt**
7. **= Brutto-Verkaufspreis**

## Deckungsbeitrag

- **DB I** = Verkaufspreis (netto) - Wareneinsatz
- **DB II** = DB I - anteilige Personalkosten
- **DB III** = DB II - anteilige Fixkosten

## Preispsychologie

- Schwellenpreise nutzen (CHF 28.50 statt 29.00)
- Keine Waehrungszeichen auf der Karte (reduziert Preissensibilitaet)
- Teuerste Position nicht ganz oben (Ankereffekt)
- Gerichte in aufsteigender Preisreihenfolge vermeiden

## Aufschlagsfaktoren nach Segment

| Segment | Faktor | Food Cost Ziel |
|---------|--------|----------------|
| Quick Service | 2.5-3.0x | 33-40% |
| Casual Dining | 3.0-3.5x | 28-33% |
| Fine Dining | 3.5-4.5x | 22-28% |
| Bar/Getraenke | 4.0-6.0x | 17-25% |
