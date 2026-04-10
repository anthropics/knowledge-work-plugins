# IB Advisory Patterns

Valuation methodology templates and layouts for investment banking decks.

## DCF Layout

### Projection Table
```
| Metric           | Year 1  | Year 2  | Year 3  | Year 4  | Year 5  |
|------------------|---------|---------|---------|---------|---------|
| Revenue          | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  |
| Revenue Growth   | +X.X%   | +X.X%   | +X.X%   | +X.X%   | +X.X%   |
| EBITDA           | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  |
| EBITDA Margin    | X.X%    | X.X%    | X.X%    | X.X%    | X.X%    |
| D&A              | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  |
| EBIT             | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  |
| Tax @ X.X%       | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  |
| NOPAT            | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  | $X,XXX  |
| + D&A            | $XXX    | $XXX    | $XXX    | $XXX    | $XXX    |
| - CapEx          | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  |
| - ΔWC            | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  | ($XXX)  |
| **UFCF**         | **$X,XXX** | **$X,XXX** | **$X,XXX** | **$X,XXX** | **$X,XXX** |
```

### Valuation Bridge
```
| Component                | Value      |
|--------------------------|------------|
| PV of Projected FCFs     | $XX,XXX    |
| PV of Terminal Value      | $XX,XXX    |
| Enterprise Value          | $XX,XXX    |
| Less: Net Debt           | ($X,XXX)   |
| Equity Value              | $XX,XXX    |
| Shares Outstanding        | X,XXXmm    |
| **Implied Price/Share**   | **$XXX**   |
```

### Sensitivity Matrix
Display as color-coded heatmap:
- Green cells: above current price (upside)
- Red cells: below current price (downside)
- Bold the base case cell
- Show WACC as rows, terminal growth as columns

## Comps Table Format

```
| Company | Ticker | Mkt Cap | TEV    | Rev Growth | EBITDA Margin | P/E   | Fwd P/E | EV/EBITDA | EV/Rev |
|---------|--------|---------|--------|------------|---------------|-------|---------|-----------|--------|
| Peer 1  | XXX    | $XXbn   | $XXbn  | +X.X%      | X.X%          | XX.Xx | XX.Xx   | XX.Xx     | X.Xx   |
| ...     |        |         |        |            |               |       |         |           |        |
| **Median** |     |         |        | +X.X%      | X.X%          | XX.Xx | XX.Xx   | XX.Xx     | X.Xx   |
| **Mean**   |     |         |        | +X.X%      | X.X%          | XX.Xx | XX.Xx   | XX.Xx     | X.Xx   |
| **Target** | **XXX** | **$XXbn** | **$XXbn** | **+X.X%** | **X.X%** | **XX.Xx** | **XX.Xx** | **XX.Xx** | **X.Xx** |
```

Footnotes at bottom:
- Source: Daloopa (company filings), market data as of {date}
- NTM estimates from consensus where available
- LTM figures based on trailing four quarters

## Precedent Transactions Format

```
| Date    | Acquirer    | Target      | TEV ($mm) | TEV/Revenue | TEV/EBITDA | Premium |
|---------|-------------|-------------|-----------|-------------|------------|---------|
| MM/YYYY | Company A   | Company B   | $X,XXX    | X.Xx        | XX.Xx      | XX%     |
| ...     |             |             |           |             |            |         |
| **Median** |          |             |           | X.Xx        | XX.Xx      | XX%     |
```

## SOTP (Sum-of-the-Parts) Format

```
| Segment       | Revenue | EBITDA | Applied Multiple | Implied Value | Methodology     |
|---------------|---------|--------|------------------|---------------|-----------------|
| Segment A     | $X,XXX  | $X,XXX | XX.Xx EV/EBITDA  | $XX,XXX       | Peer median     |
| Segment B     | $X,XXX  | $X,XXX | XX.Xx EV/EBITDA  | $XX,XXX       | Comp A, B avg   |
| Segment C     | $X,XXX  | n/a    | X.Xx EV/Revenue  | $XX,XXX       | High-growth SaaS|
| **Total EV**  |         |        |                  | **$XX,XXX**   |                 |
| Less: Net Debt|         |        |                  | ($X,XXX)      |                 |
| **Equity Value** |      |        |                  | **$XX,XXX**   |                 |
| Per Share     |         |        |                  | **$XXX**      |                 |
```

## Football Field Format

Display as horizontal bars, one per methodology:
- Each bar spans from low to high estimate
- Diamond marker at midpoint
- Vertical dashed line at current price
- Labels: methodology name on left, low/high values at bar ends
- Order from top to bottom: DCF, P/E Comps, EV/EBITDA Comps, Precedent Txns, 52W Range

Color coding:
- Bars above current price → navy/steel blue tones
- Bars below current price → gray tones
- Current price line → red dashed
