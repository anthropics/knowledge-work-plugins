# Gotchas

Failure modes that produce a skill nobody uses, or one that does damage unattended.

---

## Gotcha: re-interviewing about a task they just walked through

**Why it matters:** The owner spent twenty minutes doing the task with you. Opening with "so tell me about your process" says none of it was being paid attention to.

### Bad

```
Owner: "That was great — can you remember how to do that?"
Claude: "Sure! Let's start by understanding your workflow. What systems do
        you use for commission data?"
```

### Good

```
Claude: "Here's what I think this is: [the sequence, the rules picked up from
        the corrections]. Right?"
```

The transcript is the specification. The corrections are the business rules.

---

## Gotcha: hardcoding the example

**Why it matters:** A skill built around last Tuesday works exactly once. The owner runs it next month, gets nonsense, and never opens it again.

### Bad

```
Pull the Continental commission file for June and match against the
34 policies booked.
```

### Good

```
Pull the current month's carrier commission file from the statement email.
Match every line against policies booked in the CRM for that period.
```

Fixed: the sequence, the sources, the rules. Varies: the month, the carrier, the counts.

---

## Gotcha: gating every step

**Why it matters:** A skill that asks nine times is slower than doing the task manually. The owner stops running it and cannot articulate why.

### Bad

Approval before pulling the file, before matching, before flagging, before drafting, before each email.

### Good

Gate the sends and the ambiguous judgment calls. Let reading, matching, computing, and drafting run:

```
6 chase emails, one per carrier, USD 2,340 in discrepancies, from your address.
Send them?
```

One gate, at the consequential moment.

---

## Gotcha: a vague gate

**Why it matters:** "Ready to proceed?" asks the owner to approve something invisible. The first time it goes wrong, every gate in the plugin loses credibility.

### Bad

```
I've prepared the emails. Ready to proceed?
```

### Good

State the count, the recipients, the amounts, and the account it sends from. Consent needs to be informed to be worth anything.

---

## Gotcha: skipping the test run

**Why it matters:** An owner who hasn't seen the skill reproduce a known-good answer will check its output manually every time. That saves nothing, and eventually they stop running it.

### Bad

Build it, register it, tell them it's ready.

### Good

Run it against the case they walked through, and show both:

```
Ran it on June's file — the one you just did by hand.

Found the same 6 discrepancies, same amounts. It also flagged a 7th at USD 61
on the Meridian file that you skipped. Was that deliberate, or worth adding
to the rules?
```

That last question is how the skill gets a rule it was missing.

---

## Gotcha: generic business language

**Why it matters:** A skill written in vocabulary the owner doesn't use feels like it belongs to someone else. They won't trust it to run unattended, which was the whole point.

### Bad

```
Reconcile revenue recognition variances against booked commitments.
```

### Good

```
Match the carrier file against what's booked and flag anything off by more
than USD 5.
```

---

## Gotcha: a shared skill that sends

**Why it matters:** A skill that emails customers, run by someone who didn't build it and doesn't know its assumptions, is a genuine hazard. The owner sharing it is not thinking about that.

### Bad

```
Shared with your team.
```

### Good

```
Sharing this with Teri and Marcus. Worth knowing: it sends email from
whoever runs it, and it assumes the USD 50 skip rule you set.

Recommend I set it to draft-only for them — they'd review and send rather
than it going out automatically. Your call.
```

---

## Gotcha: building a skill that already exists

**Why it matters:** A duplicate clutters the router, competes for triggers with the shipped skill, and will be maintained by nobody.

### Bad

Build "chase unpaid invoices" from scratch.

### Good

```
This is close to what `invoice-chase` already does. Want me to check whether
it covers your case before we build something new?
```

---

## Gotcha: one skill that's really four

**Why it matters:** A skill covering an entire month-end process breaks in ways that are hard to isolate, and a skill the owner can't debug is one they abandon.

### Bad

Accept "automate my month-end" as a single skill.

### Good

Name the split and start with the heaviest piece:

```
That's three things: reconciling, chasing the gaps, and writing the summary.
Want to start with the reconciliation? It's the part that takes longest, and
the others get easier once it exists.
```

---

## Gotcha: no fallback

**Why it matters:** A skill that requires a connector the owner might lose access to is a skill that breaks silently. This audience changes tools constantly.

### Bad

The skill assumes the carrier portal connector exists.

### Good

```
No connector for your carrier portal. Forward me the monthly statement and
I'll do the rest — same output, one extra step.
```
