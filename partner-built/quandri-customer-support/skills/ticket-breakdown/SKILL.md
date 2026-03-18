---
name: ticket-breakdown
description: >
  Generate a full Linear ticket breakdown for a specific customer — covering top priority tickets,
  all in-progress work, backlog count, and recent releases — formatted for both internal CS/CSM use
  and as a clean customer-facing audit summary.
  Use when: ticket audit, ticket audit for a customer, run a ticket audit, do a ticket audit.
---

# Customer Ticket Breakdown

Produce a structured audit of all open Linear tickets for a specific customer. The output is an internal brief for the CS rep or CSM, organized by ticket status to match exactly what is visible in Linear.

**Accuracy is the top priority.** Every ticket count and every ticket listed must exactly match what is in Linear. Do not summarize, skip, or infer — pull the real data.

---

## Workflow

### Step 1 — Identify the customer

Get the customer name from the user's prompt or the conversation context. If it's ambiguous (e.g., a nickname or partial name), clarify before proceeding.

Then look up the customer in HubSpot to retrieve:
- Full company name (use this exact name when searching Linear)
- Plan tier / ARR
- Named CSM and account owner
- Renewal date (flag if within 90 days)
- Any open HubSpot tickets associated with this account — note their IDs and URLs, as these will be linked inline throughout the output

### Step 2 — Pull ALL Linear tickets for this customer via the Customers API

Tickets are linked to customers in Linear through the **Customers feature** — the same one visible at linear.app/quandriio/customers. This is the only reliable way to get all tickets for a customer. Do not use `list_issues` with `query` or `label` to find customer tickets — those approaches miss tickets and are not how Linear associates issues with customers.

**Fetch the customer and all their linked issues:**

1. Call `list_customers` with:
   - `query`: the customer name (e.g., `"Blue Ridge"`)
   - `includeNeeds: true` — this returns all issues linked to this customer
   - `limit: 250`

2. From the response, locate the matching customer record and extract every issue linked via their needs. Each need contains an associated issue ID.

3. **Paginate if needed.** If a `cursor` is returned, call `list_customers` again with that cursor and `includeNeeds: true` until no cursor is returned. Collect all linked issue IDs across every page.

4. Once you have the full list of issue IDs, call `get_issue` on each one to retrieve:
   - Ticket ID, title, current status (exact label from Linear), priority, assignee
   - Creation date and last updated date
   - Description (first 2–3 sentences)
   - Most recent comment or activity (date + content) — call `list_comments` if needed
   - Any linked HubSpot ticket URL (check attachments or external link fields)

5. Also call `list_issue_statuses` to confirm the exact status names in this workspace before bucketing in Step 3.

**After collecting all issues, record the total count.** This number must match what is shown in the customer's record in Linear. If anything seems off, re-check before proceeding.

If the customer is not found or has no linked issues, tell the user and stop.

### Step 3 — Compose the output

Follow the structure in `references/breakdown-template.md` exactly. Produce the sections in this order:

1. **Executive Summary**
2. **Todo**
3. **In Progress**
4. **Blocked**
5. **Backlog** (count only)
6. **Feature Intake**
7. **Released (last 30 days)** (count only)

Details for each section:

**1. Executive Summary**
Identify the 3 highest-impact open tickets across all statuses (prioritize by: Urgent > High > Medium, then recency as tiebreaker). For each, write 2–3 sentences covering: what the issue is, what work has been done, and what the current status or next step is. If a HubSpot ticket is linked to any of these, include the HubSpot link inline.

**2. Todo**
List every ticket in the Todo bucket — do not skip any. For each:
- Ticket ID and title
- Priority and assignee (or "Unassigned")
- 1–2 sentence summary of what the ticket is about
- Most recent update or comment (date + brief note), or "No updates since creation" if none
- HubSpot ticket link if one is associated

**3. In Progress**
List every ticket in the In Progress bucket — do not skip any. For each:
- Ticket ID and title
- Priority and assignee (or "Unassigned")
- 1–2 sentence summary of what's being worked on
- Most recent update or comment (date + brief note)
- HubSpot ticket link if one is associated

**4. Blocked**
List every ticket in the Blocked bucket — do not skip any. For each:
- Ticket ID and title
- Priority and assignee (or "Unassigned")
- 1–2 sentence summary of the issue
- What is blocking it, based on description or most recent comment
- Most recent update or comment (date + brief note)

**5. Backlog**
Report the count only. Do not list individual tickets or summaries.

**6. Feature Intake**
List every ticket in the Feature Intake bucket — do not skip any. For each:
- Ticket ID and title
- 1–2 sentence summary of what is being requested
- Most recent update or comment (date + brief note), or "No updates" if none

**7. Released (last 30 days)**
Report the count only of tickets moved to a Released/Done/Completed status within the past 30 days from today. Do not list individual tickets.

---

## Important notes

- **Never fabricate or infer.** If a field is blank (no assignee, no comments, no description), say so explicitly — do not fill it in with assumptions.
- **Every count must be exact.** The number in each section heading must equal the number of tickets listed below it. Count them before outputting.
- **Always use `list_customers` with `includeNeeds: true` to find a customer's tickets.** This is the only method that matches what Linear's Customers view shows. Never use `list_issues` with `query` or `label` as a substitute — those miss tickets.
- **Always set `limit: 250` and always paginate with `cursor`.** Never rely on a single API response.
- **Every count must be exact.** The number in each section heading must equal the number of tickets listed below it.
- **Use Linear's exact status names** from `list_issue_statuses` — do not rename or reinterpret them.
- If a customer has tickets across multiple Linear teams, pull from all teams and note the team name alongside each ticket.
- Be precise about dates — "last 30 days" means exactly that, calculated from today's date.
