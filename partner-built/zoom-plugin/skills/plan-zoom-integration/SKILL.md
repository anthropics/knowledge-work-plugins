---
name: plan-zoom-integration
description: Turn a Zoom integration idea into an implementation plan with architecture, auth, and delivery milestones. Use when you need a practical build plan, phased delivery sequence, risk list, and next-step recommendation.
argument-hint: "<what you want to build>"
user-invocable: false
---

# /plan-zoom-integration

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Create a practical build plan for a Zoom integration or app.

## Usage

```text
/plan-zoom-integration $ARGUMENTS
```

## Workflow

1. Capture the target user flow and success criteria.
2. Choose the correct Zoom surface and supporting services.
3. Define auth requirements, scopes, and account assumptions.
4. Break implementation into phases: prototype, core integration, reliability, and launch.
5. Call out hard risks early: OAuth setup, webhook verification, SDK environment limits, marketplace review, or MCP client constraints.
6. End with the smallest deliverable that proves the architecture.

## Output

- Architecture summary
- Zoom products and APIs required
- Auth and scope checklist
- Delivery phases
- Risks, open questions, and immediate next action

## Related Skills

- [start](../start/SKILL.md)
- [setup-zoom-oauth](../setup-zoom-oauth/SKILL.md)
- [build-zoom-meeting-app](../build-zoom-meeting-app/SKILL.md)
- [build-zoom-bot](../build-zoom-bot/SKILL.md)
