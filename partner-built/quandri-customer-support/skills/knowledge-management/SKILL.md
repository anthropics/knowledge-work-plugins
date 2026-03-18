---
name: knowledge-management
description: >
  Write and publish knowledge base articles for the Quandri CS team from resolved support tickets.
  Drafts structured how-to guides, troubleshooting docs, and FAQ entries and adds them to the
  Quandri Knowledge Hub (knowledge.quandri.io) via the Asana backlog process.
  Use when: write a KB article, document this solution, turn this ticket into a KB entry,
  add this to the knowledge base, create a how-to guide, document this fix, update the KB,
  add this to the Knowledge Hub.
---

# Knowledge Management

Turn a resolved support ticket or common question into a polished knowledge base article for the Quandri Knowledge Hub at knowledge.quandri.io.

## Background

The Quandri Knowledge Hub (knowledge.quandri.io) is the go-to place for all product knowledge — for customers, prospects, and internal staff alike. Articles are managed through an Asana backlog board and published via HelpJuice. Support owns the process: managing the Asana board, drafting articles, and working with Product and Marketing for review before publishing.

## Workflow

### Step 1 — Identify the source material

Gather (from context or by asking):
- What was the issue or question?
- What was the resolution or answer?
- Is there a Linear issue or HubSpot ticket to reference?
- Has this come up before? (recurring issue signals high-value KB candidate)

### Step 2 — Determine article type

Choose the appropriate format based on the content:

| Type                  | When to use                                                  |
|-----------------------|--------------------------------------------------------------|
| `how-to`              | Step-by-step instructions for completing a task              |
| `troubleshooting`     | Diagnosing and resolving a specific error or problem         |
| `faq`                 | Short Q&A format for common questions                        |
| `reference`           | Factual information (limits, supported formats, config options) |
| `release-note`        | Document a change that's causing support questions           |

### Step 3 — Draft the article

Write the article following the structure in `references/article-template.md`.

**Quality checklist:**
- Title is searchable — use terms customers would actually type
- Intro explains who this article is for and what problem it solves
- Steps are numbered, clear, and tested
- Screenshots or examples are noted where helpful (add placeholders if not available)
- Includes a "Still need help?" section pointing back to CS

### Step 4 — Add to the Knowledge Hub Asana Backlog

Add the drafted article to the Asana Knowledge Hub Backlog board so it can be reviewed and published:
- Asana board: https://app.asana.com/0/1207315850003741/1207316091410726
- Use `Asana:asana_create_task` to create a task in the backlog
- Include the article draft in the task description
- Assign to the appropriate Product Manager if product-specific, or leave for Support to handle
- Add a category tag matching the Knowledge Hub section it belongs to (e.g., Platform Settings, Product, Support)

**Note:** Articles move through stages: Backlog → In Progress → To be reviewed by Marketing → Published. Once in the backlog, the article has a two-week target to reach "In Progress."

### Step 5 — Confirm and share

Present the Asana task link. Ask if the article should be:
- Shared directly with the customer who raised the original ticket (send the knowledge.quandri.io link once published)
- Announced in Slack #support-team for team awareness
- Added to any onboarding flows or email sequences
