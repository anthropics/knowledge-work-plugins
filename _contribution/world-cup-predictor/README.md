# World Cup 2026 Predictor

Turn Claude into a professional-grade FIFA World Cup 2026 match analyst, replicating the methodology used by Opta, FiveThirtyEight, Gracenote, and major sportsbooks.

## What it does

Predicts match outcomes using a 9-layer weighted model:

| Layer | Factor | Weight |
|---|---|---|
| Layer 0 | Media sentiment (ESM) | 12% |
| Layer 2 | Historical DNA / qualifiers | 20% |
| Layer 3 | Squad & key players | 20% |
| Layer 3B | Club momentum & league level | 8% |
| Layer 4 | Recent form (IF index) | 18% |
| Layer 5 | Betting market contrast | 14% |
| Layer 6 | Poisson model (xG) | calculated |
| Layer 8 | Climate & venue impact | 8% |

## Output format

Every prediction includes:

- **Media pulse** — what ESPN, The Athletic, Marca, L'Équipe, etc. are saying about each team right now
- **Statistical table** — qualifiers, form index, club momentum, squad value, xG
- **Probability table** — Poisson model vs ESM adjustment vs betting market
- **Most likely scoreline** — with Poisson distribution
- **Final verdict** — integrating numbers + media narrative, flagging when they contradict

## Reference files included

- `references/grupos-y-calendario.md` — All 104 group stage matches with dates, times (ET), and venues
- `references/clima-sedes.md` — Climate map for all 16 venues with xG adjustment rules
- `references/momentum-de-club.md` — Club nucleus map for all 48 teams, league levels, MCM scores
- `references/medios-deportivos.md` — Priority media sources by country and confederation
- `references/modelo-poisson.md` — Full Poisson math reference and quick-lookup probability tables
- `references/fuentes-datos.md` — Reliable data sources by confederation
- `references/betcris-apuestas.md` — Betting market structure and capital management framework

## Requires

Web search (built-in to Claude) — used to fetch current odds, media coverage, and recent results before each prediction.
