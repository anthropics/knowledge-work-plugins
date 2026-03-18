# Weekly Incident & Ticket Report — Template

Use this exact structure for every report. Preserve all table formats, headers, and section order.

---

## Header Section

```
# Weekly Incident & Ticket Report
**Week:** [Start Date] – [End Date]
**Prepared by:** Nick Roach
**Generated:** [Today's date]
```

---

## Summary Table

```markdown
## Summary

| Metric               | Total | In Progress | In QA | Released | Blocked |
|----------------------|-------|-------------|-------|----------|---------|
| Sev 0                |       |             |       |          |         |
| Sev 1                |       |             |       |          |         |
| Sev 2                |       |             |       |          |         |
| Sev 3                |       |             |       |          |         |
| No Severity          |       |             |       |          |         |
| Feature Requests     |       | —           | —     | —        | —       |
| Duplicates (closed)  |       | —           | —     | —        | —       |

**Top 3 contributing components/areas:**
1. [Component/area] — X tickets
2. [Component/area] — X tickets
3. [Component/area] — X tickets
```

Rules for the Summary Table:
- Feature Requests and Duplicates (closed) rows use "—" in all status columns — they are counted separately, not by status.
- Every number in the Sev 0–No Severity rows must sum to the total ticket count minus feature requests and duplicates.
- If a severity/status combination has zero tickets, write `0` (not blank).

---

## Evidence of Analysis Section

```markdown
## Evidence of Analysis

**Tickets analyzed:**
- [QND-XXX] Title
- [QND-XXX] Title
- (list every ticket)

**Summary statistics:**
- Total tickets reviewed: X
- Date range: [Start] – [End]
- Filters applied: Created within reporting window, ONC team triage view
- Team: ONC

**Data quality notes:**
- [Note any tickets missing severity labels]
- [Note any tickets with incomplete descriptions or ambiguous status]
- [Note "None" if data is clean]

**Assumptions:**
- [Any assumptions made during analysis, e.g., how duplicates were identified]
```

---

## Root Cause Analysis Section

Aim for 2–4 patterns maximum. Only include patterns with at least 2 related tickets, or any single Sev 0 or Sev 1 incident.

```markdown
## Root Cause Analysis

### [Pattern/Incident Title]

**Tickets:** [QND-XXX], [QND-XXX]
**Root cause:** [Single sentence describing the underlying cause]
**Contributing factors:**
- [Factor 1]
- [Factor 2]
**Resolution status:** [In Progress / Released / Blocked / Open]
**Recommended action:** [Specific next step]
**Owner:** [Name or team]
**Target date:** [Date or "TBD"]

---

### [Next Pattern/Incident Title]
...
```

---

## Tickets Worth Highlighting Table

```markdown
## Tickets Worth Highlighting

| Ticket | Why it matters | Recommended action |
|--------|----------------|--------------------|
| [QND-XXX] Title | [Customer impact, systemic risk, cross-team dep, or leadership visibility] | [Action] |
```

Include tickets that are: high customer impact, systemic risk, cross-team dependencies, or require leadership visibility. If no tickets qualify, write "No tickets require highlighting this week."

---

## Open Items from Previous Weeks Table

```markdown
## Open Items from Previous Weeks

| Item | Status | Blocker (if any) |
|------|--------|------------------|
| [Item] | [Status] | [Blocker or "None"] |
```

If no historical data is available from the Linear view: write "No historical data available in provided view."

---

## Questions for EM/PM Triage

```markdown
## Questions for EM/PM Triage

- [Routing ambiguity, severity dispute, or capacity concern]
- [Another question if applicable]
```

If no open questions: write "No open questions this week."

---

## Output wrapper

Always wrap your output like this:

```
<scratchpad>
[Your full analysis here: list all tickets, categorize by severity and status, identify patterns,
flag highlights, plan root cause sections. This is your working space — be thorough.]
</scratchpad>

<report>
[Your complete formatted report here, following the exact template above]
</report>
```
