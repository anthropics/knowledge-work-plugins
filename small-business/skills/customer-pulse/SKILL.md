---
name: customer-pulse
version: 0.2.0
description: >
  Aggregates PayPal disputes, HubSpot feedback and tickets, and email
  sentiment (plus pasted or exported Google/Yelp reviews) into a themes
  report with verbatim evidence and a "do these three things this week"
  list. Use when the user asks how customers are feeling, for review
  analysis, what people are saying, or about disputes.
---

# Customer Pulse

## Quick start

Ask: *"How are customers feeling this month?"*

Claude pulls disputes, tickets, email threads, and Intercom conversations for the last 30 days, groups them into 3–5 themes with verbatim evidence, and delivers a "do these 3 things this week" action list.

To include Google/Yelp reviews, paste them after triggering — or say "I have some reviews to add."

## Workflow

1. **Set the date window.** Default: last 30 days. If the user specifies a range, use it.

2. **Pull PayPal disputes.** Fetch disputes opened in the window. If the PayPal API returns a rate-limit error, skip and add `PayPal: rate-limited — not included` to the Sources section. Do not retry; do not error. See [reference/gotchas.md](reference/gotchas.md) for the rate-limit pattern.

3. **Pull HubSpot tickets and feedback.** Fetch open and recently closed tickets. If 0 tickets exist, record `HubSpot tickets: 0` and continue — do not surface a warning.

4. **Pull Gmail threads.** Search for threads in the window containing: `refund cancel unhappy issue problem disappointed frustrated broken late slow wrong missing`. Extract subject lines and 1–2 sentence excerpts per thread.

5. **Pull Intercom conversations.** Call `search_conversations` to fetch open and recently closed conversations. Then call `get_conversation` for each conversation ID returned to access the full `conversation_parts`. Extract parts where `author.type === 'user'` — these are customer messages. Exclude parts where `author.type` is `admin` or `bot`.

6. **Accept pasted reviews (optional).** If the user pastes Google or Yelp review text, include it in the source pool tagged as `[Review]`. No connector required.

7. **Extract themes.** Group all evidence into 3–5 recurring themes. Each theme must include:
   - A one-sentence label (e.g., "Shipping delays causing repeat complaints")
   - 2–3 verbatim quotes with source tags: `[PayPal]`, `[HubSpot]`, `[Gmail]`, `[Intercom]`, or `[Review]`
   - A signal count (how many items touch this theme)

   Verbatim quotes are non-negotiable — never paraphrase. See [reference/gotchas.md](reference/gotchas.md) for the verbatim anti-pattern.

8. **Generate the "do these 3 things" list.** Rank themes by signal count. Pick the top 3 and write one concrete, owner-actionable step per theme. Format as a numbered checklist.

9. **Deliver the report.** Structure the output with these sections in order:
   - **Header** — H2 with "Customer Pulse" and the date range.
   - **Sources pulled** — Bullet list with signal counts per source (PayPal
     disputes, HubSpot tickets, Gmail threads, Intercom conversations, pasted
     reviews). Note any source that was rate-limited and skipped.
   - **Themes** — For each theme, show a bold numbered theme label with the
     signal count, followed by two verbatim quotes as blockquotes, each
     attributed to its source.
   - **Do these 3 things this week** — Numbered list of three concrete,
     owner-actionable steps, each tied to one of the top themes.

   For a complete worked example, see [reference/examples/example-report.md](reference/examples/example-report.md).

## Approval gates

This skill is **read-only** — it does not post, send, reply, or modify any records. No approval gate is required.

## Reference

- [reference/gotchas.md](reference/gotchas.md) — PayPal rate limits, HubSpot empty state, verbatim quote requirement, Gmail keyword drift
- [reference/examples/example-report.md](reference/examples/example-report.md) — full worked example output
