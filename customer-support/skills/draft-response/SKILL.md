---
name: draft-response
description: Draft a professional customer-facing response tailored to the situation and relationship. Use when answering a product question, responding to an escalation or outage, delivering bad news like a delay or won't-fix, declining a feature request, or replying to a billing issue.
argument-hint: "<situation description>"
---

# /draft-response

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Draft a professional, customer-facing response tailored to the situation, customer relationship, and communication context.

## Usage

```
/draft-response <context about the customer question, issue, or request>
```

Examples:
- `/draft-response Acme Corp is asking when the new dashboard feature will ship`
- `/draft-response Customer escalation — their integration has been down for 2 days`
- `/draft-response Responding to a feature request we won't be building`
- `/draft-response Customer hit a billing error and wants a resolution ASAP`

## Workflow

### 1. Understand the Context

Parse the user's input to determine:

- **Customer**: Who is the communication for? Look up account context if available.
- **Situation type**: Question, issue, escalation, announcement, negotiation, bad news, good news, follow-up
- **Urgency**: Is this time-sensitive? How long has the customer been waiting?
- **Channel**: Email, support ticket, chat, or other (adjust formality accordingly)
- **Relationship stage**: New customer, established, frustrated/escalated
- **Stakeholder level**: End user, manager, executive, technical, business

### 2. Research Context

Gather relevant background from available sources:

**~~email:**
- Previous correspondence with this customer on this topic
- Any commitments or timelines previously shared
- Tone and style of the existing thread

**~~chat:**
- Internal discussions about this customer or topic
- Any guidance from product, engineering, or leadership
- Similar situations and how they were handled

**~~CRM (if connected):**
- Account details and plan level
- Contact information and key stakeholders
- Previous escalations or sensitive issues

**~~support platform (if connected):**
- Related tickets and their resolution
- Known issues or workarounds
- SLA status and response time commitments

**~~knowledge base:**
- Official documentation or help articles to reference
- Product roadmap information (if shareable)
- Policy or process documentation

### 3. Generate the Draft

Produce a response tailored to the situation:

```
## Draft Response

**To:** [Customer contact name]
**Re:** [Subject/topic]
**Channel:** [Email / Ticket / Chat]
**Tone:** [Empathetic / Professional / Technical / Celebratory / Candid]

---

[Draft response text]

---

### Notes for You (internal — do not send)
- **Why this approach:** [Rationale for tone and content choices]
- **Things to verify:** [Any facts or commitments to confirm before sending]
- **Risk factors:** [Anything sensitive about this response]
- **Follow-up needed:** [Actions to take after sending]
- **Escalation note:** [If this should be reviewed by someone else first]
```

### 4. Run Quality Checks

Before presenting the draft, verify:

- [ ] Tone matches the situation and relationship
- [ ] No commitments beyond what's authorized
- [ ] No product roadmap details that shouldn't be shared externally
- [ ] Accurate references to previous conversations
- [ ] Clear next steps and ownership
- [ ] Appropriate for the stakeholder level (not too technical for executives, not too vague for engineers)
- [ ] Length is appropriate for the channel (shorter for chat, fuller for email)

### 5. Offer Iterations

After presenting the draft:
- "Want me to adjust the tone? (more formal, more casual, more empathetic, more direct)"
- "Should I add or remove any specific points?"
- "Want me to make this shorter/longer?"
- "Should I draft a version for a different stakeholder?"
- "Want me to draft the internal escalation note as well?"
- "Should I prepare a follow-up message to send after [X days] if no response?"

---

## Customer Communication Best Practices

### Core Principles

1. **Lead with empathy**: Acknowledge the customer's situation before jumping to solutions
2. **Be direct**: Get to the point — customers are busy. Bottom-line-up-front.
3. **Be honest**: Never overpromise, never mislead, never hide bad news in jargon
4. **Be specific**: Use concrete details, timelines, and names — avoid vague language
5. **Own it**: Take responsibility when appropriate. "We" not "the system" or "the process"
6. **Close the loop**: Every response should have a clear next step or call to action
7. **Match their energy**: If they're frustrated, be empathetic first. If they're excited, be enthusiastic.

### Response Structure

For most customer communications, follow this structure:

```
1. Acknowledgment / Context (1-2 sentences)
   - Acknowledge what they said, asked, or are experiencing
   - Show you understand their situation

2. Core Message (1-3 paragraphs)
   - Deliver the main information, answer, or update
   - Be specific and concrete
   - Include relevant details they need

3. Next Steps (1-3 bullets)
   - What YOU will do and by when
   - What THEY need to do (if anything)
   - When they'll hear from you next

4. Closing (1 sentence)
   - Warm but professional sign-off
   - Reinforce you're available if needed
```

### Length Guidelines

- **Chat/IM**: 1-4 sentences. Get to the point immediately.
- **Support ticket response**: 1-3 short paragraphs. Structured and scannable.
- **Email**: 3-5 paragraphs max. Respect their inbox.
- **Escalation response**: As long as needed to be thorough, but well-structured with headers.
- **Executive communication**: Shorter is better. 2-3 paragraphs max. Data-driven.

## Tone and Style Guidelines

### Tone Spectrum

| Situation | Tone | Characteristics |
|-----------|------|----------------|
| Good news / wins | Celebratory | Enthusiastic, warm, congratulatory, forward-looking |
| Routine update | Professional | Clear, concise, informative, friendly |
| Technical response | Precise | Accurate, detailed, structured, patient |
| Delayed delivery | Accountable | Honest, apologetic, action-oriented, specific |
| Bad news | Candid | Direct, empathetic, solution-oriented, respectful |
| Issue / outage | Urgent | Immediate, transparent, actionable, reassuring |
| Escalation | Executive | Composed, ownership-taking, plan-presenting, confident |
| Billing / account | Precise | Clear, factual, empathetic, resolution-focused |

### Tone Adjustments by Relationship Stage

**New Customer (0-3 months):**
- More formal and professional
- Extra context and explanation (don't assume knowledge)
- Proactively offer help and resources
- Build trust through reliability and responsiveness

**Established Customer (3+ months):**
- Warm and collaborative
- Can reference shared history and previous conversations
- More direct and efficient communication
- Show awareness of their goals and priorities

**Frustrated or Escalated Customer:**
- Extra empathy and acknowledgment
- Urgency in response times
- Concrete action plans with specific commitments
- Shorter feedback loops

### Writing Style Rules

**DO:**
- Use active voice ("We'll investigate" not "This will be investigated")
- Use "I" for personal commitments and "we" for team commitments
- Name specific people when assigning actions ("Sarah from our engineering team will...")
- Use the customer's terminology, not your internal jargon
- Include specific dates and times, not relative terms ("by Friday January 24" not "in a few days")
- Break up long responses with headers or bullet points

**DON'T:**
- Use corporate jargon or buzzwords ("synergy", "leverage", "paradigm shift")
- Deflect blame to other teams, systems, or processes
- Use passive voice to avoid ownership ("Mistakes were made")
- Include unnecessary caveats or hedging that undermines confidence
- CC people unnecessarily — only include those who need to be in the conversation
- Use exclamation marks excessively (one per email max, if any)

## Situation-Specific Approaches

**Answering a product question:**
- Lead with the direct answer
- Provide relevant documentation links
- Offer to connect them with the right resource if needed
- If you don't know the answer: say so honestly, commit to finding out, give a timeline

**Responding to an issue or bug:**
- Acknowledge the impact on their work
- State what you know about the issue and its status
- Provide workaround if available
- Set expectations for resolution timeline
- Commit to updates at regular intervals

**Handling an escalation:**
- Acknowledge the severity and their frustration
- Take ownership (no deflecting or excuse-making)
- Provide a clear action plan with timeline
- Identify the person accountable for resolution
- Offer a meeting or call if appropriate for the severity

**Delivering bad news (feature sunset, delay, can't-fix):**
- Be direct — don't bury the news
- Explain the reasoning honestly
- Acknowledge the impact on them specifically
- Offer alternatives or mitigation
- Provide a clear path forward

**Sharing good news (feature launch, milestone, recognition):**
- Lead with the positive outcome
- Connect it to their specific goals or use case
- Suggest next steps to capitalize on the good news
- Express genuine enthusiasm

**Declining a request (feature request, discount, exception):**
- Acknowledge the request and its reasoning
- Be honest about the decision
- Explain the why without being dismissive
- Offer alternatives when possible
- Leave the door open for future conversation

## Response Templates for Common Scenarios

### Acknowledging a Bug Report

```
Hi [Name],

Thank you for reporting this — I can see how [specific impact] would be
frustrating for your team.

I've confirmed the issue and escalated it to our engineering team as a
[priority level]. Here's what we know so far:
- [What's happening]
- [What's causing it, if known]
- [Workaround, if available]

I'll update you by [specific date/time] with a resolution timeline.
In the meantime, [workaround details if applicable].

Let me know if you have any questions or if this is impacting you in
other ways I should know about.

Best,
[Your name]
```

### Acknowledging a Billing or Account Issue

```
Hi [Name],

Thank you for reaching out about this — I understand billing issues
need prompt attention, and I want to make sure this gets resolved
quickly.

I've looked into your account and here's what I'm seeing:
- [What happened — clear factual explanation]
- [Impact on their account — charges, access, etc.]

Here's what I'm doing to fix this:
- [Action 1 — with timeline]
- [Action 2 — if applicable]

[If resolution is immediate: "This has been corrected and you should
see the change reflected within [timeframe]."]
[If needs investigation: "I'm escalating this to our billing team
and will have an update for you by [specific date]."]

I'm sorry for the inconvenience. Let me know if you have any
questions about your account.

Best,
[Your name]
```

### Responding to a Feature Request You Won't Build

```
Hi [Name],

Thank you for sharing this request — I can see why [capability] would
be valuable for [their use case].

I discussed this with our product team, and this isn't something we're
planning to build in the near term. The primary reason is [honest,
respectful explanation — e.g., it serves a narrow use case, it conflicts
with our architecture direction, etc.].

That said, I want to make sure you can accomplish your goal. Here are
some alternatives:
- [Alternative approach 1]
- [Alternative approach 2]
- [Integration or workaround if applicable]

I've also documented your request in our feedback system, and if our
direction changes, I'll let you know.

Would any of these alternatives work for your team? Happy to dig
deeper into any of them.

Best,
[Your name]
```

### Outage or Incident Communication

```
Hi [Name],

I wanted to reach out directly to let you know about an issue affecting
[service/feature] that I know your team relies on.

**What happened:** [Clear, non-technical explanation]
**Impact:** [How it affects them specifically]
**Status:** [Current status — investigating / identified / fixing / resolved]
**ETA for resolution:** [Specific time if known, or "we'll update every X hours"]

[If applicable: "In the meantime, you can [workaround]."]

I'm personally tracking this and will update you as soon as we have a
resolution. You can also check [status page URL] for real-time updates.

I'm sorry for the disruption to your team's work. We take this seriously
and [what you're doing to prevent recurrence if known].

[Your name]
```

### Following Up After Silence

```
Hi [Name],

I wanted to check in — I sent over [what you sent] on [date] and
wanted to make sure it didn't get lost in the shuffle.

[Brief reminder of what you need from them or what you're offering]

If now isn't a good time, no worries — just let me know when would be
better, and I'm happy to reconnect then.

Best,
[Your name]
```

## Follow-up and Escalation Guidance

### Follow-up Cadence

| Situation | Follow-up Timing |
|-----------|-----------------|
| Unanswered question | 2-3 business days |
| Open support issue | Daily until resolved for critical, 2-3 days for standard |
| Post-meeting action items | Within 24 hours (send notes), then check at deadline |
| General check-in | As needed for ongoing issues |
| After delivering bad news | 1 week to check on impact and sentiment |

### When to Escalate

**Escalate to your manager when:**
- Customer threatens to cancel or significantly downsell
- Customer requests exception to policy you can't authorize
- An issue has been unresolved for longer than SLA allows
- Customer requests direct contact with leadership
- You've made an error that needs senior involvement to resolve

**Escalate to product/engineering when:**
- Bug is critical and blocking the customer's business
- Feature gap is causing a competitive loss
- Customer has unique technical requirements beyond standard support
- Integration issues require engineering investigation

**Escalation format:**
```
ESCALATION: [Customer Name] — [One-line summary]

Urgency: [Critical / High / Medium]
Customer impact: [What's broken for them]
History: [Brief background — 2-3 sentences]
What I've tried: [Actions taken so far]
What I need: [Specific help or decision needed]
Deadline: [When this needs to be resolved by]
```
