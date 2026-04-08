# Send Your First Message (Team Chat API)

This is for **Team Chat API** (messages sent as the authenticated user).

## Endpoint

`POST https://api.zoom.us/v2/chat/users/me/messages`

## Minimal Payload

```json
{
  "message": "Hello from my integration",
  "to_channel": "CHANNEL_ID"
}
```

## Common Pitfalls

- `to_channel` must be a channel the user can access.
- Use the correct scopes:
  - `chat_message:write`

