# Output Template

This is the exact structure every pulse must follow. Do not reorder sections. Omit a section only if its connector returned no data — never leave an empty header.

Variables in `{{double braces}}` are placeholders — replace with computed values. Arrow convention: ▲ up, ▼ down, ▬ flat (<1% change). Always show the delta value after the arrow.

---

```markdown
# Business Pulse — {{Day, Month Date, Year}}

**Overall: {{🟢|🟡|🔴}} {{one-line status, e.g. "Cash healthy, one overdue invoice needs attention."}}}**

## TL;DR

- {{Most important number-backed fact, e.g. "Cash balance $84k, down $6k WoW — two large vendor payments cleared."}}
- {{Second most important, e.g. "$3,400 from Acme Corp is 47 days overdue — no response since Mar 12."}}
- {{Third, e.g. "Pipeline $128k weighted; two deals gone cold this week."}}

---

## 💰 Cash & Finance — {{🟢|🟡|🔴}}

- **Cash balance**: ${{BALANCE}} ({{▲|▼|▬}} ${{DELTA}} WoW)
- **MTD revenue**: ${{MTD}} vs. ${{PRIOR_MTD}} last month ({{▲|▼|▬}} {{PCT}}%)
- **Outstanding AR**: ${{AR_TOTAL}} across {{N}} open invoices

**AR aging**
- 0–30 days: ${{AR_0_30}}
- 31–60 days: ${{AR_31_60}} {{🟡 if nonzero}}
- 61+ days: ${{AR_61}} {{🔴 if nonzero}}

**Overdue > 30 days**
- {{customer}} — ${{amount}} ({{days}} days overdue)
- {{customer}} — ${{amount}} ({{days}} days)

---

## 📈 Revenue & Sales — {{🟢|🟡|🔴}}

- **7-day settlements**: ${{SETTLEMENTS}} ({{▲|▼|▬}} {{PCT}}% vs. prior 7 days)
- **PayPal**: ${{PAYPAL_TOTAL}} | **Square**: ${{SQUARE_TOTAL}} {{omit if not connected}}

**Unusual transactions**
- {{amount}} — {{counterparty}} — {{status: failed/pending/large}}
- {{or "No unusual transactions this week."}}

---

## 🔮 Pipeline — {{🟢|🟡|🔴}}

- **Weighted pipeline**: ${{WEIGHTED}} ({{▲|▼|▬}} ${{DELTA}} WoW)
- **Coverage vs. target**: {{RATIO}}x monthly target {{🟢|🟡|🔴}}
- **Closed-won this week**: ${{CW}} across {{N}} deals
- **New deals created**: {{N}} (${{TOTAL}})

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
Not "review cash flow" — say "The $4,200 invoice from Acme Corp is 23 days
overdue. Call Sarah Chen at 415-555-0192 today."}}

---

## Appendix

**Window**: {{date range}}

**Sources pulled**: {{list of connectors that returned data}}

**Sources unavailable**: {{list with reason, e.g. "Gmail — auth error" or "Zendesk — not connected"}}

**Thresholds used**: {{note any TODO thresholds that are still defaults}}
```

---

## Formatting rules

1. **Dollar amounts**: `$43k` for thousands, `$1.2m` for millions. No unnecessary decimals.
2. **Percentages**: one decimal for trends (e.g. "▲ 8.3%"), integers elsewhere.
3. **Dates**: human-readable in prose ("Apr 14"), ISO in metadata ("2026-04-14").
4. **Arrow spacing**: `▲ $2k` not `▲$2k`.
5. **Length**: aim for one page. Two pages max. If a section balloons, tighten prose.
