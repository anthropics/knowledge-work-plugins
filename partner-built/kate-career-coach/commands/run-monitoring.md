---
name: run-monitoring
description: Run a full monitoring cycle right now. Searches Indeed for open roles at tracked companies, scans for company and people news, checks industry topics, and writes a fresh monitoring/digest.md. User waits while this runs — use setup-monitoring to configure weekly background runs instead.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - WebSearch
  - search_jobs
  - get_job_details
---

Run the **Monitoring Flow** (Steps 1–7) in `skills/kate-coach/references/flows.md`.

Before starting:
- If `monitoring/watchlist.md` does not exist, tell the user and set it up first: create the folder, copy from `skills/kate-coach/references/templates/watchlist_template.md`, auto-populate Funnel Companies from `user/application_history.md`, and ask for any additional Watchlist companies, Key People, and Industry Topics before running.
- If it exists, read it in full alongside `user/user_profile.md` before starting searches.

After writing the digest, summarize findings in 4-5 sentences and ask: "Anything too broad or too narrow in what I tracked?"
