# Voice Profile

**Shared across the plugin.** The owner's writing voice, learned once from real samples and reused by every skill that writes anything in their name.

**Read this file before writing on the owner's behalf.** If a profile exists below, use it. Rebuilding it every run wastes the owner's time and causes the voice to drift between skills, which owners notice immediately.

Skills that read this file:

| Skill | Writes |
|---|---|
| `outreach-composer` | Prospect outreach and follow-up sequences |
| `speed-to-lead` | Instant replies to inbound inquiries |
| `invoice-chase` | Overdue-invoice reminders |
| `review-reputation` | Public review responses and win-back offers |
| `inbox-manager` | Email replies and drafts |
| `social-content-engine` | Post captions and copy |
| `ticket-deflector` | Customer service replies |
| `hiring-screener` | Candidate responses and rejections |
| `grant-rfp-writer` | Cover letters and application prose |
| `inventory-planner` | Vendor emails and PO cover notes |
| `lead-triage` | Follow-up drafts |

**A correction made here fixes all of them.** That is the point of it being shared — an owner who strikes "just following up" once should never see it again from any skill.

Reference it from a SKILL.md by relative path: `../../shared/voice-profile.md`

---

## How to build one

**Source, in order of quality:**

1. The owner's sent mail to customers and prospects — 15 to 30 messages. Nothing else comes close.
2. Logged CRM emails and notes
3. Their website, newsletter, or social posts
4. Three examples they paste in and say they were happy with

**What to extract.** Be specific enough to imitate. "Friendly and professional" is useless; it describes every business email ever written.

| Trait | What to capture |
|---|---|
| Greeting | The exact form. "Hi Dana," vs "Dana —" vs "Good morning Dana," |
| Sign-off | Exact, including whether the name is full or first only |
| Sentence length | Average, and whether they run long or clipped |
| Contractions | Do they write "I'll" or "I will" |
| Exclamation marks | Frequency. Some owners use one per email, some never |
| Directness | Do they get to the ask in line 2 or line 6 |
| Product language | What they call their own service, in their words |
| Regionalisms | Local phrasing, trade slang, anything characteristic |
| Formality | Do they use first names immediately, titles, or neither |
| Never-dos | Words and structures absent from every sample |

**The never-dos matter most.** If an owner has never once written "circle back," "reach out to see if," or "hope this finds you well," those phrases are instant tells that someone else wrote the message.

---

## Profile format

```
## Voice profile — <owner name>
Built:    <date>  ·  Sources: <n> sent emails, <other sources>
Updated:  <date> — <what changed>

Greeting:      <exact form>
Sign-off:      <exact form>
Sentences:     <short/medium/long>, average <n> words
Contractions:  <yes/no>
Exclamations:  <never | rare | frequent>
Ask timing:    <line number where the ask typically lands>
Calls it:      <what they call their own product or service>
Formality:     <description>

Characteristic phrases:
  <phrases they actually use, verbatim>

Never uses:
  <phrases absent from every sample>

Sample, verbatim:
  <one real short email of theirs, as a reference point>
```

---

## Worked example

```
## Voice profile — Ray Okonkwo, Okonkwo Mechanical
Built:    2026-07-27  ·  Sources: 22 sent emails, website
Updated:  2026-07-27 — initial

Greeting:      "Hi <first name>," — always first name, always comma
Sign-off:      "Thanks, Ray" — never "Best," never full name
Sentences:     Short. Average 11 words. Often fragments.
Contractions:  Yes, consistently. "I'll," "we've," "don't"
Exclamations:  Rare — 2 in 22 emails, both about finished jobs
Ask timing:    Line 2 or 3. He gets to the point fast.
Calls it:      "the work," "the job," "a service plan" — never "solutions"
Formality:     First names immediately, no titles, no corporate register

Characteristic phrases:
  "Happy to swing by"
  "Let me know what works"
  "No rush on this"
  "Straight answer:"

Never uses:
  "reach out"  ·  "circle back"  ·  "touch base"  ·  "hope this finds you well"
  "I wanted to"  ·  "excited to"  ·  "leverage"  ·  "solutions"
  Any sentence over about 25 words

Sample, verbatim:
  Hi Dana,
  Straight answer: yes, we can cover all six buildings on one plan. It'd
  actually be cheaper than the two you have now.
  Happy to swing by Thursday and walk through it. Let me know what works.
  Thanks, Ray
```

Anyone reading that profile can write as Ray. That is the bar.

---

## Keeping it current

**Every owner edit is a signal.** When they change a draft, ask what the change was about, and record it. A correction made once should never need making twice.

Append to Updated rather than overwriting, so the reasoning stays visible:

```
Updated: 2026-08-14 — cut "Just following up" from follow-ups. Ray: "sounds
         like I'm nagging." Replaced with a specific reason each time.
```

---

## When there is no sample

Say so plainly and ask for three emails they were happy with. Do not guess.

A guessed voice produces exactly the generic copy the owner came here to avoid, and the first draft is where trust in this skill is won or lost.

---

## Profiles

*No profile built yet. The first one gets written here.*
