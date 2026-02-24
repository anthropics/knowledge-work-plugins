---
description: Draft a well-formatted Slack announcement and save it as a draft
---

Given the topic or context provided in $ARGUMENTS:

1. Ask the user the following clarifying questions (skip any that are already clear from the provided context):
   - Which channel should this announcement be posted in?
   - Who is the target audience?
   - What is the key message or call to action?
   - Is there a deadline or date to highlight?
   - What tone is appropriate — formal, casual, or urgent?

2. Compose the announcement following Slack formatting best practices:
   - Use Slack's mrkdwn syntax: `*bold*` for emphasis (not `**bold**`), `_italic_` for secondary emphasis, `>` for callouts.
   - Lead with the most important information — don't bury the point.
   - Use a clear, descriptive opening line that works as a headline.
   - Keep paragraphs short (2-3 sentences max).
   - Use bullet points for lists of items or action steps.
   - Include relevant emoji sparingly to aid scanning (e.g., :mega: for announcements, :calendar: for dates, :point_right: for action items).
   - End with a clear call to action or next step if applicable.

3. Present the draft to the user for review. Offer to adjust tone, length, or formatting.

4. Once the user approves, use `slack_search_channels` to find the target channel ID, then use `slack_send_message_draft` to create the draft in Slack.

5. Let the user know the draft is ready in Slack and they can review and send it from the Slack client.
