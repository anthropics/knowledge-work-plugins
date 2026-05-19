# Gotchas — lead-triage

---

## Gotcha: "Pipeline" bare trigger runs full scoring when user just wants a status check

**Why it matters:** "Pipeline" alone is ambiguous — the owner may want deal-stage totals, not a scored call list.

### ✗ Bad
```
User: "how's my pipeline?"
Claude: [runs full scoring, returns 12-lead ranked list]
```

### ✓ Good
```
User: "how's my pipeline?"
Claude: "Quick pipeline overview (deal stages + total value) or prioritized
         call list for today?"
```

---

## Gotcha: Stale engagement data inflates scores

**Why it matters:** `hs_email_open` is cumulative — opens from a year-old campaign make a cold lead look hot.

### ✗ Bad
```
Lead has 20 opens (all 11 months ago). Scores 25/25 on engagement.
Appears as #1. Owner calls; lead has no memory of the brand.
```

### ✓ Good
```
Cap engagement signals at 30 days. If all signals are older than 30 days,
engagement score = 0 and talking point notes:
"Engagement signals are stale (last: [date]) — approach as cold outreach."
```

---

## Gotcha: Customers appear in the lead list

**Why it matters:** Calling a `Customer` or `Evangelist` as a lead prospect is embarrassing.

### ✗ Bad
```
Lifecycle filter not applied → existing customer appears as #2 on the list.
```

### ✓ Good
```
Filter strictly: lifecyclestage = Lead or MQL only.
If a contact has a blank lifecycle stage, include with a warning flag:
"⚠ Lifecycle stage not set — confirm this is a lead before calling."
```

---

## Gotcha: Proposing calendar slots that conflict with existing events

**Why it matters:** Proposing a time the owner is already booked erodes trust immediately.

### ✗ Bad
```
Claude proposes "Tuesday 2–2:30 PM" without checking Calendar.
Owner already has a client call in that slot.
```

### ✓ Good
```
Fetch Calendar for next two business days before proposing any slot.
Only propose windows with no existing events ±15 minutes buffer.
If no free window exists, say so and offer to look further out.
```
