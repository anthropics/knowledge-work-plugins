---
name: run-monitoring
description: Run a full monitoring cycle right now. Searches Indeed for open roles at tracked companies, scans for company and people news, checks industry topics, and writes a fresh monitoring/digest.md. User waits while this runs — use /setup-monitoring to configure weekly background runs instead.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - WebSearch
  - search_jobs
  - get_job_details
---

Run the Kate monitoring flow as defined in the kate-coach skill's `references/flows.md`.

1. Confirm `monitoring/watchlist.md` exists. If it does not, tell the user: "No watchlist found. Let me set one up before running." Then:
   - Create `monitoring/` folder
   - Copy the watchlist template from the skill's `references/templates/watchlist_template.md`
   - Populate Funnel Companies from `user/application_history.md` automatically
   - Ask the user if they want to add any Watchlist companies or Key People before running
   - Ask the user to confirm or trim the default Industry Topics before first run (offer 3-4 topic suggestions based on `user/user_profile.md` target domains)

2. Read `monitoring/watchlist.md` and `user/user_profile.md` in full before starting searches.

3. Execute the full monitoring flow — Steps 1 through 7 — as defined in `references/flows.md`:
   - Sync funnel companies
   - Search Indeed for open roles (use `search_jobs` tool)
   - Search company news via WebSearch
   - Search key people via WebSearch
   - Search industry topics via WebSearch
   - Archive previous digest and write new `monitoring/digest.md`
   - Generate similar company suggestions if this is the first run or every 5th run

4. After writing the digest, summarize findings for the user: total new roles found, any notable company news, any people activity worth flagging. Keep it to 4-5 sentences — the full detail is in the digest.

5. Ask: "Anything too broad or too narrow in what I tracked? I can add, remove, or pause topics and companies before the next run."

6. Log any relevance feedback to the tuning notes section of `watchlist.md`.

7. Update `user/session_context.md` to note that monitoring ran and the timestamp.
