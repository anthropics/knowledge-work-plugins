# Daily Triage Brief Output Template

Use this structure exactly. Keep it scannable and action-first — every item should tell the reader exactly what to do, not just what exists.

---

**Daily Triage Brief** — *[Today's Date, Day of Week]*
*Queue window: [e.g., "Friday EOD → Monday morning" or "Yesterday EOD → This morning"]*
*Prepared for: [Alma / Syed / Support Team]*

---

## 🔴 P1 — Do First

*(Bot run failures, overdue customer responses, Urgent unowned tickets. If none: "✅ Nothing urgent — no P1 items this morning.")*

**🤖 Bot Run Failures**

- **[Customer] — [Product Line: RR / RQ / EE]**
  - What happened: [1 sentence — e.g., "Go Insurance RR run failed overnight with 0% processing rate"]
  - Linear ticket: [[ONC-XXX]](link) *(or "No ticket yet — create one")*
  - Action: [e.g., "Check if manual re-run is possible via admin panel; if not, tag engineering on the ticket"]

*(Repeat for each failure. If none: "No overnight bot run failures.")*

**📬 Overdue Customer Responses**

- **[HubSpot Ticket ID] [Company] — [Subject]**
  - Customer last replied: [Date/time — N hours ago]
  - Waiting on: [What they asked or reported, 1 sentence]
  - Action: [e.g., "Reply with an update — see ONC-XXX for status", "Acknowledge receipt and set expectations"]

*(Repeat for each. If none: "No overdue customer responses.")*

**🚨 Urgent Unowned Tickets**

- **[[TICKET-ID]] [Title]** — *[Team] | Created [Date]*
  - [1 sentence description]
  - Action: [e.g., "Assign to Alma — RR issue, her area", "Investigate processing config"]

*(Repeat for each. If none: "No urgent unowned tickets.")*

---

## 🟠 P2 — Do Today

*(New unassigned tickets needing triage, new HubSpot tickets needing acknowledgement, escalated tickets.)*

**🎫 New Linear Tickets to Triage**

- **[[TICKET-ID]] [Title]** — *[Team] | [Priority] | Created [Date]*
  - [1 sentence description]
  - Suggested owner: [Alma / Syed / Unassigned]
  - Action: [e.g., "Investigate extraction failure — check customer config", "Reach out to customer for more details"]

*(Repeat for each. If none: "No new tickets to triage.")*

**📩 New HubSpot Tickets Needing Acknowledgement**

- **[Ticket ID] [Company] — [Subject]** — *opened [Date]*
  - [1 sentence on what the customer is reporting]
  - Action: [e.g., "Send acknowledgement + create a Linear ticket", "Quick answer — see KB article X"]

*(Repeat for each. If none: "No new HubSpot tickets.")*

---

## 🟡 P3 — When P1/P2 Are Clear

*(Sev-1 cleanup, stale tickets, scheduled runs to monitor today.)*

**🧹 Sev-1 / Urgent Cleanup**

*(Stale or potentially resolved Urgent tickets that need a status check.)*

- **[[TICKET-ID]] [Title]** — *No update in [N] days*
  - Action: [e.g., "Check if this is resolved and close it", "Ping engineering for an update"]

*(If none: "No Sev-1 tickets flagged for cleanup.")*

**👀 Runs to Monitor Today**

*(Scheduled bot runs happening today that should be checked on — not failures yet, just on radar.)*

- **[Customer] — [Product Line]** — run scheduled [time if known]
  - Context: [e.g., "Had issues last week — keep an eye on this one"]
  - If it fails: [e.g., "Create an ONC ticket and tag Alma", "Try manual re-run first"]

*(If none: "No specific runs flagged for monitoring today.")*

---

## ⚪ On Radar

*(Things to be aware of but no action needed yet.)*

- [Item — 1 sentence, e.g., "Wawanesa renewal run is scheduled for Thursday — monitor Wednesday EOD"]
- [Item]

*(If none, omit this section.)*

---

## 📊 Queue Snapshot

| | Count |
|---|---|
| 🔴 P1 items | [N] |
| 🟠 P2 items | [N] |
| 🟡 P3 items | [N] |
| Total open Linear tickets (ONC) | [N] |
| Open HubSpot tickets | [N] |

---

*Quandri CX — Daily Triage Brief | [Today's Date]*
