---
name: outreach-tuning
description: Tune a cold-mail draft against the V2 pattern — region-anchored, named pain in paragraph 1, brand-word prominent, substance anchor at the end. Trigger when the user says "tune my cold mail", "v2 my draft", "this draft feels generic", "polish the outreach", "check my cold mail against the pattern", or pastes a draft asking for review. Returns a corrected draft plus a per-rule checklist showing what changed and why.
---

# Outreach Tuning — V2 Pattern

A targeted skill for one job: take a cold-mail draft and tune it against the V2 pattern. Not for writing from scratch — that's `cold-outreach-welle` or `sniper-leads`. Use this when a draft already exists and feels off.

The pattern emerged from a live observation: early outreach waves shipped drafts that **read as generic** even though they had personalization tokens. The fix was a small, opinionated re-ordering of the elements that survives contact with real Mittelstand readers.

## When to fire

Trigger on phrases like:

- "tune my cold mail"
- "v2 my draft"
- "this draft feels generic"
- "polish the outreach"
- "check my cold mail against the pattern"
- "audit this draft"
- User pastes a cold-mail draft with no specific instruction → assume tuning is wanted

## The V2 pattern in one paragraph

Pain first (named, paragraph 1, with a verifiable source). Region anchor next (named city or region, in paragraph 2 or sometimes subject). Brand word ("Vertrieb neu denken" or the user's equivalent) prominent — subject or paragraph 2. Substance anchor (years in industry, certifications, references) **short, at the end**. CTA low-friction. Subject ≤ 60 characters. That's the whole pattern.

## The checklist (run every draft through it)

```
[ ] 1. Region anchor in subject OR paragraph 1 (not buried in signature)
[ ] 2. Named, company-specific pain in paragraph 1 (with a source date / URL)
[ ] 3. Brand word ("[your brand-word]") prominent — subject or paragraph 1-2
[ ] 4. Substance anchor (years / certs / references) at the END, short, 1 sentence
[ ] 5. Subject ≤ 60 characters
[ ] 6. No buzzwords ("disruptive", "synergetic", "AI-powered" etc.)
[ ] 7. CTA is low-friction (≤20 minutes, named days, easy "no")
[ ] 8. German umlauts written properly (ä, ö, ü, ß) — never "ae", "oe", "ue"
[ ] 9. Length: paragraph 1 + 2 fits on the first preview screen of typical mail clients
[ ] 10. No fake "Re:" or "Fwd:" prefix
```

A failed checkbox = revise. Two or more failed = the draft goes back to scratch, not just edited.

## Anti-patterns this skill rewrites

| Anti-pattern | What it looks like | How V2 fixes it |
|---|---|---|
| **Substance at the top** | "As a sales consultant with 24 years of experience at [OEM], I…" | Move to closing line; pain goes to paragraph 1 |
| **Generic industry pain** | "In the current cost-pressure environment, manufacturers face…" | Replace with one specific signal sourced to the company |
| **Hidden region** | "Best regards from [city]" in signature, never mentioned in body | Move region to paragraph 1 or subject |
| **Buzzword brand** | "AI-powered sales transformation platform" | Replace with brand-word ("Vertrieb neu denken") + plain-language frame |
| **High-friction CTA** | "Let's schedule a strategic alignment session" | "20 minutes next week — Mon 10:00 or Tue 14:00?" |
| **Subject > 60 chars** | "An introduction to [Consultancy]: BAFA-funded sales advisory for the German Mittelstand" | "[Region] → [Company]: [Pain stub] + [brand word]" |

## Output format

```markdown
## Tuning Result

### Checklist
- [x] Region anchor: paragraph 2 → MOVED to subject
- [x] Named pain: paragraph 1 was generic → REPLACED with the LinkedIn-post anchor from [date]
- [x] Brand word: missing → ADDED to paragraph 2
- [x] Substance at end: was at top → MOVED to penultimate paragraph
- [x] Subject ≤ 60 chars: was 78 → trimmed to 54
- [x] Buzzwords: "transformative" → removed
- [x] CTA: vague → specific (two named slots)

### Revised draft

**Subject:** [revised subject]

[Revised body]

### Changes log
1. [What changed and why]
2. ...
```

## What to do when the draft can't be saved

Some drafts fail too many checks to tune; they need re-writing. Symptoms:

- No verifiable pain hook exists for this account → drop the account from the wave (use the `trigger-pipeline` skill to find a different account)
- Substance is the only differentiator the draft has → re-source the pain; substance alone doesn't open Mittelstand doors
- Subject and paragraph 1 both fail → start over from the wave-skill template

When this happens, tell the user clearly: "This draft is below the threshold for tuning — recommend starting fresh from the template." Don't pretend a re-arranged draft will land.

## Companion files

- The V2 pattern itself is documented in `examples/welle-template.md` and `examples/tuning-checklist.md`
- The wave skill (`cold-outreach-welle`) enforces this pattern at write-time; this skill enforces it at review-time

## Why this skill is separate from the wave skill

The wave skill writes drafts. This skill audits drafts. The two failure modes are different: write-time failures show up as missing structure; review-time failures show up as drafts that are structurally fine but read wrong on second pass. Reviewing is a different job — closer to editing than writing — and the prompts have to be different to get good results.

## Sample interactions

**User:** *"Can you v2 this draft for me? [pastes draft]"*

**Skill:** Run the 10-point checklist, produce a revised draft, list changes, flag anything that needed dropping vs editing.

**User:** *"This feels generic but I can't tell why."*

**Skill:** Diagnose against the 6 anti-patterns above, name the specific issue ("substance is at the top — move it to the end"), produce a revised version.

**User:** *"Audit my wave-6 drafts."*

**Skill:** Run the checklist across each draft, return a summary table per draft + per-draft revision suggestions. If 3+ drafts fail the same check, surface that as a wave-level pattern (e.g. "all 6 drafts have substance at the top — this is a template issue, not a per-draft issue").
