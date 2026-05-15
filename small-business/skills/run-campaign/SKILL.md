---
name: run-campaign
description: Runs an end-to-end marketing campaign — sales analysis, content brief, Canva assets, HubSpot send. Accepts optional lookback and channel arguments.
allowed-tools: Read, WebFetch, Bash
---

Run the full campaign pipeline by chaining three skills in order. The owner approves at each handoff — never roll past a gate without explicit confirmation.

Parse arguments:
- `--lookback` (default `90d`) — how far back to look for the revenue dip
- `--channel` (default `both`) — `email`, `social`, or `both`

## Step 1 — Sales analysis + content brief (content-strategy)

Trigger the `content-strategy` skill workflow:
1. Pull sales data from QuickBooks and PayPal for the lookback window.
2. Identify the revenue dip — which product/service, which time period, magnitude.
3. Produce a 30-day prioritized content brief: what to push, what offer to run, what to hold.
4. Present the brief to the owner. Wait for explicit "approved, build the assets" before continuing.

If the owner edits the brief, incorporate edits and re-present.

## Step 2 — Asset generation + send staging (canva-creator)

After Step 1 approval, trigger the `canva-creator` skill workflow:
1. Take the approved brief from Step 1 as input.
2. Build the posting calendar matched to the brief's priorities.
3. Generate on-brand Canva assets for each post (apply each on screen for owner approval before moving on).
4. Draft caption copy for each post.
5. Stage the scheduled send in HubSpot (do NOT send — staging only).
6. Present the staged campaign to the owner. Wait for explicit "approved, send to segment X" before Step 3.

## Step 3 — Audience segmentation (lead-triage)

After Step 2 approval, trigger the `lead-triage` skill workflow:
1. Pull HubSpot contacts that match the campaign's target segment (from the approved brief).
2. Score by engagement, company fit, urgency markers.
3. Produce two deliverables:
   - **Bulk send list** — the segment receiving the staged campaign from Step 2
   - **High-priority call list** — top 5 leads the owner should call personally with talking points
4. Block calendar time for the call list.
5. Present both lists. Wait for explicit "send" before pushing the HubSpot campaign live.

## Approval gates (must hold)

- Never auto-progress between steps. Each handoff requires explicit owner approval.
- Never send the HubSpot campaign without the owner's "send" command in Step 3.
- If any connector is unreachable (QuickBooks, PayPal, Canva, HubSpot), stop, report which connector failed, and ask whether to retry or abort.

## Output

End the run with a one-paragraph recap: revenue dip identified, posts generated, segment size, calls booked. Link to the HubSpot campaign URL once sent.
