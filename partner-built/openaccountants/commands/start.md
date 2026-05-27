---
name: start
description: Front door for any tax question. Scope your intent and jurisdiction, get a ready plan with the right skills loaded.
---

The user wants to start a tax / accounting workflow.

If they haven't told you the **intent** (what they're trying to do — tax return, VAT return, formation, find deductions, classify transactions, payroll, comparison, etc.) or the **jurisdiction** (country, US state, Canadian province), ask them first.

Then call the `openaccountants` MCP server's `start` tool:

```json
{ "intent": "<their intent>", "jurisdiction": "<ISO code or country/state name>" }
```

You'll get back a `skills_to_load` list. Call `get_skill` for each slug, in order. Apply the rules. Cite the skill slugs. Surface every AUDIT FLASH POINT marker. When the user is ready to file or make a real decision, hand off via `request_accountant_review`.
