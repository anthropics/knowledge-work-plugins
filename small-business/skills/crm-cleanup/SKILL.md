---
name: crm-cleanup
description: Scans HubSpot for stale deals, duplicate contacts, and missing fields, then fixes what the owner approves. Accepts optional scope argument for deals, contacts, or all.
allowed-tools: Read, WebFetch, Bash
---

Run a HubSpot hygiene pass using the `crm-maintenance` skill cleanup workflow. Act immediately — the user typed /crm-cleanup, so skip the intent-detection step.

Parse arguments:
- `--scope` (default: `all`) — `deals` for deal audit only, `contacts` for contact dedup only, `all` for both

## Step 1 — Scan for stale deals

If scope includes deals:

1. Pull all open deals from HubSpot.
2. Flag deals with no activity (email, call, meeting, note) in the last 14 days.
3. For each stale deal: show deal name, stage, last activity date, associated contacts, and amount.
4. Propose actions per deal: update next-step, change stage, add a note, or close-lost.

Present the full stale-deals list before making any changes.

## Step 2 — Scan for duplicate contacts

If scope includes contacts:

1. Search HubSpot contacts for likely duplicates (same email, similar names, same company + similar name).
2. For each duplicate set: show both records side-by-side — name, email, company, deals, last activity.
3. Propose which record to keep and which fields to merge.

Present all duplicate sets before merging anything.

## Step 3 — Scan for missing required fields

1. Check all open deals for missing fields: close date, amount, deal stage, associated contact, next-step/notes.
2. Check contacts associated with open deals for missing fields: email, company, phone.
3. Present a table of records with missing fields and what's missing.

## Step 4 — Apply approved fixes

1. Walk through each finding from Steps 1-3.
2. Apply only the changes the owner explicitly approves.
3. Report each change as it's made with a HubSpot link.

## Connector failures

If HubSpot is unreachable, stop — this command requires HubSpot as the data source. Tell the owner: "HubSpot isn't connected. Connect it in Cowork settings, then rerun /crm-cleanup."

## Approval gates

- **Never delete records.** Not contacts, not deals, not activities. If the user asks, say the skill cannot and direct them to HubSpot.
- **Never change deal stage or close a deal without explicit approval.** Even if evidence is strong. Flag and defer.
- **Never auto-merge duplicate contacts.** Show side-by-side and wait for approval per pair.
- **Side-by-side diffs for all changes.** Show current value and proposed value; wait for approval per item.

## Output

End with a summary: X deals updated, Y contacts merged, Z fields filled. Include links to the affected records.
