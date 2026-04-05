---
name: setup-monitoring
description: Set up weekly background monitoring. Initializes the watchlist, runs a first monitoring cycle, then creates a scheduled task that runs the monitoring headlessly every week and writes results to monitoring/digest.md.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - WebSearch
  - search_jobs
---

Set up Kate's monitoring system for the first time, or reconfigure it.

1. Detect the current project folder path. You will need it in Step 6.

2. Check whether `monitoring/watchlist.md` already exists.

   **If it does not exist:**
   - Create the `monitoring/` folder
   - Copy the watchlist template from `skills/kate-coach/references/templates/watchlist_template.md`
   - Auto-populate Funnel Companies from `user/application_history.md`
   - Ask: "Before I set up monitoring, let me confirm what to track. Any companies you want on the watchlist beyond the ones you're already pursuing?" Wait for answer.
   - Ask: "Any specific people I should track — executives at target companies, recruiters, people you'll be interviewing with?" Wait for answer.
   - Suggest 3-4 industry topics based on `user/user_profile.md` target domains. Ask the user to confirm, trim, or modify before saving.
   - Write the completed `watchlist.md`.

   **If it already exists:** confirm with the user whether to keep the current watchlist or update it before proceeding.

3. Run `/run-monitoring` inline to generate the first digest before scheduling. This lets the user validate the output before committing to a weekly run.

4. After the first run, ask: "Does that look right? Too much, too little, anything to change before I set this up to run weekly?"

5. Apply any feedback to `watchlist.md`.

6. Generate the scheduled task prompt file. Read `skills/kate-coach/references/flows.md` — specifically the Monitoring Flow section — and write `monitoring/scheduled_task_prompt.md` using this structure, substituting the actual project folder path detected in Step 1:

```
# Kate Weekly Monitoring — Scheduled Task Prompt
# Generated: [YYYY-MM-DD]
# Re-run /setup-monitoring to regenerate this file after updating flows.md.

You are running Kate's weekly monitoring task. This is a headless background job — no user is present.

Project folder: [PROJECT_FOLDER_PATH]

Follow the Monitoring Flow as defined in the kate-coach skill's references/flows.md exactly. The flow file is at: [PROJECT_FOLDER_PATH]/skills/kate-coach/references/flows.md

Steps are defined there in full. Do not deviate from them. Do not interact with the user. Write files and exit.

Key paths:
- Watchlist: [PROJECT_FOLDER_PATH]/monitoring/watchlist.md
- User profile: [PROJECT_FOLDER_PATH]/user/user_profile.md
- Application history: [PROJECT_FOLDER_PATH]/user/application_history.md
- Digest output: [PROJECT_FOLDER_PATH]/monitoring/digest.md
- Digest archive: [PROJECT_FOLDER_PATH]/monitoring/digest_archive/
- Pending suggestions: [PROJECT_FOLDER_PATH]/monitoring/pending_suggestions.md
```

This file is the single source of truth for the scheduled task. If the monitoring flow in `flows.md` changes, re-run `/setup-monitoring` to regenerate it.

7. Create the scheduled weekly task pointed at `monitoring/scheduled_task_prompt.md`. Set it to run weekly (cron: `0 7 * * 1` — Monday mornings at 7am local time, adjustable).

8. Record the scheduled task ID in the `monitoring/watchlist.md` Scheduled Task Settings section.

9. Confirm to the user: "Monitoring is live. It'll run every Monday morning and have a fresh digest ready when you start your next session after that. You'll see a note at session start if the digest is more than 7 days old."
