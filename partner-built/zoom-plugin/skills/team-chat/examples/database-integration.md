# Database Integration (Stateful Bots)

Store state when you need:

- multi-step workflows
- approvals
- linking Zoom users to internal system users

## Suggested Tables

- `installations` (account_id, bot_jid, created_at)
- `users` (zoom_jid, internal_user_id)
- `workflows` (workflow_id, status, payload_json)

