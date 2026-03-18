---
name: weekly-incident-report
description: >
  Generate a weekly incident and ticket report for the Quandri ONC team by pulling data from
  the Linear triage view, analyzing tickets by severity and status, identifying patterns, and
  producing a structured report with root cause analysis.
  Use when: weekly report, incident report, weekly incident report, generate the weekly report,
  ONC report, weekly ticket summary, triage report, incident summary, run the weekly report.
---

# Weekly Incident Report

Generate a structured weekly incident and ticket report by connecting to Linear, analyzing the ONC triage view, and producing a full report with severity breakdowns, root cause analysis, and actionable recommendations.

**Accuracy is the top priority.** Every ticket count, severity label, and status must exactly match what is in Linear. Do not summarize, skip, or infer — pull the real data.

---

## Configuration

- **Linear view to analyze:** `https://linear.app/quandriio/team/ONC/triage`
- **Time window:** The previous 7 full calendar days from today
- **Prepared by:** Nick Roach

---

## Workflow

### Step 1 — Determine the date range

Calculate the reporting window: today's full date minus 7 calendar days. For example, if today is March 16, 2026, the report covers March 9–15, 2026 (inclusive). Use this window to filter tickets by creation date.

### Step 2 — Pull tickets from the Linear ONC triage view

Fetch all issues from the ONC team's triage view. Use the following approach:

1. Call `list_teams` to find the ONC team ID.
2. Call `list_issue_statuses` for the ONC team to get the exact status names (e.g., "In Progress", "In QA", "Released", "Blocked"). Use these exact strings throughout the report — do not rename or reinterpret them.
3. Call `list_issues` with:
   - `teamId`: ONC team ID
   - Filter to tickets created within the 7-day reporting window
   - `limit: 250`
   - Paginate using `cursor` if needed — collect every page before proceeding
4. For each issue, collect:
   - Ticket ID and title
   - Severity label (Sev 0, Sev 1, Sev 2, Sev 3, No Severity — check labels)
   - Current status (exact value from `list_issue_statuses`)
   - Component/area tags
   - Whether it's a feature request (check labels or title conventions)
   - Whether it's a duplicate or closed
   - Creation date and resolution/updated date
   - Description (first 2–3 sentences for context)
   - Any root cause or incident notes (from description or comments — call `list_comments` if useful)
5. Call `list_issue_labels` for the ONC team to understand what severity labels look like (e.g., "Sev 0", "Sev 1", etc.) before categorizing tickets.

**Record the total ticket count before proceeding.** This is your ground truth — all counts in the report must sum to this total.

### Step 3 — Do your analysis (scratchpad)

Before writing the report, work through this analysis privately:

1. List all tickets found with their IDs, titles, severities, and statuses
2. Categorize them: bucket by severity (Sev 0–3, No Severity) and by status (In Progress, In QA, Released, Blocked)
3. Count feature requests and closed/duplicate tickets separately
4. Identify the top 3 contributing components or areas by ticket volume (look at labels and titles)
5. Identify patterns: are there 2–4 recurring themes or Sev 0/1 incidents that share a root cause?
6. Flag tickets with high customer impact, systemic risk, cross-team dependencies, or needing leadership visibility
7. Note any data quality gaps: tickets missing severity labels, incomplete descriptions, ambiguous status
8. Plan your root cause analysis sections (aim for 2–4 patterns max)

### Step 4 — Generate the report

Follow the structure in `references/report-template.md` exactly. Produce all sections in order, preserving all markdown tables and formatting.

---

## Important notes

- **Never fabricate or infer.** If a field is missing (no severity label, no description), say so explicitly — do not fill it in.
- **Every count must be exact.** The totals in the Summary Table must sum to the total tickets pulled from Linear.
- **Use Linear's exact status names** from `list_issue_statuses` — do not rename them.
- **Paginate with cursor.** Always set `limit: 250` and paginate until no cursor is returned.
- For the Root Cause Analysis, aim for 2–4 patterns maximum — quality over quantity.
- If you cannot access previous week data for the "Open Items from Previous Weeks" section, note "No historical data available in provided view."
- Wrap your analysis in `<scratchpad>` tags and your final report in `<report>` tags.
