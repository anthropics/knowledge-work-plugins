# Zoom Chatbot API

Authoritative endpoint inventory for Chatbot. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/chatbot/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 4 |
| Path templates | 3 |
| Tags | 1 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Chatbot Messages | 4 |

## Endpoints by Tag

### Chatbot Messages

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/im/chat/messages` | Send Chatbot messages | `sendChatbot` |
| DELETE | `/im/chat/messages/{message_id}` | Delete a Chatbot message | `deleteAChatbotMessage` |
| PUT | `/im/chat/messages/{message_id}` | Edit a Chatbot message | `editChatbotMessage` |
| POST | `/im/chat/users/{userId}/unfurls/{triggerId}` | Link Unfurls | `unfurlingLink` |
