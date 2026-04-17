# Interview Answer: Routing with zoom-general

Use `zoom-general` as the triage layer, then route implementation to specialized skills.

## Short answer

1. Classify the query in `zoom-general` by product intent, platform, and integration pattern.
2. Route to the minimum specialized skills:
- Auth/scopes -> `zoom-oauth`
- API operations -> `zoom-rest-api`
- Embedded meetings -> `zoom-meeting-sdk`
- Custom video experiences -> `zoom-video-sdk`
- Event delivery -> `zoom-webhooks` or `zoom-websockets`
- Live media/transcripts -> `zoom-rtms`
3. Execute in sequence: `zoom-general` -> auth -> core product -> events/media.
4. If ambiguous, ask one disambiguation question before locking the chain.

Canonical guidance and handoff structure:
- [Query Routing Playbook](query-routing-playbook.md)

