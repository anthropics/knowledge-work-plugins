---
name: grow-pipeline
description: Fills the funnel end to end without the owner babysitting it — reads the market and the competition for context, builds a ranked list of named prospects with a reason attached to each, writes personalized outreach in the owner's own voice, and logs every touch to the CRM. Chains lead-finder, outreach-composer, and crm-autopilot behind a web-native market read, with an owner approval at every handoff. Use this whenever the owner wants more pipeline rather than one specific piece of it, including phrasings like "I need more leads," "fill my funnel," "who should I be calling and what do I say," "find me customers like my best ones and reach out," "build me a prospect list and write the emails," or "sales has gone quiet, get something moving." Reach for it when the owner describes wanting new business generally rather than asking for a list or a single email.
allowed-tools: Read, WebFetch
---

Run the pipeline-building chain: a web-native market read for context, then `lead-finder` for the list, `outreach-composer` for the copy, and `crm-autopilot` for the record. Each skill keeps its own gates, and this command does not loosen any of them.

Connectors: Apollo (or Clay) plus HubSpot is the full path. Mail (Gmail or Microsoft 365) adds sending. Zoom adds recorded discovery and sales calls to Step 4's logging — read-only, only meetings the owner hosted or attended, and its recordings list covers a one-month window per call, so a sweep asks month by month rather than for a range it cannot return. With none of them, web research plus an uploaded customer CSV goes in, a ranked list and drafted outreach come out for the owner to send by hand, and the log lives in a spreadsheet. That is a real run.

## Step 1 — Market context first (web research)

Run this leg inline and keep it scoped to what informs targeting — not a full weekly brief. Scan public sources on the owner's competitors and their market: sites and pricing, ad and social activity, job postings, and press.

**In:** the competitor watchlist if one exists, plus public sources. Win-loss data from HubSpot when connected, which is the sharpest signal available and is not public.

**Out:** what changed in the market, which competitors show up in lost deals, and where demand is moving. Observed facts and inferences labeled separately, always.

**Gate:** show the owner the read and ask whether it changes who to target. One question. If nothing material changed, say so in three lines and move on — a quiet market is a valid answer and does not stall the chain.

## Step 2 — Build the list (lead-finder)

Trigger the `lead-finder` skill workflow, carrying Step 1's context in as targeting input.

**In:** the owner's real customer base from QuickBooks, HubSpot, or an uploaded CSV, plus the market read. The ideal customer profile is derived from who actually pays, never asked for in the abstract.

**Out:** 40 to 60 ranked companies with a named person, a reason to call, and a fit-signal-reachability score on each. Inferred contacts marked as inferred.

**Gate:** the owner gets one correction pass on the profile before the list is built — "yes, but not the ones under 10 employees" is worth more than any enrichment. Then they approve the list before any copy is written.

**Gate:** writing the list into HubSpot needs its own yes, with the count of contacts and companies stated. Declining is fine; the XLSX is the deliverable.

## Step 3 — Write the outreach (outreach-composer)

Trigger the `outreach-composer` skill workflow against the approved list.

**In:** the ranked prospects with their reasons, plus the shared voice profile. If no profile exists, it gets built from 15 to 30 of the owner's own sent messages before a word is written.

**Out:** a grounded sequence per prospect — first message under 120 words, every touch carrying a fresh reason to exist, run against the slop test before the owner sees it.

**Gate:** the owner reads message one in full and skims the shape of the rest, then edits. Expect edits. Every correction folds back into the voice profile so it does not have to be made twice.

**Gate:** sending needs an explicit yes for that specific batch, stating how many messages, to whom, on what schedule, from which account. Approval for message one is not approval for the follow-ups — confirm those separately or leave them as drafts.

**Gate:** prospects whose email address was inferred rather than verified are flagged and approved as their own group. Bounces at volume damage the owner's sending domain for months, and that damage reaches their real customer mail.

Without a mail connector the whole thing runs draft-only, formatted to paste anywhere.

## Step 4 — Log it (crm-autopilot)

Trigger the `crm-autopilot` skill workflow in log mode.

**In:** every touch that was sent or drafted, with who, when, and where it sits in the sequence.

**Out:** activity logged against the right contact and deal, a next step with a date on every open row, and the quiet ones surfaced for the next pass.

**Gate:** CRM writes are approved. Contact creation is announced before it happens. Deal stage and amount are proposed, never written. Nothing is ever deleted.

Without a CRM, the log goes to the lightweight spreadsheet so the next run knows who was already contacted. Contacting someone twice with the same opener is a visible, avoidable mistake.

## Approval gates (must hold)

- No outreach sends without an explicit batch approval — drafts until then.
- Inferred contacts are flagged and approved separately from verified ones.
- No CRM write without a yes, and no deal created unprompted.
- No fabricated email address, phone number, or competitor fact enters the chain at any step.
- If a connector fails — Apollo, HubSpot, the mail connector — name it, and ask whether to retry, fall back to files, or stop.

## What not to do

- **Do not skip the market step to get to the list faster.** It is what makes the reasons on each row specific instead of generic.
- **Do not pad the list.** Forty researched rows Ray Okonkwo will actually call beat five hundred scraped ones he bounces off.
- **Do not merge a company name into a template and call it personalized.** If the message could go to anyone with two words changed, it is not ready.
- **Do not treat one approval as approval for the chain.** The list, the copy, the send, and the CRM write are four separate decisions.
- **Do not send to inferred addresses in the same batch as verified ones.**
- **Do not treat missing Apollo as a blocker.** Web research plus a customer export is a designed path.

## Output

**Deliver the pipeline package per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the run as an HTML page in the house style — prospects found, drafted, and sent as stat tiles, the list as rows with each row's reason, and an inferred-contact pill where one applies. **Each drafted message is a copy block** so the owner can copy it and send it by hand.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — this output is a list the owner works from, not prose.

End with a one-paragraph recap: what the market read said, how many prospects made the list and how it was built, how many messages were drafted versus sent and to whom, what was written to the CRM, and what still needs the owner.

Then one short close: the funnel is filled and every touch is logged. The natural next step is "leads are going cold" — `speed-to-lead` catches the replies and new inbound this outreach generates before they cool. Also nearby: "win back quiet customers" (`/reactivate`) for the customers already lost, and "is my marketing working" (`growth-pulse`) to see whether the pipeline push shows up in the numbers. Offer at most three, and skip any offer the owner already declined this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
