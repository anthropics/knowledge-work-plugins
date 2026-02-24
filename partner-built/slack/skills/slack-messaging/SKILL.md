---
name: slack-messaging
description: Guidance for composing well-formatted, effective Slack messages using mrkdwn syntax
---

# Slack Messaging Best Practices

This skill provides guidance for composing well-formatted, effective Slack messages.

## When to Use

Apply this skill whenever composing, drafting, or helping the user write a Slack message — including when using `slack_send_message`, `slack_send_message_draft`, or `slack_create_canvas`.

## Slack Formatting (mrkdwn)

Slack uses its own markup syntax called **mrkdwn**, which differs from standard Markdown. Always use mrkdwn when composing Slack messages:

| Format | Syntax | Notes |
|--------|--------|-------|
| Bold | `*text*` | Single asterisks, NOT double |
| Italic | `_text_` | Underscores |
| Strikethrough | `~text~` | Tildes |
| Code (inline) | `` `code` `` | Backticks |
| Code block | `` ```code``` `` | Triple backticks |
| Quote | `> text` | Angle bracket |
| Link | `<url\|display text>` | Pipe-separated in angle brackets |
| User mention | `<@U123456>` | User ID in angle brackets |
| Channel mention | `<#C123456>` | Channel ID in angle brackets |
| Bulleted list | `- item` or `• item` | Dash or bullet character |
| Numbered list | `1. item` | Number followed by period |

### Common Mistakes to Avoid

- Do NOT use `**bold**` (double asterisks) — Slack uses `*bold*` (single asterisks)
- Do NOT use `## headers` — Slack does not support Markdown headers. Use `*bold text*` on its own line instead.
- Do NOT use `[text](url)` for links — Slack uses `<url|text>` format
- Do NOT use `---` for horizontal rules — Slack does not render these

## Message Structure Guidelines

- **Lead with the point.** Put the most important information in the first line. Many people read Slack on mobile or in notifications where only the first line shows.
- **Keep it short.** Aim for 1-3 short paragraphs. If the message is long, consider using a Canvas instead.
- **Use line breaks generously.** Walls of text are hard to read. Separate distinct thoughts with blank lines.
- **Use bullet points for lists.** Anything with 3+ items should be a list, not a run-on sentence.
- **Bold key information.** Use `*bold*` for names, dates, deadlines, and action items so they stand out when scanning.

## Thread vs. Channel Etiquette

- **Reply in threads** when responding to a specific message to keep the main channel clean.
- **Use `reply_broadcast`** (also post to channel) only when the reply contains information everyone needs to see.
- **Post in the channel** (not a thread) when starting a new topic, making an announcement, or asking a question to the whole group.
- **Don't start a new thread** to continue an existing conversation — find and reply to the original message.

## Tone and Audience

- Match the tone to the channel — `#general` is usually more formal than `#random`.
- Use emoji reactions instead of reply messages for simple acknowledgments (though note: the MCP tools can't add reactions, so suggest the user do this manually if appropriate).
- When writing announcements, use a clear structure: context, key info, call to action.
