---
description: Prepare for a customer meeting with account context, talking points, risks, and questions to ask
argument-hint: "<account name and meeting type>"
---

# Meeting Prep

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a meeting preparation pack with account context, talking points, and risk assessment.

## Workflow

### 1. Understand the Meeting

Ask the user:
- What account or customer is this meeting with?
- What type of meeting? (QBR, check-in, escalation, executive briefing, sales call)
- When is the meeting?
- Who is attending from the customer side? What are their roles and priorities?
- Any specific topics or concerns to address?

### 2. Pull Context from Connected Tools

If **~~user feedback** is connected:
- Pull open support tickets for this account and their severity
- Search for recent feature requests or feedback from this customer
- Check support ticket volume and resolution time trends

If **~~meeting transcription** is connected:
- Pull notes from previous meetings with this account
- Identify open action items from the last meeting
- Surface recurring themes or concerns raised in past calls

If **~~chat** is connected:
- Search for recent internal conversations about this account
- Pull any customer-facing thread activity
- Identify any escalations or urgent issues discussed

If **~~knowledge base** is connected:
- Search for account plans, success plans, or internal notes
- Pull any relevant case studies or reference materials
- Find related feature specs or roadmap items

If **~~project tracker** is connected:
- Search for tickets tagged with this account or customer
- Pull status on any committed deliverables for this customer

If these tools are not connected, ask the user to paste:
- Account health score, NPS, and contract details
- Recent support tickets for this account
- Previous meeting notes or Gong call summaries
- Any relevant internal context

### 3. Generate the Prep Pack

Produce a structured meeting preparation document. See the **meeting-preparation** skill for detailed guidance on account review methodology, talking point frameworks, and risk identification.

- **Account Snapshot**: Key facts — contract details, health score, tenure, usage summary
- **Meeting Context**: Type, attendees with roles, and agenda
- **Talking Points**: Proactive points (what you want to communicate), reactive points (what they will likely ask), and discovery questions (what you want to learn)
- **Open Items**: Status of their feature requests, support tickets, and previous action items
- **Risks**: Issues that could come up — escalations, delays, competitor mentions, renewal concerns
- **Opportunities**: Expansion potential, case study opportunity, new stakeholder introduction
- **Recommended Approach**: How to structure the conversation and what outcome to aim for

### 4. Follow Up

After generating the prep pack:
- Offer to draft the meeting agenda to send in advance
- Offer to prepare specific talking point scripts for sensitive topics
- Offer to create a post-meeting summary template
- Offer to prep a QBR deck if this is a quarterly review

## Output Format

Use markdown with clear headers. Keep the document actionable — the reader should be able to walk into the meeting confidently after a 5-minute read.

## Tips

- Know who is in the room. Different stakeholders care about different things — a CTO cares about technical roadmap, a VP of Ops cares about support and reliability.
- Review previous meeting action items before the call. Nothing erodes trust faster than forgotten commitments.
- Prepare at least 3 discovery questions. Meetings where you only present and never learn are wasted opportunities.
- If there are known issues or risks, address them proactively rather than waiting for the customer to bring them up.
- Have a clear outcome in mind for every meeting. What do you want to be true after the meeting that is not true before it?
