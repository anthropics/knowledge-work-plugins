# Rivet Architecture and Lifecycle

## What Rivet Provides

Rivet wraps three concerns into one module client:
- Auth/token orchestration
- Webhook receiver + event dispatch
- Typed REST API endpoint wrappers

## Architecture Model

```text
+--------------------+        +------------------------------+
| Zoom Marketplace   |        | Your Rivet App               |
| App Config         |        | (Node.js/TypeScript)         |
+----------+---------+        +---------------+--------------+
           |                                  |
           | OAuth install / token exchange   |
           |--------------------------------->|
           |                                  |
           | Webhooks (POST /zoom/events)     |
           |--------------------------------->|
           |                                  v
           |                        +------------------------+
           |                        | Rivet Module Clients   |
           |                        | - ChatbotClient        |
           |                        | - TeamChatClient       |
           |                        | - Meetings*Client      |
           |                        | - Users*Client         |
           |                        | - Phone*Client         |
           |                        | - VideoSdkClient       |
           |                        +-----+------------+-----+
           |                              |            |
           |                              |            +--> webEventConsumer
           |                              |
           |                              +--> endpoints.* (REST wrappers)
           |                                           |
           |                                           v
           |                                  +------------------+
           +--------------------------------> | Zoom APIs        |
                                              +------------------+
```

## Lifecycle Workflow

1. Select module(s):
- Example: `ChatbotClient` + `TeamChatClient` for bot + channel lookup.
- Example: `UsersS2SAuthClient` + `MeetingsS2SAuthClient` for admin automation.

2. Pick auth model by module:
- Chatbot: Client Credentials
- Team Chat/Meetings/Phone/Accounts/Users: User OAuth or S2S OAuth
- Video SDK: JWT auth for Video SDK API

3. Configure client options:
- Required: `clientId`, `clientSecret`
- Often required: `webhooksSecretToken`
- Conditional: `accountId`, `installerOptions`, `receiver`, `port`, `tokenStore`

4. Register listeners:
- Generic: `webEventConsumer.event("event_name", handler)`
- Shortcuts where available: `onSlashCommand`, `onButtonClick`, `onChannelMessagePosted`

5. Start server(s):
- `await client.start()` returns server handler/address
- For multi-module apps, assign unique ports

6. Wire Marketplace subscriptions:
- Endpoint URL must target each module's receiver port
- Endpoint path should include `/zoom/events`

7. Process API + events:
- API calls via `client.endpoints.*`
- Event-driven actions via callback handlers

8. Operate and upgrade:
- Persist OAuth tokens/state for stable restarts
- Use changelog + TypeDoc workflow for version upgrades

## Why Multi-Client Port Strategy Matters

In sample patterns, each module runs its own receiver port. If multiple modules share one port by mistake, webhook routing and verification behavior can break in non-obvious ways.
