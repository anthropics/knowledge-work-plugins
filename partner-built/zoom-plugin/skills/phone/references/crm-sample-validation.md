# CRM Sample Validation (https://github.com/zoom/CRM-Sample)

## Useful architecture patterns adopted

- Smart Embed as dedicated iframe sidebar component.
- Server-only OAuth token handling with `next-auth` callbacks.
- API route pattern that reads session token and calls Phone APIs.
- Client-side event listener for Smart Embed message events.

## Environment keys observed in sample

- `ZOOM_CLIENT_ID`
- `ZOOM_CLIENT_SECRET`
- `NEXTAUTH_URL`
- `NEXTAUTH_SECRET`

## Lifecycle pattern extracted

1. User authenticates with Zoom OAuth.
2. Server stores access/refresh token session state.
3. UI renders Smart Embed iframe.
4. UI sends click-to-call command and listens for events.
5. Backend fetches call history/contact data for CRM views.

## Contradictions and drift issues found

- Sample still maps response via `data.call_logs` (legacy shape) while migration docs push toward call history/call element shapes.
- README references `.env.example`, repository provides `.env.sample`.
- Middleware matcher and route naming are inconsistent (`/call-log` vs `/call-logs`, missing `/api/calls/[id]` route used by modal).
- Sample contains hardcoded demo records in some screens alongside live API calls.

## Guidance

- Treat sample as architectural reference, not canonical API contract.
- Apply migration-safe normalizers for call history fields.
- Validate each endpoint payload against current Phone API docs.
