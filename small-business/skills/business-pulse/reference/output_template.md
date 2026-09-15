# Output Template

This is the exact structure every pulse must follow. Do not reorder sections. Omit a section only if its connector returned no data — never leave an empty header.

Variables in `{{double braces}}` are placeholders — replace with computed values. Arrow convention: ▲ up, ▼ down, ▬ flat (<1% change). Always show the delta value after the arrow.

`{{CCY}}` is the business's ISO currency code from the `## Business context` block (`../../../shared/currency-and-locale.md`) — `AUD`, `GBP`, `USD`. Never emit a bare `$`.

---

```markdown
# Business Pulse — {{Day, Month Date, Year}}

**Overall: {{🟢|🟡|🔴}} {{one-line status, e.g. "Cash healthy, one overdue invoice needs attention."}}}**

## TL;DR

- {{Most important number-backed fact, e.g. "Cash balance USD 84k, down USD 6k WoW — two large vendor payments cleared."}}
- {{Second most important, e.g. "USD 3,400 from Acme Corp is 47 days overdue — no response since Mar 12."}}
- {{Third, e.g. "Pipeline USD 128k weighted; two deals gone cold this week."}}

---

## 💰 Cash & Finance — {{🟢|🟡|🔴}}

- **Cash balance**: {{CCY}} {{BALANCE}} ({{▲|▼|▬}} {{CCY}} {{DELTA}} WoW)
- **MTD revenue**: {{CCY}} {{MTD}} vs. {{CCY}} {{PRIOR_MTD}} last month ({{▲|▼|▬}} {{PCT}}%)
- **Outstanding AR**: {{CCY}} {{AR_TOTAL}} across {{N}} open invoices

**AR aging**
- 0–30 days: {{CCY}} {{AR_0_30}}
- 31–60 days: {{CCY}} {{AR_31_60}} {{🟡 if nonzero}}
- 61+ days: {{CCY}} {{AR_61}} {{🔴 if nonzero}}

**Overdue > 30 days**
- {{customer}} — {{CCY}} {{amount}} ({{days}} days overdue)
- {{customer}} — {{CCY}} {{amount}} ({{days}} days)

---

## 📈 Revenue & Sales — {{🟢|🟡|🔴}}

- **7-day settlements**: {{CCY}} {{SETTLEMENTS}} ({{▲|▼|▬}} {{PCT}}% vs. prior 7 days)
- **PayPal**: {{CCY}} {{PAYPAL_TOTAL}} | **Square**: {{CCY}} {{SQUARE_TOTAL}} {{omit if not connected}}

**Unusual transactions**
- {{amount}} — {{counterparty}} — {{status: failed/pending/large}}
- {{or "No unusual transactions this week."}}

---

## 🔮 Pipeline — {{🟢|🟡|🔴}}

- **Weighted pipeline**: {{CCY}} {{WEIGHTED}} ({{▲|▼|▬}} {{CCY}} {{DELTA}} WoW)
- **Coverage vs. target**: {{RATIO}}x monthly target {{🟢|🟡|🔴}}
- **Closed-won this week**: {{CCY}} {{CW}} across {{N}} deals
- **New deals created**: {{N}} ({{CCY}} {{TOTAL}})

**Deals needing attention**
- {{deal name}} — {{stage}} — {{why: gone cold / slipped / stalled}}
- {{or "No deals flagged this week."}}

---

## 📅 This Week

- {{Meeting/deadline — external party, why it matters}}
- {{Meeting/deadline}}
- {{Meeting/deadline}}
{{3–5 items max. Omit internal-only calendar noise.}}

---

## ✉️ Watch List

- {{sender / source}} — {{one-line summary of what needs attention}}
- {{sender / source}} — {{summary}}
{{Or: "No urgent threads detected." — include this explicitly so the owner knows the check ran.}}

---

## ⚠️ #1 Priority

{{One specific thing to act on today. Name amounts, people, deadlines.
Not "review cash flow" — say "The USD 4,200 invoice from Acme Corp is 23 days
overdue. Call Sarah Chen at 415-555-0192 today."}}

---

## Appendix

**Window**: {{date range}}

**Sources pulled**: {{list of connectors that returned data}}

**Sources unavailable**: {{list with reason, e.g. "Gmail — auth error" or "Zoho Desk — not connected"}}

**Thresholds used**: {{note any TODO thresholds that are still defaults}}
```

---

## Formatting rules

1. **Amounts**: the business's currency code, then the figure — `AUD 43k` for thousands, `GBP 1.2m` for millions. No unnecessary decimals, never a bare symbol.
2. **Percentages**: one decimal for trends (e.g. "▲ 8.3%"), integers elsewhere.
3. **Dates**: human-readable in prose, in the owner's country convention ("14 Apr" for most countries, "Apr 14" for the US — `../../../shared/currency-and-locale.md`); ISO in metadata ("2026-04-14").
4. **Arrow spacing**: `▲ USD 2k` not `▲USD 2k`.
5. **Length**: aim for one page. Two pages max. If a section balloons, tighten prose.
