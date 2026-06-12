---
name: dashboard-generation
description: Generate a contradictions and open questions dashboard as structured markdown plus a print-friendly HTML version. The dashboard consolidates per-domain data into a single meeting-ready document.
---

# Contradictions & Open Questions Dashboard

You produce `contradictions_dashboard.md` — a structured markdown document that
consolidates all contradictions and open questions across every domain into one
meeting-ready view. After writing the markdown, you generate a print-friendly HTML
version using the Write tool with the inline HTML template defined below.

This is the document architects bring to client meetings. It answers: "here's what
we found, here's what we need from you." Other AI tools can consume the markdown
to help find answers.

## When to Generate

- After the onboarding guide in a full pipeline run (Phase 1)
- Again after Phase 2 verification (to capture Phase 2 contradictions/questions)
- On demand when an architect requests a dashboard refresh

## Process

Read data per-domain to avoid loading everything into context at once.

1. Discover all domains using Glob on `.magellan/domains/*/` (each subdirectory
   name is a domain).
2. Read `.magellan/index.json` using the Read tool for overall stats (total entities, edges).
3. For each domain:
   a. Read `.magellan/domains/<domain>/contradictions.json` using the Read tool —
      the `active` array contains active contradictions for this domain.
   b. Read `.magellan/domains/<domain>/open_questions.json` using the Read tool —
      the `active` array contains active questions for this domain.
   c. For resolved items, check if a `resolved` directory exists under the domain.
      Read `.magellan/domains/<domain>/resolved/contradictions.json` if it exists —
      these are resolved contradictions for this domain (audit trail). Also check
      for a `resolved` array within the contradictions.json file itself.
   d. Similarly read `.magellan/domains/<domain>/resolved/questions.json` if it
      exists — these are answered questions for this domain. Also check for a
      `resolved` array within the open_questions.json file itself.
   e. Read `.magellan/domains/<domain>/summary.json` using the Read tool — entity
      count, hub count for context.
4. Synthesize the markdown following the Dashboard Structure below.
5. Write `contradictions_dashboard.md` to `.magellan/contradictions_dashboard.md`
   using the Write tool.
6. Generate the HTML version by converting the markdown to HTML using the template
   and CSS defined in the "HTML Generation" section below. Write the result to
   `.magellan/contradictions_dashboard.html` using the Write tool.

## Dashboard Structure

Write the dashboard in Markdown with these exact sections:

### 1. Executive Summary

A table showing at-a-glance metrics:

```markdown
| Metric | Count |
|--------|-------|
| Open Contradictions | N |
| Resolved Contradictions | N |
| Open Questions | N |
| Answered Questions | N |
| Domains Covered | N |
| Total Entities | N |
```

### 2. Severity Distribution

A table showing the severity breakdown of all open items:

```markdown
| Severity | Contradictions | Open Questions | Total |
|----------|---------------|----------------|-------|
| [critical] | N | N | N |
| [high] | N | N | N |
| [medium] | N | N | N |
| [low] | N | N | N |
```

### 3. Domain Breakdown

A table showing per-domain counts:

```markdown
| Domain | Open Contradictions | Open Questions | Entities | Hubs |
|--------|--------------------:|---------------:|---------:|-----:|
| billing | N | N | N | N |
| title | N | N | N | N |
```

Order domains by total open items (most first).

### 4. Open Contradictions

Group by domain, then by severity within each domain.

For each contradiction:

```markdown
### domain_name

#### [severity] contradiction_id: Short description

**Description**: Full description of the contradiction.

- **Source A**: document_name — "exact claim from source A"
- **Source B**: document_name — "exact claim from source B"
- **Related entities**: `entity_id_1`, `entity_id_2`
- **Route to**: directed_to_role
```

If there are no open contradictions, write:
"No open contradictions. All contradictions have been resolved."

### 5. Open Questions

Group by `directed_to` role first (so a client can forward the right section to
the right person), then by domain within each role group.

For each question:

```markdown
### For role_name

#### [priority] question_id: The question

**Context**: Why this question matters and what evidence prompted it.

- **Domain**: domain_name
- **Related entities**: `entity_id_1`, `entity_id_2`
```

If there are no open questions, write:
"No open questions. All questions have been answered."

### 6. Audit Trail

Two sub-sections showing resolved/answered items as tables:

```markdown
### Resolved Contradictions

| ID | Domain | Resolution | Resolved At |
|----|--------|-----------|-------------|
| c_001 | billing | Resolution note text | 2026-02-20T10:00:00Z |

### Answered Questions

| ID | Domain | Answer Source | Answered At |
|----|--------|--------------|-------------|
| oq_001 | billing | interviews/john_smith.md | 2026-02-21T14:30:00Z |
```

If no resolved/answered items exist, write "No items resolved yet."

## Writing Style

- Be direct and factual. This is a meeting document, not a narrative.
- Use the exact contradiction_id and question_id — clients track by ID.
- Include the actual source claims in quotes for contradictions. Don't paraphrase.
- Keep descriptions concise — one sentence for the description, full quotes for sources.
- Use severity badges: `[critical]`, `[high]`, `[medium]`, `[low]` — the HTML
  renderer converts these to color-coded badges.
- The `directed_to` grouping is critical — it tells the client "forward this section
  to your DBA" or "this is for the business analyst."

## Critical: Use Built-in Tools

- ALL reads MUST go through the Read tool on the appropriate file paths.
- Always read per-domain files individually. Do NOT try to load all data at once —
  that defeats the per-domain storage principle.
- The HTML generation MUST use the inline template below with the Write tool.
- Write the markdown using the Write tool (same pattern as onboarding_guide.md).

## HTML Generation

After writing the markdown dashboard, generate the HTML version. Convert the
markdown content to HTML by applying these transformations:

1. **Headers**: `# text` becomes `<h1>text</h1>`, `##` becomes `<h2>`, etc.
2. **Tables**: Pipe-delimited rows become `<table>` with `<thead>` for the first row.
   Skip separator rows (lines like `|---|---|`).
3. **Bold**: `**text**` becomes `<strong>text</strong>`
4. **Italic**: `*text*` becomes `<em>text</em>`
5. **Code spans**: `` `text` `` becomes `<code>text</code>`
6. **Unordered lists**: `- item` becomes `<li>item</li>` wrapped in `<ul>`
7. **Severity badges**: `[critical]` becomes `<span class="badge severity-critical">critical</span>`,
   similarly for `[high]`, `[medium]`, `[low]`
8. **Paragraphs**: Consecutive non-special lines wrapped in `<p>` tags

Wrap the converted HTML body in this template, replacing `{body}` with the
converted content and `{timestamp}` with the current UTC datetime formatted
as `YYYY-MM-DD HH:MM UTC`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contradictions &amp; Open Questions Dashboard</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: "Georgia", "Times New Roman", serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
    color: #1a1a1a;
    background: #fff;
}
h1 { font-size: 1.8rem; margin: 1.5rem 0 1rem; border-bottom: 2px solid #333; padding-bottom: 0.3rem; }
h2 { font-size: 1.4rem; margin: 1.5rem 0 0.8rem; color: #2c3e50; }
h3 { font-size: 1.15rem; margin: 1.2rem 0 0.6rem; color: #34495e; }
h4 { font-size: 1rem; margin: 1rem 0 0.5rem; color: #555; }
p { margin: 0.5rem 0; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.5rem 0; }
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.9rem;
}
th, td {
    border: 1px solid #ddd;
    padding: 0.5rem 0.75rem;
    text-align: left;
}
th {
    background: #f5f5f5;
    font-weight: 600;
}
tr:nth-child(even) { background: #fafafa; }
ul { margin: 0.5rem 0 0.5rem 1.5rem; }
li { margin: 0.25rem 0; }
code {
    background: #f0f0f0;
    padding: 0.15rem 0.35rem;
    border-radius: 3px;
    font-size: 0.85em;
    font-family: "Menlo", "Consolas", monospace;
}
strong { font-weight: 700; }
.badge {
    display: inline-block;
    padding: 0.1rem 0.5rem;
    border-radius: 3px;
    font-size: 0.8em;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}
.severity-critical { background: #dc3545; color: #fff; }
.severity-high { background: #fd7e14; color: #fff; }
.severity-medium { background: #ffc107; color: #1a1a1a; }
.severity-low { background: #0d6efd; color: #fff; }
.header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 3px solid #2c3e50;
}
.header h1 { border-bottom: none; margin-bottom: 0.3rem; }
.header .subtitle { color: #666; font-style: italic; }
.footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #ddd;
    text-align: center;
    color: #888;
    font-size: 0.85rem;
}
@media print {
    body { font-size: 10pt; }
    h1 { page-break-before: avoid; }
    h2 { page-break-before: always; }
    h2:first-of-type { page-break-before: avoid; }
    table { page-break-inside: avoid; }
    .no-print { display: none; }
}
</style>
</head>
<body>
<div class="header">
<h1>Contradictions &amp; Open Questions Dashboard</h1>
<p class="subtitle">Generated {timestamp}</p>
</div>
{body}
<div class="footer">
Generated by Magellan &mdash; Enterprise Knowledge Discovery
</div>
</body>
</html>
```

Write the resulting HTML to `.magellan/contradictions_dashboard.html` using the Write tool.

## What You Do NOT Do

- Do not invent contradictions or questions. Only report what's in the KG.
- Do not editorialize or suggest resolutions. Present the data objectively.
- Do not skip the audit trail. Resolved items prove the system is working.
- Do not load all contradictions at once. Read per-domain.
