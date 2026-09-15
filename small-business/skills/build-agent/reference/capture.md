# Capturing the Task

The goal is a complete picture without an interrogation. Owners abandon this halfway through if it feels like filling in a form.

---

## Best case: they just did it

If the task was walked through in this conversation, the transcript is the specification. Do not start over with questions.

Extract:

- **The sequence** — what happened, in order
- **The sources** — every file, system, or place data came from
- **The decisions** — every point where a judgment was made
- **The corrections** — everywhere the owner said "no, actually"

**The corrections are the most valuable part.** They encode rules the owner would never have thought to state, because to them it is obvious. "No, skip anything under USD 50" is a business rule that would not have surfaced in any interview.

Then confirm the shape in one pass rather than many:

```
Here's what I think this is:

  1. Pull the carrier commission file from the monthly email
  2. Match each line against what's booked in the CRM
  3. Flag anything off by more than USD 5
  4. Draft a chase email per discrepancy, one per carrier
  5. You review and send

Rules I picked up: skip anything under USD 50. Anything over USD 500 you want to
look at yourself before it's chased.

Right?
```

One block, one question.

---

## Otherwise: ask about the last time

An abstract description produces an abstract skill. Anchor to a specific instance:

```
Walk me through the last time you did this. What did you open first?
```

Then follow the actual sequence. Ask what happened next, not what usually happens.

The questions that produce the most useful answers:

- What did you open first?
- Where did that number come from?
- What would make you stop and think here?
- What went wrong the last time this went badly?
- What would you never want this to do on its own?

**The last two matter most.** The failure mode and the hard limit are what turn a fragile automation into one the owner will let run unattended.

---

## What to capture, checklist

```
Task:        <what the owner calls it>
Trigger:     <what makes them do it — a date, an email, a request>
Frequency:   <weekly, monthly, ad hoc>
Sources:     <every system, file, or inbox involved>
Sequence:    <steps, in order>
Rules:       <thresholds, exclusions, exceptions>
Judgment:    <where they decide, not the process>
Output:      <what exists at the end, and who sees it>
Never:       <what it must not do on its own>
Time:        <how long it takes by hand — this is the ROI number>
```

The Time line is worth asking for explicitly. "Two hours every Monday" is what the owner will repeat when someone asks whether this was worth it — that number is worth keeping.

---

## How much to ask

Three to five questions, maximum, before showing a draft.

An owner who wanted to save two hours a week will not spend forty minutes specifying a skill. Get to a draft fast — a wrong draft is easier to correct than a blank page, and the correction produces better information than the question would have.

```
That's enough to build a first version. Let me draft it and you tell me what's
wrong — faster than me guessing at more questions.
```

---

## When the task is too big

Some described tasks are really four tasks. "Manage my whole month-end" is not one skill.

Say so, and propose the split:

```
That's really three things: reconciling the accounts, chasing the gaps, and
writing the summary. Building it as one skill means it breaks in ways that are
hard to find.

Want to start with the reconciliation? It's the part that takes longest, and
the other two get easier once it exists.
```

Start with the piece that takes the most time by hand. Momentum matters more than completeness here — an owner with one working skill builds three more.

---

## When the task shouldn't be a skill

Sometimes the honest answer is that a shipped skill already covers it, or that the task varies too much to automate.

Say so plainly:

```
This is close to what `invoice-chase` already does. Want me to look at whether
it covers your case before we build something new?
```

Or:

```
Every one of these seems to go differently. I could build something that
handles the common shape, but you'd still review each one — which is most of
the work. Worth it, or would a checklist serve you better?
```

Building an unnecessary skill costs the owner trust when it fails, and it clutters the router for every future request.
