---
description: Draft personalized candidate outreach messages
argument-hint: "<candidate info and role>"
---

# Draft Outreach

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Craft personalized outreach messages that stand out in a candidate's inbox. Generates multi-touch sequences with tailored hooks based on the candidate's background and motivations.

## Input

The user provides one or more of:
- Candidate name, current role, and company
- LinkedIn profile or resume
- Role being recruited for
- Why this candidate is a fit (specific reasons)
- Outreach channel (email, LinkedIn InMail, other)
- Any prior relationship or warm connection

If minimal input, ask: "Who are you reaching out to and for what role? Share the candidate's background and the position."

## Workflow

1. **Research the candidate** — Parse provided info and use web search to understand their background, interests, recent activity, and likely motivations
2. **Identify hooks** — Find 2-3 personalized angles: recent project, company news, shared connection, career trajectory, technical interests
3. **Match to role** — Connect the candidate's likely motivations to what the role offers
4. **Draft the sequence** — Write a 3-touch outreach sequence (initial + 2 follow-ups) with different angles
5. **Optimize for channel** — Adjust length and tone for the outreach channel (LinkedIn InMail is shorter, email allows more detail)
6. **Add subject lines** — Write 2-3 subject line options for email outreach
7. **If data enrichment connected** — Pull verified contact info, mutual connections, and recent activity

## Output Structure

```
## Outreach: [Candidate Name] → [Role Title]

### Candidate Research
- **Current**: [Role at Company]
- **Background**: [Key career highlights]
- **Likely motivations**: [What would make them move]
- **Personalization hooks**: [Specific details to reference]

### Message 1: Initial Outreach
**Channel**: [Email/LinkedIn] | **Tone**: [warm/direct/curious]
**Subject line options**:
1. [Option A]
2. [Option B]

---
[Message body — personalized, concise, specific about why them + why this role]
---

### Message 2: Follow-up (3-5 days later)
**Angle**: [Different hook than message 1]

---
[Follow-up message — adds new information, doesn't just "bump"]
---

### Message 3: Final Touch (5-7 days later)
**Angle**: [Lightest touch, easy call-to-action]

---
[Brief final message — respectful, offers a clear next step or graceful close]
---

### Outreach Tips
- **Best time to send**: [day/time recommendation]
- **If they respond positively**: [suggested next steps]
- **If no response after sequence**: [recommended waiting period and re-engagement strategy]
```

## With Connectors

- **If email connected**: Send the messages directly, schedule follow-ups
- **If data enrichment connected**: Pull verified email, phone, mutual connections, and recent social activity
- **If ATS connected**: Log the outreach, check for prior contact history, and avoid double-outreach
- **If chat connected**: Notify the hiring manager when a candidate responds

## Tips

- The more you know about the candidate, the better the personalization — LinkedIn profiles produce much better outreach than just a name
- Mention the specific reason you think they're a fit — generic "your background is impressive" messages get ignored
- For passive candidates, lead with what's in it for them, not what you need
