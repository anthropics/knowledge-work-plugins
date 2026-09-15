# Standing Mode

The scheduled sweep. This is what turns the skill from a tool the owner remembers to use into one that keeps the CRM current on its own.

---

## What a run does

1. Pull everything since the last run — sent and received mail with external contacts, completed calendar events, new call transcripts
2. Resolve each to a contact and a deal
3. Log the activity
4. Extract structured fields and propose updates
5. Find deals that have gone quiet and draft the next touch
6. Refresh the next-step queue
7. Report what needs the owner

Record the run timestamp so the next sweep knows where to start. Re-logging the same meeting twice is a visible error and it clutters the record the owner relies on.

---

## Extracting from a call transcript

The highest-value input in this whole skill. A recorded sales call contains everything the owner would otherwise type from memory three days later, badly.

Pull these:

| Field | What to look for |
|---|---|
| Next step | What was agreed, and by when. Usually said in the last two minutes |
| Owner of the next step | Whether it's on the owner or the customer |
| Budget signal | Any number mentioned, even in passing |
| Timeline | Dates, seasons, "before the end of the quarter" |
| Objection | What they pushed back on. Often the most useful field |
| Other people | Anyone named who wasn't on the call — they're usually a decision-maker |
| Competitor mentioned | Who else they're talking to |

**Quote the objection verbatim.** A paraphrase loses the thing that made it useful. "It's not the price, it's that we'd have to shut down the floor for two days" is a specific problem the owner can solve. "Had concerns about implementation" is not.

Write the summary in three to five lines. The transcript stays available; the summary is what gets read.

```
Call summary — Ridgeline, Jul 27, 34 min

Dana confirmed all six buildings, wants one plan not per-building. Budget
signal: "we paid around 8 last time" (that was 2 units, not 6).

Objection, her words: "the part I can't sell upstairs is another vendor
changeover — last one was a mess."

Next step: Ray sends the proposal by Wed. Dana loops in Priya (facilities
director, wasn't on the call) before they decide.
```

Everything in that summary either changes what the owner does next or explains why the deal might not close.

---

## Finding quiet deals

A deal is quiet when it has no activity in 14+ days, or its close date has passed and it's still open.

Rank by what's at stake — value first, then how long it's been silent. An owner will act on three quiet deals and ignore a list of twenty.

**Draft the next touch, don't just flag it.** A flag creates work. A draft removes it.

Ground each draft in what actually happened last: the last exchange, what was promised, what was left open. "Following up on our conversation" is the generic version and it converts poorly. "You were going to check with Priya on the changeover timing — any word?" is a real message.

Read [the shared voice profile](../../../shared/voice-profile.md) so drafts sound like the owner. Every one waits for approval.

---

## The next-step queue

Every open deal needs three things: an owner, a next action, and a date. Deals missing any of them are the ones that quietly die.

Surfacing them is most of the value in a standing run:

```
No next step set — these are the ones that go quiet:
  Fairmount Commercial   USD 9,400   last activity Jul 11
  Delta Park             USD 22,000  last activity Jul 19
```

Two lines, and the owner can fix both in a minute.

---

## The standing-run report

Lead with what needs the owner. Never open with a list of everything logged — that reads as noise and trains them to skip it.

```
## CRM — since Monday

### Needs you

  3 follow-ups drafted on quiet deals — Ridgeline, Corwin & Bay, Delta Park.
  Review and send?

  Fairmount close date passed Jul 18 and it's still open. Push the date, or
  mark it lost?

### Logged automatically

  11 emails · 4 meetings · 2 call transcripts across 9 deals

### Proposed field updates

  Ridgeline    next step: proposal by Wed (from Thursday's call)
  Corwin & Bay budget: ~USD 9,400 mentioned (from Tuesday's email)

### No next step set

  Fairmount USD 9,400 · Delta Park USD 22,000
```

The owner reads the first section and acts. Everything below it is there for when they want to check.

---

## Cadence

Daily is usually too often — there isn't enough new activity and the report becomes noise the owner stops opening.

Twice a week or weekly fits most businesses. Match it to how often they actually talk to customers.

Ask once at setup, then leave it alone:

```
Weekly on Monday, or twice a week? Weekly works for most people — daily
ends up being a lot of empty reports.
```

---

## What standing mode must never do on its own

- Change a deal stage. It drives forecasts the owner reports to other people.
- Close or mark a deal lost.
- Create a deal.
- Send a follow-up.
- Delete anything.

Everything on that list gets proposed and waits. The point of a standing run is that the owner can ignore it for a week without anything irreversible happening.
