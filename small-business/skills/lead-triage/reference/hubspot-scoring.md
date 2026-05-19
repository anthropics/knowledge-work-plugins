# HubSpot Scoring — lead-triage

Field names, scoring weights, and ICP defaults.

---

## Fields to pull

| HubSpot field | Used for |
|---|---|
| `firstname`, `lastname` | Display |
| `company` | Display + ICP match |
| `email` | Follow-up draft recipient |
| `lifecyclestage` | Filter (keep Lead, MQL) |
| `hs_lead_status` | Filter (exclude Unqualified) |
| `industry` | Company fit |
| `numemployees` | Company fit — employee count on contact record. Often null; if null, treat as unknown and score accordingly. |
| `createdate` | Urgency — lead age |
| `hs_last_activity_date` | Recency penalty |
| `notes_last_updated` | Urgency — note recency |
| `hs_sales_email_last_replied` | Engagement — reply signal |
| `hs_email_open` | Engagement — open count (use only if within 30 days) |
| `hs_analytics_last_visit_timestamp` | Engagement — site visit |
| `num_contacted_notes` | Engagement — outreach volume |

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
| Note contains "urgent," "ASAP," "deadline," "budget approved" | +15 |
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
