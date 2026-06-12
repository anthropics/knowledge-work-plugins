# JLC Vertrieb Mittelstand — Cold-Outreach + Trigger-Based Selling for German B2B

A Claude plugin built for solo consultants and small sales teams running B2B outreach into the German **Mittelstand** (manufacturing SMEs, 30-250 employees, DACH region). Encodes the patterns that a BAFA-funded sales consultant in DACH refined across ~4 months of weekly outreach waves into roughly 60 manufacturing accounts.

It is not a generic sales plugin. It is opinionated about:

- **Wave-based cold outreach** — small, named, weekly batches (5-10 accounts) instead of bulk sequences
- **Trigger-driven lead identification** — fresh hooks (new VP Sales, hiring signals, funded news) over evergreen lists
- **Sniper accounts** — 2-3 named ICP fits per cycle with a per-account hand-built first touch, not a template merge
- **A tuning pattern** for cold mail that survived contact with real prospects — region-anchored, pain-first, brand-word prominent

## Why this plugin

Most sales tooling assumes a US-style funnel: high-volume sequencing, generic personalization tokens, CRM-first. That does not fit the DACH Mittelstand. German manufacturing buyers respond to: regional proximity, named pain with a verifiable source, a clear competence anchor, and an unhurried CTA.

This plugin captures the cadence, gates, and tuning rules built by a solo consultant with a B2B sales background (large industrial OEMs, 20+ years) and four months of live outreach iteration. It is offered as a contribution to the `anthropics/knowledge-work-plugins` catalogue so other solo consultants and small sales teams in DACH can start from a tested baseline rather than a blank template.

## What's inside

Four skills, each loaded automatically when relevant:

| Skill | Triggers when you say… |
|---|---|
| `cold-outreach-welle` | "build wave 7", "next outreach batch", "10 prospects this week" |
| `trigger-pipeline` | "find leads from this week's news", "VP-sales hiring signals", "trigger-based prospecting" |
| `sniper-leads` | "3 named accounts to chase", "top ICP fits in my region", "build a sniper list" |
| `outreach-tuning` | "tune my cold mail", "v2 my draft", "this mail feels generic" |

Plus:

- `examples/` — wave template, trigger types, pre-send checklist
- `docs/` — installation and end-to-end workflow

## Installation

### Cowork

Install from [claude.com/plugins](https://claude.com/plugins/) once this plugin is added to a marketplace — or sideload by pointing Cowork at this repository directory.

### Claude Code

```bash
# Add a marketplace that includes this plugin, then:
claude plugin install jlc-vertrieb-mittelstand
```

Once installed, skills fire automatically when their triggers appear in conversation. No slash commands — the plugin is skills-only.

## Making it yours

Three things you will want to override:

1. **Your region anchor.** The skills reference "your region" rather than a specific city. Drop your actual region/city into a `settings.local.json` and the skills will consume it.
2. **Your competence anchor.** The substance line at the close of every cold mail (years in industry, certifications, references) is yours, not ours.
3. **Your ICP.** The hard gates here are calibrated for manufacturing SMEs 30-250 FTE in DACH. If you sell into a different segment, edit the gates in `skills/sniper-leads/SKILL.md` and `skills/cold-outreach-welle/SKILL.md`.

A starter `settings.local.json` example is included in `docs/installation.md`.

## What this plugin is NOT

- **Not a sequencer.** It does not send mail. It produces drafts you review and send manually. (Cold outreach into the Mittelstand rewards low volume + high care.)
- **Not a CRM.** It assumes you already track leads somewhere — Notion, a spreadsheet, anywhere.
- **Not enrichment.** It works fine alongside enrichment tools but does not depend on them.
- **Not US-style high-volume.** The cadence caps at ~30 cold touches per week per consultant. The patterns break above that.

## Author

[Lepper Consulting](https://lepperconsulting.de), Ravensburg/DACH. BAFA-certified sales consultant for the German Mittelstand. Background: 20+ years B2B sales at large industrial OEMs.

This plugin is an open-source contribution to the Anthropic knowledge-work-plugins catalogue — same shape as the official `sales` plugin, but opinionated for the DACH Mittelstand segment that the generic plugin does not cover.

## License

MIT — see [LICENSE](LICENSE).
