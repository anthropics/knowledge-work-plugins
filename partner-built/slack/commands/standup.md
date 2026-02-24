---
description: Generate a standup update based on your recent Slack activity
---

1. Use `slack_read_user_profile` (with no user_id) to get the current user's profile information, including their user ID and display name.

2. Search for the user's recent messages using `slack_search_public` with the filter `from:<@USER_ID>` and `after:` set to yesterday's date. This captures messages from the last working day.

3. Review the messages found and categorize them into standup themes:
   - **What I worked on** — Topics, projects, or tasks the user discussed or contributed to
   - **What I'm working on next** — Any mentions of upcoming work, plans, or follow-ups
   - **Blockers** — Any questions asked that went unanswered, issues raised, or explicit mentions of being stuck

4. For messages in threads, use `slack_read_thread` to get the full context so you can accurately describe what the user contributed.

5. Format the standup as:
   ```
   *Standup for <display name> — <today's date>*

   *Done:*
   - Item 1
   - Item 2

   *Doing:*
   - Item 1

   *Blockers:*
   - None / Item 1
   ```

6. Present the standup to the user for review. They can edit, adjust, or ask you to post it to a specific channel.
