# Video SDK Token Contract Test Spec

## Purpose

Define one backend token contract and validation sequence used by Android, iOS, macOS, and Unity clients.

## Contract inputs

| Field | Required | Description |
| --- | --- | --- |
| `sessionName` | Yes | Session/topic identifier used for join |
| `userName` | Yes | Display name in session |
| `roleType` | Optional | Role/permission shaping in token claims |
| `expirationSeconds` | Optional | Token TTL override within policy window |

## Contract output

| Field | Required | Description |
| --- | --- | --- |
| `token` | Yes | Short-lived Video SDK JWT |
| `expiresAt` | Yes | Absolute expiration timestamp |
| `sessionName` | Yes | Echoed join session identifier |

## Required backend assertions

1. Signing uses `ZOOM_VIDEO_SDK_KEY` + `ZOOM_VIDEO_SDK_SECRET` from server config.
2. Token TTL is short-lived and policy-compliant.
3. Response does not expose secret material.
4. Invalid input returns structured 4xx error payload.

## Client-side smoke test (all platforms)

1. Request token with same `sessionName` pattern and unique `userName`.
2. Join session using returned token.
3. Confirm join success callback/event.
4. Start local media and verify participant state event.
5. Leave session and verify cleanup callback/event.

## Failure diagnostics

- `join failed/auth` on one platform only:
  - compare claim payload handling and SDK version differences.
- `token expired` immediately:
  - check server clock drift and TTL config.
- `works native, fails Unity`:
  - validate wrapper supports same join/token expectation for this version.
