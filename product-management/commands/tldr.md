---
description: Create a quick 3-5 bullet summary optimized for Slack, email, or async communication
argument-hint: "<content to summarize>"
---

# TL;DR

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Create a 30-second summary optimized for Slack, email, and mobile reading.

## Workflow

### 1. Understand What to Summarize

Ask the user:
- What content should be summarized? (Paste a document, describe a topic, or reference a previous conversation)
- Who is the audience? (Team, leadership, stakeholders, customers)
- What should the reader do after reading this? (Review, approve, discuss, FYI only)

Accept any of:
- A full document (sprint review, PRD, meeting notes, report)
- A long Slack thread or email chain
- A verbal description of what happened
- Output from another command (sprint review, one-pager, competitive brief)

### 2. Generate the TL;DR

Produce a 3-5 bullet summary. See the **executive-synthesis** skill for detailed guidance on TL;DR writing rules and Slack formatting.

Strict constraints:
- **3-5 bullets** (never more — if you need more, suggest a one-pager instead)
- **Under 100 words total**
- **Each bullet is one clear point** (not a paragraph)
- **Includes a call-to-action** on a separate line at the end

Writing rules:
- Start each bullet with the key fact, not context
- Use numbers over adjectives ("40% faster" not "significantly faster")
- Active voice ("We shipped" not "Was shipped")
- Cut qualifiers ("basically", "essentially", "somewhat")
- One idea per bullet — if it has "and", consider splitting it
- Bold the most important words for quick scanning
- Use emoji sparingly as visual markers (one per bullet maximum)

### 3. Follow Up

After generating the TL;DR:
- Offer to create a longer one-pager using `/one-pager` if the topic needs more depth
- Offer to adjust the tone for a different audience
- Offer to create a Slack-formatted version ready to copy-paste
- Offer to add more context to any specific bullet

## Output Format

Plain text optimized for pasting into Slack or email. Use emoji sparingly for visual scanning. Bold key words. End with a clear call-to-action on its own line.

## Tips

- If you cannot fit the summary in 5 bullets, the source material covers too many topics. Ask which topic to focus on, or suggest a one-pager instead.
- The call-to-action is not optional. Every summary should tell the reader what to do next, even if it is just "FYI, no action needed."
- Test on mobile. If the TL;DR requires scrolling on a phone screen, it is too long.
- Lead with what changed or what matters, not with context. "Search NPS: 3.2 → 4.1" is better than "After the Q3 search initiative, our NPS score improved from 3.2 to 4.1."
- Match the audience's language. Engineering teams want technical specifics. Executives want business impact. Customers want user value.
