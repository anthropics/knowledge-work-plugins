# Onboard checklist

## The five interview questions

Ask one at a time. Wait for the full answer before moving on. One follow-up is fine if an answer is vague; do not drill further.

1. **Industry and business type.** "What kind of business do you run? Give me the one-liner."
2. **Team size.** "How many people work with you, including yourself?"
3. **Top three headaches.** "What are your three biggest headaches right now — the things that eat your time or keep you up at night?"
4. **Tools already in use.** *Covered in Step 2 of the workflow — skip in the interview pass.*
5. **Preferred cadence.** "How would you like me to check in — daily, weekly, or only when you ask?"

If the owner is short on time, compress to questions 1 and 3 — those two feed the most downstream skills.

---

## Headache → functional categories

Translate the owner's stated headache into two functional categories. **Use the category names in conversation with the owner — never the connector names from the next table.**

| Primary headache | Category 1 | Category 2 | Prove-value recipe |
|---|---|---|---|
| Cash flow / invoicing | Bookkeeping | Payment processor | `cash-flow-snapshot` |
| Customer follow-up | CRM | Inbox | `crm-maintenance` (read-only demo) |
| Hiring / job posts | Inbox | Calendar | `job-post-builder` |
| Staying organized | File storage | Inbox | Desktop folder structure demo |
| Scheduling overload | Calendar | Inbox | `business-pulse` |
| General / unsure | Inbox | Bookkeeping | `cash-flow-snapshot` |

---

## Category → supported connectors + skill availability

Claude-internal reference. **Do not surface this table to the owner.** Use it to know:

- Which connector to mention in branch (c) of Step 3 as the "supported connector here."
- Which skills work via CSV/paste when the owner doesn't have the supported connector.
- Which skills require live data and won't run without it.

| Category | Supported connector | Works via CSV/paste | Requires live data (won't run without) |
|---|---|---|---|
| Bookkeeping | QuickBooks Online | `cash-flow-snapshot`, `margin-analyzer`, `month-end-prep` | `invoice-chase`, `sales-brief`, `quarterly-review`, `plan-payroll`, `content-strategy` |
| Payment processor | PayPal, Square, or Stripe | `cash-flow-snapshot`, `margin-analyzer` (with bookkeeping CSV) | `invoice-chase` (cross-reference step), `ticket-deflector` (refund action) |
| CRM | HubSpot | (paste a basic lead list for ad-hoc prioritization only) | `lead-triage`, `call-list`, `crm-maintenance`, `crm-cleanup` |
| Inbox | Gmail or Microsoft 365 (Outlook) | paste threads if needed | most skills degrade gracefully without Inbox; very few hard-require it |
| Calendar | Google Calendar or Microsoft 365 | paste week if needed | most skills degrade gracefully without Calendar |
| File storage | Desktop (folder access) | n/a (file-native) | none |

---

## Recipe selection

Run the prove-value recipe immediately after the **first** data path is live — connector, CSV upload, or pasted data. If connectors are already active at session start, run the matched recipe for the owner's primary headache before beginning the interview. Priority order:

1. Bookkeeping data live (QB or CSV) → `cash-flow-snapshot`
2. CRM live (HubSpot) → `crm-maintenance` (log-a-note demo, read-only)
3. Inbox live (Gmail) → search for unread invoice-related threads, surface top 3
4. Calendar live → `business-pulse`
5. File storage only → walk Desktop folder setup, create recommended structure

**QuickBooks profile_info_required:** If QuickBooks returns a `profile_info_required` status (missing business_name or industry), use the `quickbooks-profile-info-update` tool with the owner's business name from interview question 1 before running `cash-flow-snapshot`. Do not skip the recipe — collect the missing info first.

---

## Owner profile — storage format

Write this block to the Cowork session memory directory under the heading `## Business context`. Every other skill reads this section by heading match. Do not rename the heading or change the field names.

```markdown
## Business context

- **Business:** <one-liner — industry, product/service>
- **Size:** <number of people, including owner>
- **Top headaches:** <headache 1> · <headache 2> · <headache 3>
- **Connected tools:** <comma-separated list of active connectors>
- **CSV/paste paths:** <categories the owner uses via CSV instead of connector, e.g. "Bookkeeping (Xero CSV)">
- **Weekly cadence:** <trigger phrase and day, e.g. "weekly check-in every Monday">
- **Onboarded:** <YYYY-MM-DD>
```

If a memory file already exists, append or update only the `## Business context` section. Do not touch other content.
