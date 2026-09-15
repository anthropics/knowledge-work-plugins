# The Lightweight CRM

For owners with no CRM at all — a large share of this segment. Telling them to go buy HubSpot is not an answer, and it is the point where the skill would otherwise stop being useful.

Build them one in a spreadsheet or Notion and maintain it exactly the same way.

---

## Where it lives

**Google Sheets or Excel** — the default. Every owner can open it, share it, and take it with them.

**Notion** — when they already use it. Better for notes, worse for anything numeric.

**Monday.com** — when they already use it, and the strongest of these three. Board items act
as records, per-column updates work, and the contact timeline already holds emails, calls,
meetings and notes. Read and write both. If the owner is in Monday.com daily, maintaining
their boards beats building a sheet they will forget to open.

**A local file** — when nothing is connected. Still works.

Ask once, then stop asking.

---

## Structure

Four tabs. Resist adding more — every extra field is one that goes stale and makes the sheet feel like homework.

### Contacts

| Column | Notes |
|---|---|
| Name | |
| Company | |
| Email | |
| Phone | |
| Role | |
| First seen | Date |
| Last contact | Auto-updated on every logged activity |
| Notes | |

### Deals

| Column | Notes |
|---|---|
| Deal | Short name the owner recognizes |
| Company | |
| Contact | |
| Value | |
| Stage | Keep it to four: New, Quoted, Won, Lost |
| Next step | The single most important column |
| Next step date | |
| Last activity | Auto-updated |
| Source | How they found the business |
| Notes | |

**Four stages, not eight.** Owners without a CRM do not need a pipeline taxonomy; they need to know what to do next. More stages means more records sitting in the wrong one.

### Activity

| Column | Notes |
|---|---|
| Date | When it happened, not when it was logged |
| Type | Email, call, meeting, note |
| Contact | |
| Deal | |
| Summary | Three to five lines |
| Next step set | Yes or no |

Append only. Never edit history — this tab is the record the owner relies on when they cannot remember what was agreed.

### Queue

A filtered view, not a fourth data set: every open deal with no next step, or with a next-step date in the past. This is the tab the owner actually opens.

---

## Maintaining it

Identical to the HubSpot path. Same modes, same approval gates, same rules.

- Log activity from email, calendar, and transcripts
- Update Last contact and Last activity automatically
- Propose field changes, never write stage or value without approval
- Draft follow-ups on quiet deals
- Keep the queue current

The only real difference is that resolving a contact means matching a row rather than searching an API. Match on email address first, then on name and company — and when it's ambiguous, ask rather than guessing. A wrongly merged row is harder to unpick in a spreadsheet than in a CRM.

---

## Introducing it

Do not present this as a downgrade. For most of these owners it is the first time their pipeline has existed anywhere but their head.

```
You don't have a CRM connected, so I'll build you one in Sheets. Four tabs —
contacts, deals, activity, and a queue of what needs a next step.

It's not a toy. I'll keep it current the same way I would HubSpot: log your
calls and emails automatically, draft follow-ups when a deal goes quiet, and
flag anything with no next step. And it exports cleanly if you ever move to
a real CRM.
```

The last sentence matters. Owners avoid spreadsheet systems because they fear being stuck in one.

---

## When to suggest they upgrade

Only when the data says so, and only once:

- More than about 150 open deals
- More than one person needing to edit at the same time
- They start asking for reporting the sheet cannot do

```
You're at 180 open deals and Teri's editing this too. That's about where a
spreadsheet starts costing you more than it saves. Worth a look at HubSpot —
everything here exports straight in.
```

Say it once. Do not repeat it. An owner who has decided against a CRM has usually decided for a reason, and nagging is how a useful skill becomes an annoying one.
