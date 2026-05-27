# Welle Template — Cold Mail V2

The default body template for a wave-shipped cold mail. Each draft inherits this skeleton; paragraph 1 is per-account, paragraphs 2-5 vary lightly.

## Subject formula

`[Region] → [Company]: [pain stub] + [brand word]`

Max 60 characters. Examples (anonymized):

- `[Region] → [Company]: KI-augmented Sales gegen [Pain]`
- `Aus [Region]: Vertrieb neu denken für [Company]`
- `[Region] → [Company]: [Pain] mit KI-augmented Sales adressieren`

Anti-patterns to avoid in the subject:

- `[Consultancy]: BAFA-funded sales advisory for the German Mittelstand` — substance at the top
- `Practitioner with 24 years of industry sales` — generic, substitutable
- `Introducing [Consultancy]` — about you, not the prospect

## Body skeleton (5 blocks, in this order)

```
[Block 1 — Pain]  (1-2 sentences, per-account)
Herr [LastName],

[Open with the verifiable signal. Reference the source — a LinkedIn
post date, a press release, an open role, a trade-show event.
Do not invent — if no verifiable signal exists, this account does
not belong in the wave.]

[Block 2 — Region anchor]  (1-2 sentences)
Aus [Region], [Consultancy] arbeitet seit [N] Jahren mit fertigendem
Mittelstand in [region-specific subset] — Schwerpunkt
[industry-sub-segment, e.g. Sondermaschinenbau, Werkzeugbau,
Antriebstechnik] zwischen [size band].

[Block 3 — Solution frame with brand word]  (1-2 sentences)
[Brand word]-Ansatz: [Vertrieb neu denken] — KI-augmented Sales als
Schicht auf Ihre bestehenden Werkzeuge (CRM, ERP, Office). Nicht
ersetzen, sondern härten.

[Block 4 — Substance anchor]  (1 sentence, short)
Hintergrund: [N] Jahre B2B-Vertrieb bei [reference industry OEMs],
[certification, e.g. BAFA-zugelassen], [optional third anchor].

[Block 5 — CTA]  (1 sentence)
20 Minuten Sondierung in den nächsten zwei Wochen — passt für
[Company]? [Calendar link] oder Antwort mit Wunsch-Zeitfenster.

Herzliche Gruesse aus [Region]
[Sender Name]
```

## Worked example (anonymized)

**Subject:** `Bodensee → MachineCo: KI-augmented Sales gegen die 9-Tage-Trips`

```
Herr Schmidt,

Ihr LinkedIn-Post vom 12. Mai über die 9-Tage-Vertriebs-Reise-Trips
ohne Pre-Trip-Lead-Priorisierung — genau dort sehe ich den scharfsten
Hebel.

Aus Ravensburg arbeitet Lepper Consulting seit drei Jahren mit
fertigendem Mittelstand am Bodensee und in Sueddeutschland — Schwerpunkt
Sondermaschinen- und Anlagenbau zwischen 50 und 200 Mitarbeiter.

JLC-Ansatz: Vertrieb neu denken — KI-augmented Sales als Schicht auf
Ihre bestehenden Werkzeuge. Nicht ersetzen, sondern härten.

Hintergrund: 24 Jahre B2B-Vertrieb bei grossen Industrie-OEMs,
BAFA-zugelassener Berater, regionaler Industrieverband.

20 Minuten Sondierung in den naechsten zwei Wochen — passt das fuer
MachineCo? Zeeg-Link: [...] oder Antwort mit Wunsch-Zeitfenster.

Herzliche Gruesse aus Ravensburg
Jan Lepper
```

(Note: in a real mail, German umlauts are written properly — ä, ö, ü, ß — never "ae", "oe", "ue".)

## Block-by-block fail patterns

| Block | Common failure | Fix |
|---|---|---|
| 1 — Pain | Generic industry pain | Replace with verifiable signal + date + source |
| 2 — Region | Region in signature only | Move to first sentence of block 2 |
| 3 — Brand word | Buzzword frame | Replace with brand-word + plain frame |
| 4 — Substance | Substance at top | Keep at end, single sentence |
| 5 — CTA | "Let's schedule a meeting" | Name 2 specific slots OR provide a booking link |

## Variants by trigger type

- **T1 (new appointment):** Block 1 references the appointment date and what the new role-holder is likely solving in their first 90 days
- **T2 (open role 8+ weeks):** Block 1 references the open role and the revenue exposure of a prolonged gap
- **T3 (funded initiative):** Block 1 references the funded initiative + a question about how sales fits into the rollout
- **T4 (milestone anniversary):** Block 1 references the anniversary + a question about how modernized sales features into the celebration

## Localization

This template is German-language by default. For English-language outreach into DACH (e.g. UK / US subsidiaries), translate but keep the structure — pain first, region anchor, brand word, substance at end, low-friction CTA. The pattern works across languages; the German formulation is just the field-tested version.
