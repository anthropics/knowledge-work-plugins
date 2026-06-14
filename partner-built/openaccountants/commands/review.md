---
name: review
description: THE handoff. Routes the user (with their working paper) to the named lead verifier for their jurisdiction with a Calendly booking link.
---

The user wants a licensed accountant to review their tax situation.

Call the `openaccountants` MCP server's `request_accountant_review` tool with:

- **jurisdiction**: the country code (or US state code) the user is in
- **scenario**: a 1-2 sentence summary of what they need reviewed
- **working_paper**: if you have produced a worksheet, classified transactions, draft return lines, or any structured tax output in this conversation, **paste it in full as markdown**. The verifier needs to see the actual numbers before the call, not just a text brief. Without the working paper, they walk in blind and have to rebuild the case from scratch.
- **contact_name** and **contact_email**: ask the user (encourage them to share, but not strictly required)
- **tax_year**: if known
- **urgency**: `urgent` (filing in <2 weeks), `standard` (current filing season), or `planning` (future-year strategy)

Present the returned response to the user:

- The **named accountant** routed (e.g. "Werner Britz, CA(SA)", "Michael Cutajar, CPA")
- The **Calendly URL** for booking
- Confirmation the working paper was captured
- The standing disclaimer: no client-accountant relationship until both sides sign an engagement letter; the initial call is a review conversation

End with a clear call-to-action: click the Calendly link to book.
