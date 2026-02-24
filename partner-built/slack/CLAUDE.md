# Slack Plugin

This plugin integrates Slack with Claude Code, providing tools to search, read, and send messages in Slack.

## Commands

- `/slack:summarize-channel <channel-name>` — Summarize recent activity in a Slack channel
- `/slack:find-discussions <topic>` — Find discussions about a specific topic across Slack channels
- `/slack:draft-announcement <topic>` — Draft a well-formatted Slack announcement and save it as a draft
- `/slack:standup` — Generate a standup update based on your recent Slack activity
- `/slack:channel-digest <channel1, channel2, ...>` — Get a digest of recent activity across multiple Slack channels

## Skills

- **slack-messaging** — Guidance for composing well-formatted Slack messages using mrkdwn syntax
- **slack-search** — Guidance for effectively searching Slack to find messages, files, channels, and people
