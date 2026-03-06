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

1. Detect the current project folder path. Store it — you will embed it in the scheduled task prompt so the headless task knows where to find the project files.

2. Check whether `monitoring/watchlist.md` already exists.

   **If it does not exist:**
   - Create the `monitoring/` folder
   - Copy the watchlist template from `skills/kate-coach/references/templates/watchlist_template.md`
   - Auto-populate Funnel Companies from `user/application_history.md`
   - Ask the user: "Before I set up monitoring, let me confirm what to track. Any companies you want on the watchlist beyond the ones you're already pursuing?" Wait for answer.
   - Ask: "Any specific people I should track — executives at target companies, recruiters, people you'll be interviewing with?" Wait for answer.
   - Suggest 3-4 industry topics based on `user/user_profile.md` target domains. Ask the user to confirm, trim, or modify before saving.
   - Write the completed `watchlist.md`.

   **If it already exists:** confirm with the user whether to keep the current watchlist or update it before creating the scheduled task.

3. Run `/run-monitoring` inline to generate the first digest before scheduling. This ensures the user can see and validate the output before committing to a weekly run.

4. After the first run, ask: "Does that look right? Too much, too little, anything to change before I set this up to run weekly?"

5. Apply any feedback to `watchlist.md`.

6. Create the scheduled weekly monitoring task using the following prompt, substituting the actual project folder path detected in Step 1:

---
SCHEDULED TASK PROMPT (substitute [PROJECT_FOLDER_PATH] with the actual path):

You are running Kate's weekly monitoring task. This is a headless background job — no user is present.

Project folder: [PROJECT_FOLDER_PATH]

Run the full monitoring flow as defined in the kate-coach skill's references/flows.md. Steps:

1. Read [PROJECT_FOLDER_PATH]/monitoring/watchlist.md and [PROJECT_FOLDER_PATH]/user/user_profile.md.
2. Sync funnel companies from [PROJECT_FOLDER_PATH]/user/application_history.md.
3. Search Indeed (search_jobs tool) for open roles at all companies in Funnel Companies and Watchlist sections, using role titles and domains from user_profile.md.
4. Web search for company news (past 14 days) for all companies in Funnel and Watchlist sections.
5. Web search for Key People activity (past 30 days).
6. Web search for Industry Topics with Status: Active.
7. Archive the previous digest to [PROJECT_FOLDER_PATH]/monitoring/digest_archive/[today's date].md.
8. Write a new [PROJECT_FOLDER_PATH]/monitoring/digest.md using the digest format defined in flows.md.
9. Every 5 runs, generate 4-6 similar company suggestions and append them to a file at [PROJECT_FOLDER_PATH]/monitoring/pending_suggestions.md for Kate to surface in the next session.

Do not interact with the user. Write files and exit.
---

7. Set the scheduled task to run weekly (cron: `0 7 * * 1` — Monday mornings at 7am local time, adjustable).

8. Record the scheduled task ID in the `monitoring/watchlist.md` Scheduled Task Settings section.

9. Confirm to the user: "Monitoring is live. It'll run every Monday morning and have a fresh digest ready when you start your next session after that. You'll see a note at session start if the digest is more than 7 days old."
