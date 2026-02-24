---
description: Structure raw ideas, feedback, and problems into concrete feature concepts with action plans
argument-hint: "<idea or problem statement>"
---

# Feature Ideation

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Transform raw ideas into structured feature concepts. This is the upstream step before `/write-spec` — use it when an idea needs shaping before it is ready for a full PRD.

## Workflow

### 1. Understand the Raw Idea

Ask the user what they are working with. Accept any of:
- A raw idea ("We should add AI search")
- A customer problem ("Users cannot find content quickly")
- A feature request ("Customer X wants bulk export")
- A Slack thread or brainstorm output ("Here is what the team discussed...")
- A competitive observation ("Competitor Y just launched Z")

### 2. Gather Signal

Ask the user about the evidence behind this idea. Be conversational — do not dump all questions at once:

- **Customer signal**: Who is asking for this? How many customers or users? How often does it come up?
- **Problem severity**: How painful is the current state? What workaround do people use today?
- **Strategic alignment**: Does this connect to a company or team goal?
- **Competitive context**: Are competitors doing this? Is it table stakes or a differentiator?
- **Constraints**: Any known technical, timeline, or resource constraints?

### 3. Pull Context from Connected Tools

If **~~chat** is connected:
- Search for related Slack discussions about this idea
- Pull threads where customers or teammates have mentioned the problem
- Identify any prior decisions or discussions about this area

If **~~user feedback** is connected:
- Search for related support tickets or feature requests
- Count how many customers have asked for something similar
- Pull representative quotes from customer feedback

If **~~product analytics** is connected:
- Pull usage data related to the problem area
- Search for behavioral signals (drop-offs, workarounds, low adoption)
- Find data that quantifies the impact of the problem

If these tools are not connected, work from what the user provides. Explicitly note where more data would strengthen the concept.

### 4. Generate the Feature Concept

Produce a structured feature concept document. See the **feature-spec** skill (especially the Idea Structuring section) for guidance on moving from raw idea to PRD-ready concept.

- **Problem Definition**: What user problem does this solve? Who experiences it? How severe is it? (2-3 sentences, grounded in evidence)
- **Customer Signal Summary**: What evidence supports this idea? Number of requests, support tickets, community votes, competitive pressure.
- **Solution Options**: 2-3 approaches to solving the problem:
  - **Option A**: Simplest version that addresses the core problem
  - **Option B**: More comprehensive approach with broader impact
  - **Option C**: Different angle or creative alternative
  - For each: brief description, estimated effort, expected impact, key risk
- **Assumptions to Validate**: What must be true for this to work? List 3-5 assumptions that should be tested before committing.
- **Open Questions**: What do we not know yet? Tag each with who should answer.
- **Recommended Next Step**: Is this ready for a PRD? Should we prototype first? Run customer interviews? Analyze data?
- **2-Week Action Plan**: Specific steps to move this forward, with owners and dates.

### 5. Follow Up

After generating the concept:
- Offer to turn it into a full PRD using `/write-spec`
- Offer to create a prototype of the most promising option using `/prototype`
- Offer to draft customer interview questions to validate assumptions
- Offer to create a one-pager summary for stakeholder alignment

## Output Format

Use markdown with clear headers. Keep the document to 1-2 pages — this is a concept document, not a full spec. The goal is to structure thinking enough to make a go/no-go decision on further investment.

## Tips

- Do not fall in love with the first solution. Generate at least 2-3 options before recommending one.
- The "Assumptions to Validate" section is the most important part. Every idea has hidden assumptions that can make or break it.
- Be direct about signal strength. "2 customers mentioned this once" is different from "47 support tickets in 3 months."
- The recommended next step should match the signal strength. Strong signal → write the PRD. Weak signal → validate first.
- Keep the action plan to 2 weeks. If it takes longer to validate an idea, the idea may be too big or too vague.
