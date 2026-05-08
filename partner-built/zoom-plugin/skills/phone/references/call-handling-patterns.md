# Call Handling API Patterns

## Endpoint family

- `POST /phone/extension/{extensionId}/call_handling/settings/{settingType}`
- `PATCH /phone/extension/{extensionId}/call_handling/settings/{settingType}`
- `GET /phone/extension/{extensionId}/call_handling/settings`

## Supported extension targets

- Users
- Auto receptionists
- Call queues

## Common subsettings

- `custom_hours`
- `holiday`
- `call_handling`
- `call_forwarding` (user-focused)

## Practical implementation pattern

1. Read current settings snapshot with `GET`.
2. Build small, typed patch payloads by subsetting.
3. Update business/closed/holiday hours independently.
4. Validate E.164 formatting for external phone numbers.
5. Store previous settings for rollback.

## Drift watchpoints

- Enum/action values may evolve.
- Routing field names differ between docs sections and old implementations.
- Keep a server-side validator to reject malformed call-handling payloads before API call.
