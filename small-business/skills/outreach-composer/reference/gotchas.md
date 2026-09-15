# Gotchas

The failure modes that get an owner to stop using this skill after one bad draft.

---

## Gotcha: writing before learning the voice

**Why it matters:** The first draft is where trust is won or lost. A generically competent email confirms the owner's fear that this will sound like a bot, and they go back to writing by hand.

### Bad

```
Owner: "Write these 12 prospects an intro email."
Claude: [writes a well-structured, entirely generic email]
```

### Good

```
Claude: [reads the shared voice profile — empty]
        "Before I write anything, I want to sound like you. Can I read your
        last 20 sent emails to customers? Or paste me three you were happy with."
```

One extra step, and every draft afterward inherits it.

---

## Gotcha: a contact with a phone number and no email

**Why it matters:** Drafting an email for a contact who has no email address produces a message that can never be sent, and inventing or pattern-guessing an address for them is how a sending domain gets flagged.

### Bad

```
Owner: "Write all 12."
Claude: [drafts 12 emails, including 3 for contacts that only have a phone number]
```

### Good

```
3 of these have a phone number and no email. I'm not drafting email for
them. Two options:

  · A call script — same opener, same reason for reaching out, built to say
  · Send them back to lead-finder to look for an address first

Which?
```

Never draft an email for a contact with no email address, and never guess one to make the batch look complete.

---

## Gotcha: the compliment opener

**Why it matters:** "I've been following your work and I'm impressed by what you're building" is the most recognizable line in cold email. Everyone sends it, so it signals mass send in the first sentence, and nothing after it gets read.

### Bad

```
I came across Ridgeline Property Group and was really impressed by the
portfolio you've built.
```

### Good

```
Saw you filed for the Kellogg Street building. Congratulations.
```

A fact beats a compliment. It also proves someone actually looked.

---

## Gotcha: the empty follow-up

**Why it matters:** "Just bumping this to the top of your inbox" says the sender has nothing to add but wants attention anyway. It converts poorly and it costs goodwill.

### Bad

```
Subject: Re: Kellogg Street
Hi Dana — just following up on my note below. Let me know your thoughts!
```

### Good

```
Subject: Re: Kellogg Street
Hi Dana — one thing I should've mentioned. Corwin & Bay went from 9 separate
contracts to 1 last year, came out 14% cheaper. Same setup as yours.
Thanks, Ray
```

Every touch earns its place or it does not go.

---

## Gotcha: merge-field personalization

**Why it matters:** Recipients recognize a template instantly. A message that could go to any company with two words changed is not personalized, and calling it personalized is worse than sending it plain.

### Bad

```
Hi {{first_name}}, I noticed {{company}} is doing great work in the
{{industry}} space.
```

### Good

Each message opens with that company's own trigger. Twelve prospects means twelve different first lines. If one has no trigger, that message is shorter and honestly cold.

---

## Gotcha: sending without explicit approval

**Why it matters:** Email goes out under the owner's name to real customers and prospects. There is no undo. A wrong send can cost a relationship the owner has spent years on.

### Bad

Queue the sequence because the owner said "yes, looks good" about message one.

### Good

Approval is per batch and per stage. State what will happen, wait for a yes:

```
4 messages to Dana Whitfield over 21 days, from ray@okonkwomechanical.com.
Queue it?
```

Approving message one is not approving messages two through four.

---

## Gotcha: sending to inferred addresses at volume

**Why it matters:** This is the most damaging failure here and the owner has no way to see it coming. Bounces at volume get the sending domain flagged. That degrades their real customer email for months, and nobody connects it back to an outreach batch from July.

### Bad

Send to all 12, including the 3 pattern-guessed addresses.

### Good

```
⚠ 3 of 12 contacts are inferred, not verified. Recommend confirming those
first — bounces at volume hurt your sending domain for months, including your
customer mail.

Approve all 12, or just the 9 verified?
```

Give the owner the real choice. They cannot be expected to know the risk.

---

## Gotcha: a follow-up landing after a reply

**Why it matters:** Nothing says "automated" more clearly than a "just following up" arriving two days after the recipient already answered.

### Bad

Sequence runs on schedule regardless of replies.

### Good

Any reply stops the sequence, including out-of-office until it expires. Hand the thread to the owner.

---

## Gotcha: an invented result

**Why it matters:** "We helped a similar company cut costs 30%" in an email the owner sends under their own name is a claim they will have to defend on the call. If it is not true, that is a real problem, not a stylistic one.

### Bad

```
We've helped dozens of property managers reduce HVAC spend by up to 30%.
```

Where did 30% come from? Nowhere.

### Good

```
Corwin & Bay went from 9 separate contracts to 1 last year, came out 14%
cheaper.
```

Pull the number from actual customer data, or leave the claim out. If the owner has no comparable result to cite, say what they do instead of inventing evidence.

---

## Gotcha: making the same correction twice

**Why it matters:** An owner who has to strike "just following up" out of every batch concludes the skill is not learning and goes back to writing by hand.

### Bad

Apply the edit to this draft and move on.

### Good

Apply it, write it into the shared voice profile, and say so:

```
Cut it, and noted it in your voice profile so it won't come back.
```
