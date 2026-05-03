# Contact Center Integration

Build support and engagement workflows with Zoom Contact Center across app, web, and mobile surfaces.

## Skills Needed

- `contact-center` (primary)
- `zoom-apps-sdk` (for Contact Center apps in Zoom client)
- `zoom-rest-api` (for Contact Center API automation)
- `zoom-oauth` (for authorization patterns)

## Choose the Surface

1. Contact Center app in Zoom client:
- Use engagement APIs/events and state by `engagementId`.
2. Website embed:
- Use campaign/web SDK scripts with readiness gating.
3. Native mobile:
- Use Android/iOS SDK service lifecycle patterns.

## Core Architecture

1. Initialize context and identity.
2. Start channel service (chat/video/ZVA/scheduled callback).
3. Handle engagement events and context switches.
4. Persist engagement-scoped workflow state.
5. End and cleanup channel services.

## High-Value Use Cases

- Agent notes app keyed by engagement.
- CRM integration with Smart Embed events.
- Campaign-driven routing to chat/video channels.
- Native app rejoin flow for dropped video sessions.

## Where to Go Next

- `../../contact-center/SKILL.md`
- `../../contact-center/RUNBOOK.md`
