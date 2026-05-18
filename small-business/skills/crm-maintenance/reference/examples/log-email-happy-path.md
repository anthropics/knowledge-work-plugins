# Example: log email to an existing deal (happy path)

A worked scenario for the email path — contact exists, deal resolves unambiguously, activity logs cleanly.

## Setup

- User is viewing an email thread with subject "Acme Q2 pricing follow-up"
- Thread has three messages between the user and `sarah.lin@acme.com` over the last two days
- `sarah.lin@acme.com` is an existing contact in HubSpot
- She is associated to exactly one open deal: "Acme Q2 Expansion" (proposal sent, $18K, close date May 15)

## User says

> "Add this thread to the deal."

## Skill behavior

**Step 1 — Identify intent.**
Email path (user said "this thread").

**Step 2 — Gather context.**
Reads the thread. Subject: "Acme Q2 pricing follow-up." Latest message (yesterday, 4:12pm) from Sarah: *"Confirmed, 50 seats at $360/seat works. Sending the signed SOW Friday."* Primary external contact: `sarah.lin@acme.com`.

**Step 3 — Resolve contact + deal.**
Looks up `sarah.lin@acme.com` → contact exists (Sarah Lin, Acme Corp). Finds open deals associated to her: exactly one, "Acme Q2 Expansion." Match is unambiguous.

**Step 4 — Execute.**
Writes an email activity on Acme Q2 Expansion:
- `hs_email_subject`: Acme Q2 pricing follow-up
- `hs_email_text`: "Sarah confirmed 50 seats at $360/seat ($18K). Signed SOW coming Friday."
- `hs_timestamp`: yesterday, 4:12pm
- Associated contact: Sarah Lin
- Associated deal: Acme Q2 Expansion

**Step 5 — Approval gate.**
Contact already existed, no creation announcement needed. Activity write happens inline — no separate gate because the user explicitly asked.

**Step 6 — Report.**

> Logged email activity to Acme Q2 Expansion:
> *"Sarah confirmed 50 seats at $360/seat ($18K). Signed SOW coming Friday."*
> Timestamped yesterday 4:12pm. No contact created — Sarah was already on the deal.
> [HubSpot: Acme Q2 Expansion]

## What makes this the happy path

- Single unambiguous deal association — no fuzzy match needed
- Contact already existed — no creation flow
- Thread subject is descriptive — usable as-is for activity title
- Summary focuses on decisions and numbers, not full thread transcript
