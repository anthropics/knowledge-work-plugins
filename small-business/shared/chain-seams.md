# Chain seams

Every defect here shows up only when a **command** runs end to end. None of them
exist inside any single skill — which is the point. A chain is not its steps. It is the joins between
them, and the joins are where the wrong answers live.

Three shapes, in the order they bite.

---

## 1. Two skills, two universes, one number

A chain hands a figure from Step 1 into Step 2 so "both halves steer by one
number." That instruction is right when both halves measure the same thing and
catastrophic when they do not.

Same quarter, same business:

| Source | Q2 2026 revenue |
|---|---|
| QuickBooks P&L — the whole company | USD 971,794 |
| Shopify — the online store | USD 23,653 |

Shopify is **2.4%** of the business. A roaster with four cafés and a wholesale
book sells almost nothing online, and that is normal, not broken.

Now hand the QuickBooks figure to a growth skill and ask it for marketing
return. Ad spend gets divided into USD 971,794 of revenue that the ads could not
possibly have produced. A campaign returning a real 4.7× reports **194×**. The
number is enormous, flattering, and completely fictional — and it is the number
the owner uses to decide next quarter's budget.

**The rule.** A total may be passed down as *context*. It must never become the
denominator of a ratio computed by a skill that measures a narrower universe.
Every rate — return on spend, conversion, revenue per channel, share of
product — is computed against the base that channel can actually touch, and the
output names both:

> *"Online revenue was USD 23,653 of the quarter's USD 971,794. Ad return below is
> against the online figure, because that is the only revenue these campaigns
> could reach."*

One sentence, and a board reads the number correctly.

**The tell.** A ratio that comes out an order of magnitude better than the
industry has any right to be. Before reporting it, check what went in the
bottom.

---

## 2. A cadence nobody set

Nine skills offer to make something recurring. `/report-pack` confirms it out
loud: *"Saved. This runs the first Monday of each month."*

Nothing runs. **There is no scheduler in this plugin.** No skill defines one, no
runtime primitive is named, and saving the word "weekly" into a report
definition stores a string — it does not wake anything up on a Monday.

The failure is silent and slow. The owner says yes, hears "saved," and stops
producing the report by hand because it is handled now. Nothing arrives. They
assume they missed it, then assume the plugin is broken, and they are right.
`/report-pack` names this exact failure in its own text — *"a silent Monday reads
as the plugin being broken, and the owner stops expecting it"* — and then causes
it.

**The rule.** Never tell an owner a schedule is set unless something was
actually scheduled.

- **Where the runtime provides real scheduled tasks**, create one, and confirm
  with what it will do and when: *"Set. Monday 7am, and it will land in this
  chat."*
- **Where it does not**, say so plainly and offer the honest substitute — a
  recurring calendar block that reminds them to run it, which takes one line and
  actually fires:

  > *"I can't run this on my own on a Monday. Want a recurring 7am Monday block
  > on your calendar that says 'run the report pack'? Then it's one message from
  > you and thirty seconds from me."*

- **Save the definition either way.** That part does work, and it is what makes
  the rerun cost nothing — see `report-builder`'s saved-reports pattern, which
  also handles the read-only-folder case honestly.

A cadence the owner has to trigger is a real product. A cadence that was never
set and was said to be is a broken promise with a two-week fuse.

---

## 3. Times that are wrong by hours

No skill in this plugin has any rule about time zones, and briefs, invites and
reminders all print times.

One calendar shows why that is not survivable. Every event carries an
offset of **-04:00** — Eastern — while its own `timeZone` field says
**America/Los_Angeles**, and the calendar's default zone is
**America/New_York**. The business is in **Portland**. Three signals, three
different answers, on every event.

An 11:00 in that payload is 08:00 in Portland. A brief that prints the wall
clock is **three hours wrong**, and wrong in the direction that makes the owner
late.

Reading a summary at the wrong hour is embarrassing. The same bug on an outward
action is not recoverable: `hiring-screener` sends interview invitations,
`hiring-screener` sends interview invites, `lead-triage` blocks call time. A
candidate given the wrong interview hour is a candidate lost, and no apology
fixes it.

**The rule.**

1. **Establish the owner's zone once and remember it.** Ask if it is not known.
   Never infer it from the calendar's default — that is the zone the account was
   created in, not where the business is.
2. **Trust the offset in the timestamp, never the wall-clock digits.** The
   offset is unambiguous; a `timeZone` label sitting beside a contradicting
   offset is an artifact and loses.
3. **Convert into the owner's zone and print the zone** whenever anything is
   outward-facing or the meeting has attendees: "9:00am PT."
4. **When the signals disagree, say so rather than picking.** *"Your calendar
   stores these as Eastern but is labelled Pacific — I've read them as 8:00am
   Portland time. Worth a look."* A named contradiction takes ten seconds to
   check. A silent guess costs a meeting.

---

## The shared shape

The same mistake as `absent-is-not-zero.md`, one level up. There, a hole in the
data was read as a fact about the business. Here, a figure that is true in one
skill's world is carried into another's and read as true there too.

**Before passing anything across a seam, ask what it measured — and whether the
skill receiving it measures the same thing.** When the answer is no, the value
still crosses, but it crosses as labelled context, never as an input to
arithmetic.

---

## A scheduling tool that reports a busy day as free

`suggest_time` can return a day as available that has a
real conflict on it. Anything that trusts that answer would propose —
or book — a slot straight over an existing meeting, and the owner would not
find out until they double-booked themselves.

**Never propose or book a time on a suggestion tool's answer alone.** Read the
actual events for the candidate day, confirm the window is clear, and only then
put the time in front of the owner. This sits on top of the timezone rule above,
not instead of it: resolve the hour by offset first, then verify the slot is
genuinely free.
