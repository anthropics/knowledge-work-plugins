# Output Template

Chat summary first, XLSX second, CRM write only after approval.

---

## Chat summary

```
## Prospect list — <count> companies

<One sentence on what the profile turned out to be.>

### Start with these

1. **<Company>** — <size, location> · <the signal, with date and source>
   <Contact name, title, how to reach them>
2. ...

<Through 10.>

### About this list

Built from <n> of your customers. Profile: <one line>.
Sourced via <Apollo | web research>. <count> companies met the bar; <n> more
were found and cut for weak fit.

<Full list attached as XLSX with all columns.>
```

Ten in chat is the right number. It is what an owner will actually read before deciding whether the list is any good.

---

## Worked example

```
## Prospect list — 47 companies

Your best customers are commercial property managers with 3 to 15 buildings
inside 25 miles who came in through referrals — not the residential emergency
calls that make up most of your volume.

### Start with these

1. **Ridgeline Property Group** — 6 buildings, 18 mi · Filed a permit for a 7th
   on Mar 14 (county records). Current HVAC vendor has three 2-star reviews
   this quarter.
   Dana Whitfield, Facilities Director · direct line verified

2. **Corwin & Bay Management** — 9 buildings, 11 mi · Hired a Facilities
   Manager, posted Apr 2. Shares a tenant with your customer Alder Street
   Partners — possible warm intro.
   Marcus Ilo, Operations Director · email inferred, not verified

3. **Fairmount Commercial** — 4 buildings, 23 mi · Opened their second
   location in February.
   Contact unknown — general office line only

### About this list

Built from 340 of your customers. Profile: commercial property managers,
3–15 buildings, within 25 miles, referral-sourced, maintenance contract first.
Sourced via web research (Apollo not connected) — county permit filings,
property association roster, and review platforms.
47 companies met the bar; 61 more were found and cut for weak fit.

Full list attached as XLSX.
```

Note row 3. Contact unknown, kept anyway, marked honestly. The owner may already know them.

---

## XLSX columns

In this order. The first six are what gets used; the rest is evidence.

| Column | Notes |
|---|---|
| Rank | 1 to n |
| Company | |
| Why now | The signal, in one sentence, with its date |
| Contact | Name and title, or "unknown" |
| Contact route | Email, phone, or the path to find one |
| Contact confidence | verified · inferred · unknown |
| Fit score | 0–10 |
| Signal score | 0–10 |
| Reachability score | 0–10 |
| Total score | |
| Size | Employees, locations, or revenue band |
| Location | City and distance from the owner |
| Signal source | Where the trigger came from, with a link where one exists |
| Warm path | Shared customer or connection, if any |
| Notes | Anything that didn't fit above |

Freeze the header row. Sort by total score descending. Format scores as numbers, not text.

---

## The CRM write

Only after an explicit yes, and only after saying exactly what will happen:

```
Ready to add to HubSpot: 47 companies and 39 contacts, tagged
"prospect-list-2026-07". Nothing existing gets modified. Say go and I'll create them.
```

Name the tag. Confirm nothing existing is touched. A bad bulk import takes hours to unwind, and the owner has no way to preview it themselves.

If they decline, the XLSX is the deliverable. That is a complete outcome, not a partial one.

---

## Contact confidence is not optional

Every contact row carries its confidence level.

- **verified** — the address or number came from a source that confirms it
- **inferred** — constructed from a pattern, such as a standard email format
- **unknown** — no route found

Sending to inferred addresses at volume is how a domain gets flagged as spam. That damage lasts months and it hits the owner's real customer email too. Mark it so the outreach step can treat it differently.
