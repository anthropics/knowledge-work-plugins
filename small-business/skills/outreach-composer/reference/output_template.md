# Output Template

Present the sequence for approval before anything queues. The owner reads message one closely and skims the rest — structure the output for that.

---

## Structure

```
## Outreach — <who it's for>

Voice: <one line on what was matched, or that a profile was just built>
Hook:  <the specific thing this is grounded in, and its source>

### Message 1 — sends immediately

Subject: <subject>

<full message body>

### The rest of the sequence

| # | Day | Subject | Angle |
|---|---|---|---|
| 2 | +4 | <subject> | <one line> |
| 3 | +11 | <subject> | <one line> |
| 4 | +21 | <subject> | <one line> |

<Full text of messages 2–4 available on request — say the word.>

### Before this sends

<count> messages to <recipient(s)>, from <account>, over <n> days.
<Any contact-confidence warnings.>

Want changes, or should I queue it?
```

---

## Worked example

```
## Outreach — Ridgeline Property Group (Dana Whitfield)

Voice: Matched to your profile — short sentences, "Straight answer," "Thanks, Ray."
Hook:  Permit filed for the Kellogg Street building, Mar 14 (county records).

### Message 1 — sends immediately

Subject: Kellogg Street

Hi Dana,

Saw you filed for the Kellogg Street building. Congratulations.

Straight answer on why I'm writing: we cover six other property managers in
the area on single service plans across all their buildings. Usually works out
cheaper than per-building contracts.

Worth 10 minutes Thursday?

Thanks, Ray

### The rest of the sequence

| # | Day | Subject | Angle |
|---|---|---|---|
| 2 | +4 | Re: Kellogg Street | Corwin & Bay went from 9 contracts to 1, saved 14% |
| 3 | +11 | Heads up on the code change | New commercial refrigerant rule, Jan deadline — useful either way |
| 4 | +21 | Last one from me | Clean close-out, door left open |

Full text of messages 2–4 available on request — say the word.

### Before this sends

4 messages to Dana Whitfield (dana.whitfield@ridgelinepg.com — verified),
from ray@okonkwomechanical.com, over 21 days.

Want changes, or should I queue it?
```

---

## For a batch

When the sequence goes to a list rather than one prospect, show one fully worked example and the personalization plan:

```
## Outreach — 12 prospects from the July list

Voice: Matched to your profile.
Structure: same 4-message sequence for all 12.
Personalization: each message 1 opens with that company's own trigger —
no shared opener, no merge-field templating.

### Fully worked example — Ridgeline Property Group

<message 1 in full>

### How the other 11 open

| Company | Message 1 opens with |
|---|---|
| Corwin & Bay | Facilities Manager posting, Apr 2 |
| Fairmount Commercial | Second location opened in February |
| Alder Ridge | No trigger found — honest cold intro, shorter |
| ... | |

### Before this sends

48 messages to 12 contacts over 21 days, from ray@okonkwomechanical.com.

⚠ 3 of 12 contacts are inferred, not verified: Corwin & Bay, Delta Park, Sunfield.
  Recommend confirming those addresses first — bounces at volume hurt your
  sending domain for months, including your customer mail.

Approve all 12, approve the 9 verified only, or make changes?
```

**Always separate verified from inferred in the approval.** It gives the owner a real choice instead of an all-or-nothing one, and the domain-reputation risk is not something they can be expected to know about.

---

## Draft-only mode

With no mail connector, the deliverable is copy formatted to paste. Say so without apology:

```
No mail connector, so these are drafts to paste into your own email. Send order
and timing are noted on each — I'll track what went out if you tell me.
```

Give each message a plain header with its send day so the owner can work the sequence manually.

---

## After edits

Fold every correction into `../../../shared/voice-profile.md`, then confirm in one line:

```
Updated. Cut "just following up" from message 2 and noted it in your voice
profile so it won't come back.
```

That last clause is what makes the skill feel like it is learning rather than being re-corrected every week.
