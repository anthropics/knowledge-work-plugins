# Onboard checklist

## The five interview questions

Ask one at a time. Wait for the full answer before moving on. One follow-up is fine if an answer is vague; do not drill further.

1. **Industry and business type.** "What kind of business do you run? Give me the one-liner."
2. **Team size.** "How many people work with you, including yourself?"
3. **Top three headaches.** "What are your three biggest headaches right now — the things that eat your time or keep you up at night?"
4. **Tools already in use.** "Which tools do you already use day-to-day? Things like QuickBooks, Gmail, Slack, Square…"
5. **Preferred cadence.** "How would you like me to check in — daily, weekly, or only when you ask?"

If the owner is short on time, compress to questions 1, 3, and 4 — those three feed the most downstream skills.

---

## Connector priority matrix

Map the owner's stated headache to the best two connectors to link first.

| Primary headache | First connector | Second connector | Prove-value recipe |
|---|---|---|---|
| Cash flow / invoicing | QuickBooks | PayPal or Square | `cash-flow-snapshot` |
| Customer follow-up | HubSpot | Gmail | `crm-maintenance` (read-only demo) |
| Hiring / job posts | Gmail | Google Calendar | `job-post-builder` |
| Staying organized | Desktop (folder setup) | Gmail | Desktop folder structure demo |
| Scheduling overload | Google Calendar | Gmail | `business-pulse` |
| General / unsure | Gmail | QuickBooks | `cash-flow-snapshot` |

If the owner names a connector not in this table, add it as the second connector and use `business-pulse` as the recipe.

---

## Recipe selection

Run the prove-value recipe immediately after the **first** connector is live — do not wait for the second. If connectors are already active at session start, run the matched recipe for the owner's primary headache before beginning the interview. Priority order:

1. QuickBooks or Square → `cash-flow-snapshot`
2. HubSpot → `crm-maintenance` (log-a-note demo, read-only)
3. Gmail → search for unread invoice-related emails, surface top 3
4. Google Calendar → `business-pulse`
5. Desktop only → walk Desktop folder setup, create recommended structure

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
- **Weekly cadence:** <trigger phrase and day, e.g. "weekly check-in every Monday">
- **Onboarded:** <YYYY-MM-DD>
```

If a memory file already exists, append or update only the `## Business context` section. Do not touch other content.
