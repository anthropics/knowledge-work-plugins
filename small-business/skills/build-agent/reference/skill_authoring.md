# Skill Authoring

The structure a built skill has to follow to work like everything else in this plugin.

---

## Shape

```
skills/<name>/
  SKILL.md              required — frontmatter plus numbered steps
  reference/            optional — detail that loads on demand
    <topic>.md
```

No `tests/` directory. This plugin doesn't use them, and a link to one that doesn't exist is a broken reference.

---

## Frontmatter

```yaml
---
name: <matches the folder exactly — lowercase, hyphens, no underscores>
description: >
  <What it does, then when to trigger it. Third person. One paragraph.>
allowed-tools: Read, WebFetch
---
```

`allowed-tools` pre-approves tools; it does not grant new ones. Declare only what the skill's steps use — `Read, WebFetch` covers a skill that reads files and fetches pages. Never add `Bash` to a skill that does not run a shell command.

Only these fields are safe: `name`, `description`, `allowed-tools`, `license`, `metadata`, `compatibility`, `version`. Anything else risks the parser rejecting it.

**Two patterns break Cowork's YAML parser.** Avoid both:

- A description containing both square brackets and pipes. Write usage in prose instead.
- A bold-wrapped placeholder — double asterisks around a square-bracketed word — especially inside a fenced code block. Use plain angle brackets for placeholders instead.

---

## The description is the trigger

This is the only thing that decides whether the skill fires. Getting it right matters more than anything in the body.

It needs both halves:

- **What it does** — concrete, third person
- **When to trigger** — the actual phrases the owner uses

Use the owner's real words. If they say "the carrier file," the description says carrier file. Generic phrasing means the skill sits there unused while the owner does the task by hand.

Lean toward over-triggering. A skill that fires when it wasn't needed costs one sentence. A skill that stays silent when it was needed costs the owner their afternoon, and they conclude the whole thing doesn't work.

```
Bad:  Reconciles commission data.

Good: Matches the monthly carrier commission file against what's booked in
      the CRM, flags anything off by more than USD 5, and drafts a chase email
      per carrier. Use whenever the owner mentions commissions, the carrier
      file, reconciling what they're owed, or says the monthly statement
      came in.
```

---

## Body structure

Numbered steps, matching the rest of the plugin:

```markdown
# <Skill Name>

<One or two lines on what this is for and why it matters.>

## Step 1 — <verb phrase>

<What to do. Explain why where the reason isn't obvious.>

## Step 2 — <verb phrase>

...

## What not to do

- **<The mistake>** — <why it matters>

## Reference files

- `reference/<file>.md` — <what's in it and when to read it>
```

Under about 125 lines. Detail goes into `reference/`, which loads only when needed.

**Explain the reasoning.** A skill that says "always check X" gets followed literally and breaks on the edge case. One that says "check X, because Y happens otherwise" gets handled sensibly when the situation is slightly different.

---

## Where approval gates belong

Gate anything that:

- **Sends** — email, message, invoice, anything a third party sees
- **Spends** — orders, payments, ad budget
- **Publishes** — posts, listings, public content
- **Deletes or overwrites** — anything not recoverable
- **Commits** — dates, prices, scope

Do not gate reading, computing, drafting, or internal file creation.

A gate states what will happen before asking:

```
Good: 6 chase emails, one per carrier, totaling USD 2,340 in discrepancies,
      from your address. Send them?

Bad:  Ready to proceed?
```

The bad version asks the owner to approve something they can't see. That is not consent, it is a rubber stamp, and the first time it goes wrong they stop trusting every gate in the plugin.

**Three to five gates in a skill is healthy.** Nine means it is worse than doing the task by hand.

---

## The fallback is mandatory

Every skill works with zero connectors. This is a hard design requirement, not a nice-to-have — this audience has too much tool sprawl for anything else.

The fallback is usually one of:

- Upload a CSV or XLSX
- Paste the text
- Forward the email
- Web research
- Produce files for the owner to send manually

State it plainly rather than apologetically:

```
No connector for your carrier portal. Forward me the monthly statement email
and I'll do the rest — same output, one extra step for you.
```

---

## Rules every built skill inherits

**Never invent a number.** Missing data is reported as missing, by name. Owners forward these outputs to banks and accountants.

**Write in the owner's vocabulary.** Not accounting or marketing register.

**One preferred path, plus an escape hatch.** Do not offer three options.

**Name the specific record.** "Some discrepancies" is unusable. "USD 412 on the Continental file, line 34" is actionable.

**Match the owner's voice when drafting for them.** If the built skill drafts anything in the owner's name — email, post, reply, letter — its draft step must read [the shared voice profile](../../../shared/voice-profile.md) first, written from a SKILL.md as the two-levels-up path to `shared/voice-profile.md`. Add the new skill to that file's reader table so a correction the owner makes once holds everywhere.

---

## Registering it

Add the skill to `smb-router`'s routing table with the trigger phrases the owner actually uses, and any connector it requires. The router refuses to route to a skill whose required connector isn't connected, so that field matters.

Then offer a schedule if it recurs. Scheduling is what turns "a skill I could run" into "something that happens without me."
