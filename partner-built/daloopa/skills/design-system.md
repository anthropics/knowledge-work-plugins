# Design System

Shared formatting and styling reference for all skills. Building block skills output styled HTML directly using these conventions. Investment deliverables (Word, Excel, PDF decks) follow the same design system in their rendered format.

## Number Formatting

| Type | Format | Example |
|------|--------|---------|
| Currency (large) | `$X.Xbn` or `$X,XXXmm` | `$95.4bn`, `$2,345mm` |
| Currency (small) | `$X.XX` or `$X,XXX` | `$6.08`, `$1,234` |
| Percentages | One decimal + `%` suffix | `42.3%` |
| Multiples | One decimal + `x` suffix | `8.5x EV/EBITDA` |
| Growth rates | Signed + `%` suffix + context | `+12.3% YoY` |
| Basis points | Signed + `bps` | `+150bps` |
| Share counts | `X.XXbn` or `X,XXXmm` shares | `15.33bn shares` |

Right-align all numbers in tables. Never display raw unformatted numbers.

## Analytical Density

Every data point should include three layers where possible:

1. **The data point itself** — with Daloopa citation
2. **Context** — vs. prior period, vs. peers, vs. guidance, vs. consensus
3. **Implication** — what it suggests (margin expansion, deceleration, thesis risk)

Example:
> Revenue: [$95.4bn](https://daloopa.com/src/123) (+6.1% YoY, beat consensus by +2.3%) — acceleration from +4.8% last quarter driven by iPhone 16 cycle

Avoid single-metric tables. Combine related metrics: Revenue + Revenue Growth + Gross Margin in one table.

## Table Conventions

- **Columns** = time periods (left to right, chronological)
- **Rows** = metrics (grouped by category: P&L, margins, per-share, balance sheet)
- Include YoY growth rates as sub-rows in italics
- Highlight beats/misses with notation: `$1.52 (beat +3.2%)`
- Source citation row at bottom of every table: `Source: Daloopa (company filings)`
- Group related metrics together — no single-metric tables

## Commentary Blocks

After every major data table, include a 2-3 sentence interpretive commentary block:

1. **What the data shows** — trend, inflection, anomaly
2. **Why it matters** — competitive positioning, estimate revision risk, thesis confirmation/challenge
3. **What to watch** — upcoming catalyst, guidance change, peer divergence
4. **What could go wrong** — risks to the trend, bear case interpretation, sustainability concerns

## Analyst's Perspective

All analysis is written from the perspective of a **long/short equity investor** conducting fundamental research. This means:

**Be critical, not promotional.** Management narratives are marketing until proven by the data. When results look good, ask: Is this sustainable? Is it one-time? Is the market already pricing it in? When trends look bad, ask: Is this cyclical or structural? Is management acknowledging the problem or hiding behind adjusted metrics?

**Challenge the numbers.** Look for quality-of-earnings issues: revenue pulled forward, unsustainable margin drivers (e.g., under-investing in R&D, favorable one-time items), channel stuffing signals, aggressive accounting changes. A beat isn't bullish if it's low-quality.

**Be honest about valuation.** Don't anchor to the current stock price and work backwards. If a DCF implies 50% upside, say so — but also say what has to go right. If a stock trades at 40x earnings with decelerating growth, say that's expensive. The analysis should help the reader decide whether to own the stock, not confirm whatever they already believe.

**Flag red flags explicitly.** When you see concerning patterns — deteriorating cash conversion, growing gap between GAAP and non-GAAP, rising DSOs, management selling stock, guidance cuts disguised as "conservatism," buybacks at all-time highs — call them out clearly.

**Assign conviction.** Don't hide behind balanced language when the data points in a clear direction. If the bear case is more likely, say so. If growth is clearly decelerating, don't soften it with "remains resilient." Use precise language: "decelerating," "deteriorating," "unsustainable," "mispriced" when warranted.

**Separate signal from noise.** Not every data point matters equally. Highlight what changes the thesis and deprioritize what doesn't. A 10bps margin fluctuation is noise; a 300bps margin decline is signal.

## Report Structure

- **Header**: Company name, ticker, date, "Prepared by {FIRM_NAME}"
- **Executive summary first**: 3-5 key takeaways, each one sentence
- **Daloopa citations on every financial figure** — no uncited numbers
- **Footer**: "Prepared by {FIRM_NAME} | Data sourced from Daloopa" on every report
- Firm defaults to "Daloopa" if user doesn't specify `--firm`; see `data-access.md` Section 4.5
- Section ordering follows each skill's defined structure

## Color Palette

Consistent across charts, PDF, deck, and model:

| Role | Color | Hex |
|------|-------|-----|
| Primary | Navy | `#1B2A4A` |
| Secondary | Steel Blue | `#4A6FA5` |
| Accent | Gold | `#C5A55A` |
| Positive | Forest Green | `#27AE60` |
| Negative | Crimson | `#C0392B` |
| Light Gray | — | `#F8F9FA` |
| Mid Gray | — | `#E9ECEF` |
| Dark Gray | — | `#6C757D` |
| Near Black | — | `#343A40` |

Chart color sequence: Navy, Steel Blue, Gold, then grays.

## Chart Styling

All charts follow these rules:
- Grid lines: light gray (`#E9ECEF`), no box border
- Labels: 11px, gray (`#6C757D`)
- Title: 14px bold, navy
- Source citation below every chart: `Source: Daloopa (company filings)`
- Adjacent commentary block required for every chart

Standard chart types:
1. **Time-series** — Revenue, margins, EPS, KPIs over quarters. Bar + line combo.
2. **Waterfall** — Bridge from base to target value (revenue walk, value creation, EPS bridge)
3. **Football field** — Horizontal range bars comparing valuation methodologies
4. **Pie** — Segment revenue/profit breakdown, geographic mix
5. **Scenario bar** — Bull/base/bear comparison
6. **DCF sensitivity** — WACC vs terminal growth heatmap

## Output Formats

All skills must produce professional deliverables suitable for institutional distribution:

| Skill Type | Primary Output | Secondary | Notes |
|------------|---------------|-----------|-------|
| Building block analysis | .html | — | Styled HTML with design system CSS inlined; opens in any browser |
| Research notes | .docx | — | Word for editability |
| Financial models | .xlsx | — | Excel for interactivity |
| Pitch decks | .pdf | .html (source) | HTML is working format; PDF is the deliverable |
| Comp sheet models | .xlsx | — | Excel for interactivity |

**Never deliver raw markdown as a final output.** Building block skills write styled HTML directly using the HTML Report Template below. The analyst receives HTML, Word, Excel, or slide deck files.

## Typography (Rendered Outputs — HTML, Deck, Docx)

- Primary font: system sans-serif stack (Segoe UI, -apple-system, Arial)
- Headers: bold, 18-28px, navy (`#1B2A4A`)
- Body: 12-13px, dark gray (`#343A40`)
- Table cells: 11px, tabular-nums for number alignment
- Citations: 8-9px italic
- Slide content (deck): 11-14px with generous line-height

## HTML Report Template

Building block skills write styled HTML directly using this template. Copy the full template (including all CSS) into every report. Write the analysis as HTML content inside the `<body>` — use `<h1>`, `<h2>`, `<h3>` for headings, `<table>` for data tables, `<blockquote>` for commentary blocks, `<p>` for prose, `<ul>`/`<ol>` for lists, and `<a>` for Daloopa citation links.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
:root {
    --navy: #1B2A4A;
    --steel-blue: #4A6FA5;
    --gold: #C5A55A;
    --green: #27AE60;
    --red: #C0392B;
    --light-gray: #F8F9FA;
    --mid-gray: #E9ECEF;
    --dark-gray: #6C757D;
    --near-black: #343A40;
}

@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
}

* {
    box-sizing: border-box;
}

body {
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    font-size: 12px;
    line-height: 1.6;
    color: var(--near-black);
    max-width: 100%;
    margin: 0 auto;
    padding: 20px 40px;
}

h1 {
    font-size: 24px;
    font-weight: bold;
    color: var(--navy);
    border-bottom: 3px solid var(--navy);
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 16px;
}

h2 {
    font-size: 18px;
    font-weight: bold;
    color: var(--navy);
    border-bottom: 1px solid var(--mid-gray);
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 12px;
}

h3 {
    font-size: 14px;
    font-weight: bold;
    color: var(--steel-blue);
    margin-top: 16px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 8px;
}

a {
    color: var(--steel-blue);
    text-decoration: none;
}

strong {
    font-weight: 600;
}

em {
    font-style: italic;
    color: var(--dark-gray);
}

blockquote {
    border-left: 4px solid var(--steel-blue);
    background: var(--light-gray);
    padding: 12px 16px;
    margin: 12px 0;
    font-size: 11px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 11px;
    font-variant-numeric: tabular-nums;
}

thead {
    background: var(--navy);
    color: white;
}

th {
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

td {
    padding: 6px 10px;
    border-bottom: 1px solid var(--mid-gray);
}

/* Right-align numeric columns (2nd column onward) */
td:not(:first-child), th:not(:first-child) {
    text-align: right;
}

tr:nth-child(even) {
    background: var(--light-gray);
}

tr:hover {
    background: #EDF2F7;
}

code {
    background: var(--light-gray);
    padding: 2px 4px;
    border-radius: 3px;
    font-size: 10px;
}

pre {
    background: var(--light-gray);
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 10px;
}

ul, ol {
    padding-left: 20px;
    margin-bottom: 8px;
}

li {
    margin-bottom: 4px;
}

hr {
    border: none;
    border-top: 1px solid var(--mid-gray);
    margin: 20px 0;
}

img {
    max-width: 100%;
    height: auto;
    margin: 12px 0;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 9px;
    color: var(--dark-gray);
    font-style: italic;
    margin-top: 24px;
    padding-top: 8px;
    border-top: 1px solid var(--mid-gray);
}
    </style>
</head>
<body>

<!-- Report content goes here: use <h1>, <h2>, <table>, <blockquote>, <p>, <a>, etc. -->

<!-- Replace {FIRM_NAME} with user's --firm argument, or "Daloopa" if not specified -->
<div class="footer">Prepared by {FIRM_NAME} | Data sourced from Daloopa</div>
</body>
</html>
```
