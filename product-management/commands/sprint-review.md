---
description: Generate a sprint review summary with accomplishments, metrics, demos, and next sprint preview
argument-hint: "<sprint name or number>"
---

# Sprint Review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a stakeholder-ready sprint review summary.

## Workflow

### 1. Understand the Sprint

Ask the user:
- Which sprint? (name or number)
- Sprint dates (start and end)
- What was the sprint goal?
- Which team is this for?

### 2. Pull Context from Connected Tools

If **~~project tracker** is connected:
- Pull all stories completed this sprint with point values
- Identify carried-over items and their reasons
- Calculate velocity: planned vs completed points
- Pull bug counts: opened, closed, and remaining
- Identify any scope changes made mid-sprint

If **~~chat** is connected:
- Search for sprint-related discussions and decisions
- Identify any blockers discussed in team channels
- Surface any customer reactions to recently shipped features

If **~~user feedback** is connected:
- Pull customer feedback related to features shipped this sprint
- Search for support ticket changes related to completed work
- Identify any new issues introduced by sprint deliverables

If these tools are not connected, ask the user to paste:
- List of completed stories with point values
- Sprint metrics (planned vs completed, velocity, bug count)
- Blockers encountered and how they were resolved
- Customer feedback received during the sprint

### 3. Generate the Sprint Summary

Produce a structured sprint review document. See the **sprint-execution** skill for detailed guidance on sprint metrics, demo preparation, and health indicators.

- **Sprint Overview**: Sprint name, dates, team, and goal — was the goal met?
- **Key Accomplishments**: Top 3-5 completed items with brief descriptions of user value delivered
- **Metrics Dashboard**: Velocity (planned vs completed), completion rate, bug count, carry-over items
- **Demo Highlights**: Features worth demonstrating, with a brief description of the user scenario
- **Blockers and Learnings**: Issues encountered, how they were resolved, and what the team learned
- **Customer Feedback**: Relevant customer reactions to shipped features or ongoing work
- **Next Sprint Preview**: What the team plans to work on next, with key items listed

### 4. Follow Up

After generating the summary:
- Offer to prepare a demo script for the sprint review meeting
- Offer to generate a TL;DR version for Slack
- Offer to create talking points for specific accomplishments
- Offer to draft a retrospective agenda based on the blockers and learnings

## Output Format

Use markdown with clear headers. Include a metrics summary table for easy scanning. Keep the document under 2 pages — sprint reviews should be digestible, not exhaustive.

## Tips

- Lead with what was shipped and the value it delivers, not the process of how it was built.
- Be honest about what did not get done. Carry-over is normal; hiding it is not.
- Metrics tell a story. If velocity dropped, explain why. If bugs spiked, explain the root cause.
- Demo highlights should tell a user story, not walk through a feature list.
- Customer feedback is the most valuable section for stakeholders. Include direct quotes when possible.
- The "Next Sprint Preview" builds confidence that the team has a clear plan ahead.
