---
name: run-monitoring
description: >
  Run a full monitoring cycle right now. Searches for open roles at tracked companies, scans
  for company and people news, checks industry topics, and writes a fresh monitoring/digest.md.
  User waits while this runs. Use setup-monitoring to configure weekly background runs instead.
  Trigger phrases: "run monitoring", "check for new roles", "monitor now", "fresh monitoring run",
  "update the digest", "what's new at my target companies", "check my watchlist".
---

If kate-coach SKILL.md is not already loaded in this session, read `skills/kate-coach/SKILL.md` now — it contains Kate's identity, session context, and file ownership rules.

Run the **Monitoring Flow** (Steps 1–7) in `skills/kate-coach/references/flows.md`.

## Watchlist Structure

`monitoring/watchlist.md` contains five sections:
- **Funnel Companies** — auto-populated from `user/application_history.md`; always tracked
- **Watchlist** — user-defined companies to follow without an active application
- **Similar Companies** — Kate-suggested, user-approved, with reasoning logged
- **Key People** — individuals from transcripts, upcoming calls, or explicitly named
- **Industry Topics** — web search terms for domain news; each has Active/Paused status

Before starting:
- If `monitoring/watchlist.md` does not exist: create the `monitoring/` folder, copy from `skills/kate-coach/references/templates/watchlist_template.md`, auto-populate Funnel Companies from `user/application_history.md`, and ask for Watchlist companies, Key People, and Industry Topics before running
- If it exists: read it in full alongside `user/user_profile.md` before starting searches

After writing the digest, summarize findings in 4-5 sentences and ask: "Anything too broad or too narrow in what I tracked?"
