# Deprecations and Migration Notes (Zoom Phone)

## Timeline extracted from docs

- Legacy Call Logs API (v1) full deprecation: **April 2026**.
- Legacy Call Log webhooks (v1) full deprecation: **May 2026**.
- Legacy array fields deprecation:
- `call_log` array deprecation: **November 2026**.
- `call_path` array deprecation: **November 2026**.

## API migration map

- `GET /phone/call_logs` -> `GET /phone/call_history`
- `GET /phone/call_logs/{callLogId}` -> `GET /phone/call_history/{call_history_uuid}`
- `GET /phone/call_history_detail/{callHistoryId}` -> `GET /phone/call_element/{call_element_id}`

## Webhook migration map

- `phone.call_log_deleted` -> `phone.call_history_deleted` -> `phone.call_element_deleted`
- `phone.callee_call_log_completed` -> `phone.callee_call_history_completed` -> `phone.callee_call_element_completed`
- `phone.caller_call_log_completed` -> `phone.caller_call_history_completed` -> `phone.caller_call_element_completed`

## Compatibility strategy

- Standardize storage fields:
- `call_id`
- `call_history_uuid`
- `call_element_id`
- Add adapters for old/new field names during transition windows.
- Prefer v3 naming for all new features and schemas.
