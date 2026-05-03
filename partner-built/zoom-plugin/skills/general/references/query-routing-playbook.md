# Query Routing Playbook (zoom-general)

Use `zoom-general` as the routing/orchestration layer.  
Do not implement product-specific logic in `zoom-general` if a specialized skill exists.

## Goal

Convert a complex developer query into:
- `selected_skills`
- `execution_order`
- `assumptions`
- `next_actions`

## Routing rules

| Query signal | Route to skill | Why |
|---|---|---|
| OAuth, scopes, S2S, token strategy | `zoom-oauth` | Authentication and authorization design |
| Meetings/users/recordings/reports API operations | `zoom-rest-api` | Server-side Zoom resource management |
| Embed full Zoom meetings/webinars | `zoom-meeting-sdk` | Meeting runtime integration |
| Build custom video session experience | `zoom-video-sdk` | Custom media UX runtime |
| Receive event callbacks via HTTP | `zoom-webhooks` | Event lifecycle notifications |
| Need lower-latency event stream | `zoom-websockets` | Persistent real-time event transport |
| Live audio/video/transcript stream ingestion | `zoom-rtms` | Real-time media and transcript pipeline |
| App runs inside Zoom client | `zoom-apps-sdk` | In-client app model and APIs |

## Sequencing

1. Start with `zoom-general` (triage and architecture).
2. Add `zoom-oauth` if any protected resource access is required.
3. Select one primary runtime/API skill (`zoom-meeting-sdk`, `zoom-video-sdk`, or `zoom-rest-api`).
4. Add event/media skills (`zoom-webhooks`, `zoom-websockets`, `zoom-rtms`) based on requirements.
5. Keep the chain minimal; do not add extra skills without explicit need.

## Handoff contract

```json
{
  "selected_skills": [
    "zoom-general",
    "zoom-oauth",
    "zoom-meeting-sdk",
    "zoom-webhooks"
  ],
  "execution_order": [
    "zoom-general",
    "zoom-oauth",
    "zoom-meeting-sdk",
    "zoom-webhooks"
  ],
  "assumptions": [
    "embedded meeting experience required",
    "server-side event endpoint available"
  ],
  "next_actions": [
    "confirm OAuth scopes",
    "implement auth/token flow",
    "implement runtime integration",
    "implement event consumer and verification"
  ]
}
```

## Ambiguity handling

If confidence is low, ask one focused question before final routing:
- “Do you need embedded Zoom meetings, or a fully custom video session UI?”
- “Is webhook latency acceptable, or do you require persistent low-latency events?”

## Example route

Query: “Build a Linux bot that joins meetings, auto-creates meetings, streams transcript, and tracks lifecycle events.”

Recommended chain:
- `zoom-general`
- `zoom-oauth`
- `zoom-rest-api`
- `zoom-meeting-sdk`
- `zoom-rtms`
- `zoom-webhooks`

Why:
- `zoom-rest-api` for meeting provisioning
- `zoom-meeting-sdk` for runtime join/control
- `zoom-rtms` for live transcript/media stream
- `zoom-webhooks` for lifecycle notifications

