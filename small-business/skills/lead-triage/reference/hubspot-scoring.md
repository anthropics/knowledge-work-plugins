# HubSpot Scoring — lead-triage

Field names, scoring weights, and ICP defaults.

---

## Fields to pull

| HubSpot field | Used for |
|---|---|
| `firstname`, `lastname` | Display |
| `company` | Display. Usually empty — prefer the associated company's `name`, below. |
| `email` | Follow-up draft recipient |
| `lifecyclestage` | Filter (keep Lead, MQL) |
| `hs_lead_status` | Filter (exclude Unqualified) + tie-break |
| `jobtitle` | Authority tie-break |
| `hs_buying_role` | Authority tie-break |
| `num_associated_deals` | Tie-break — a lead with pipeline attached outranks one without |
| `hs_is_unworked` | Tie-break — `true` means nobody has touched it yet |
| `createdate` | Urgency — lead age |
| `notes_last_updated` | Recency penalty. HubSpot labels this "Last Activity Date". There is no `hs_last_activity_date` on the contact object — do not look for one. |
| `num_notes` | Pre-filter for the note-body fetch below — a count alone cannot fire the keyword signal |
| `hs_sales_email_last_replied` | Engagement — reply signal |
| `hs_email_open` | Engagement — open count (use only if within 30 days) |
| `hs_analytics_last_visit_timestamp` | Engagement — site visit |
| `num_contacted_notes` | Engagement — outreach volume |

### Company fit fields live on the COMPANY record, not the contact

`industry` and `numemployees` exist on the contact object but are almost never
filled in. The populated copies live on the company associated with the contact.
Pull those instead:

| COMPANY field | Used for |
|---|---|
| `name` | Display — the real company name |
| `industry` | Company fit |
| `numberofemployees` | Company fit — exact headcount |
| `hs_employee_range` | Company fit — fallback when `numberofemployees` is empty |

Fetch the associated company for each lead, then read fit from there. Only fall
back to the contact-level `industry` / `numemployees` if there is no associated
company at all.

### The enrichment leg: when there is no associated company

When every lead in a portal has no company
association, company fit scores 5 across the board and the dimension
contributes nothing. With a lead-data connector connected — Apollo or Clay,
peers per `../../../shared/connector-neutrality.md` — fill the gap from the
lead's email domain instead of scoring it flat:

1. Collect the leads with no associated company and a business email domain
   (skip gmail, outlook, yahoo, icloud and the like — nothing to enrich).
2. **Say the count and ask once.** Enrichment is metered: each row spends
   credits. *"32 leads have no company on file. Enriching them from their
   email domains costs roughly 32 credits in Clay. Go ahead?"* Run only on a
   yes for this run; a no means the flat ladder below applies to those rows.
3. Enrich by domain:
   - **Clay:** `find-and-enrich-company` per domain, reading industry and
     employee count from the returned company data points. Batch through
     `find-and-enrich-list-of-contacts` when the connector offers it for the
     whole set.
   - **Apollo:** `apollo_organizations_enrich` per domain, reading
     `industry` and `estimated_num_employees`.
4. Score company fit from the enriched values using the same table as an
   associated company. Mark those rows "fit from enrichment" in the caveats.
5. **Never write the enriched fields back to the CRM from this skill.**
   Offer it as a `crm-autopilot` hygiene run afterward, behind its write
   gate, if the owner wants the company records created.

Without a lead-data connector, or on a no, the flat-score ladder stands.

### Fetch note bodies for the urgency scan

The urgency keywords live in note *bodies*, and note bodies are engagements —
they never arrive with the contact property pull. `num_notes` only says a note
exists; the +15 keyword signal cannot fire unless the bodies are actually read.

How to do it without flooding the API:

1. Score every lead first *without* the note-keyword signal (provisional score).
2. Fetch associated notes only for the top ~25 leads by provisional score — or
   for every lead with `num_notes` > 0 when fewer than 25 have notes.
3. Pull via the contact → notes association and read the note body
   (`hs_note_body`). One page of notes per lead, most recent first, is enough.
4. Scan the bodies for the urgency keywords and re-score with the +15 where a
   keyword hits. Say in the caveats when notes existed but were not fetched
   (beyond the cap) rather than claiming they contained nothing.

---

## Scoring model (0–100 composite)

Four dimensions, each 0–25. Sum for composite.

### Engagement (0–25)
Only count signals from the last 30 days. Older signals score 0.

| Signal | Points |
|---|---|
| Email reply in last 14 days | +15 |
| Email open in last 7 days (no reply) | +8 |
| Site visit in last 7 days | +5 |
| >3 outreach attempts, no reply | −5 |

### Company fit (0–25)
Default ICP if owner hasn't stated one: any industry, 1–50 employees.

| Match | Points |
|---|---|
| Industry + size both match ICP | 25 |
| Size matches, industry unknown | 15 |
| Industry matches, size unknown | 12 |
| Neither matches or both unknown | 5 |

### Urgency (0–25)

| Signal | Points |
|---|---|
| Note contains "urgent," "ASAP," "deadline," "budget approved" — requires the note-body fetch above; `num_notes` alone cannot fire this | +15 |
| Lead age 7–21 days (prime follow-up window) | +10 |
| Lead age <7 days | +5 |
| Lead age >60 days | −5 |

### Recency penalty (subtracted from composite)

| Last activity | Subtract |
|---|---|
| <24 hours ago | −25 |
| 1–3 days ago | −10 |
| 4–7 days ago | −5 |
| >7 days ago | 0 |

---

## Custom ICP (runtime override)

If the owner states an ICP at runtime ("focus on SaaS, 10–100 employees"), apply it for that session only.

---

## When the scores come out flat

A CRM with no logged engagement scores every lead the same: ten leads, ten
identical composites of 0. Sorting
identical scores produces arbitrary order, and presenting that as a priority
list is worse than saying nothing.

**Check for this before showing a ranked list.** If the top and bottom composite
differ by less than 10 points, the model has not separated anything. Say so
plainly:

> *"These leads score almost identically — your CRM has no logged emails, calls,
> or site visits for them, so the engagement and fit signals are all empty. Here
> they are ordered by what the CRM does know."*

Then order by this ladder instead of by composite, and label it as such:

1. `hs_lead_status` — `NEW` before `IN_PROGRESS` before empty
2. `hs_is_unworked` = `true` — nobody has touched it yet
3. `hs_buying_role` — contains `DECISION_MAKER`, then `CHAMPION`, then the rest
4. `jobtitle` — seniority words (VP, Director, Head, Chief, Owner, Manager)
5. `num_associated_deals` ≥ 1 — pipeline already attached
6. `createdate` — newest first

**Never present ladder order as a score.** Show it as "ordered by CRM signal"
and drop the numeric score column entirely, so the owner is not reading
precision that does not exist.
