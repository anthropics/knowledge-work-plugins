# Phone API Service Pattern (Migration-Safe)

## Pattern goals

- Isolate OAuth token usage to server code.
- Support current call history/call element model.
- Keep compatibility with old payload fields while migrating.

## Service example

```javascript
export async function getCallHistory(accessToken, from, to) {
  const qs = new URLSearchParams({ from, to }).toString();
  const res = await fetch(`https://api.zoom.us/v2/phone/call_history?${qs}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!res.ok) throw new Error(`call_history failed: ${res.status}`);

  const data = await res.json();

  // Normalize v2/v3 style for downstream code.
  return (data.call_history || data.call_logs || []).map((row) => ({
    callHistoryUuid: row.call_history_uuid || row.id,
    callId: row.call_id,
    raw: row,
  }));
}

export async function getCallElement(accessToken, callElementId) {
  const res = await fetch(`https://api.zoom.us/v2/phone/call_element/${callElementId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!res.ok) throw new Error(`call_element failed: ${res.status}`);
  return res.json();
}
```

## Operational notes

- Add explicit logging when fallback fields (`call_logs`, `call_path`) are encountered.
- Remove fallback path once migration is complete.
