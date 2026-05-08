# Video SDK 5-Minute Preflight Runbook

Use this before deep debugging. It catches the most common Video SDK failures fast.

## Skill Doc Standard Note

- Agent-skill standard entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- `SKILL.md` is also a navigation convention for larger skill docs.

## 1) Confirm Product Choice

- Video SDK is for custom video experiences (not Zoom Meeting UI).
- If you expect native Zoom meeting UI behavior, use Meeting SDK instead.

## 2) Confirm Lifecycle Order

Required order:
1. `createClient()`
2. `init()`
3. `join()`
4. `getMediaStream()`
5. `startAudio()` / `startVideo()`

Calling stream APIs before `join()` causes silent failures.

## 3) Confirm Token Generation

- JWT must be generated server-side.
- Validate `app_key`, `role_type`, `tpc`, `iat`, `exp` claims.
- Ensure topic (`tpc`) matches what clients join with.

## 4) Confirm Rendering Pattern

- Use event-driven attach/detach flow for participant video.
- Handle user join/leave and peer video state changes.
- Do not assume remote video auto-renders.

## 5) Confirm Delivery Method

- npm vs CDN globals differ (`ZoomVideo` vs `WebVideoSDK.default`).
- In CDN/module setups, guard for SDK-load race conditions.

## 6) Quick Probes

- Signature endpoint returns valid JWT payload.
- Join succeeds for two users on same `topic`.
- Audio/video start calls return success.
- Browser logs show no mixed-content/CORS blocking.

### Copy/Paste Validation Commands

```bash
# 1) Verify signature/token endpoint responds
curl -sS -i "$VIDEO_SDK_BASE_URL/api/signature"

# 2) Verify app page is reachable
curl -sS -i "$VIDEO_SDK_BASE_URL"
```

Expected: JSON from token endpoint and HTML from app route.

## 7) Fast Decision Tree

- **No media stream** -> check lifecycle order (`getMediaStream` after `join`).
- **Only local video works** -> missing event-driven remote attach flow.
- **Join auth errors** -> JWT claims mismatch or expired token.

## 8) SDK Selection Guardrail

- Use Video SDK for custom video sessions you design.
- Use Meeting SDK for Zoom-native meeting experience embedding.

## 9) Wrong-Path Detector (SDK vs REST/Meeting SDK)

- If implementation asks for `meetingNumber` or uses `join_url`, you are not in Video SDK flow.
- If implementation creates resources via `/v2/meetings` for join flow, you are on REST/Meeting path.
- For Video SDK MVP, require: Video SDK JWT + `client.join(topic, ...)` + media stream lifecycle.
