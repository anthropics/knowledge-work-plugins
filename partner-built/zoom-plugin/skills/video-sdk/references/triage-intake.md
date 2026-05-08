---
title: "Video SDK Triage Intake (What to Ask First)"
---

# Video SDK Triage Intake (What to Ask First)

Use this when someone asks “Video SDK isn’t working” without enough context.

## 1) Platform + UI Choice

- Platform: `web` | `react-native` | `flutter` | `ios` | `android` | `windows` | `linux`
- UI approach:
  - **UI Toolkit** (`@zoom/videosdk-zoom-ui-toolkit`)
  - **Custom UI** (direct SDK APIs)

## 2) Session Basics (Copy/Paste)

- `topic` / `sessionName` (must match exactly across joiners)
- `userName`
- `password` / `sessionPasscode` (if used)
- SDK version + UI Toolkit version (if applicable)

## 3) Auth (Signature/JWT)

- Confirm signature/JWT is generated **server-side**
- Confirm expiry/clock skew if joins fail

## 4) Symptom Bucket

- join fails
- video not rendering / self-view black (often browser/device permissions or lifecycle ordering)
- audio not starting / audio route changes
- screen share issues
- performance/latency/freezing (browser differences matter)

## 5) Logs + Minimal Repro

- Minimal reproduction steps
- SDK logs (see `general/references/sdk-logs-troubleshooting.md`)
- Web: browser + OS + console errors + whether SAB/crossOriginIsolated is configured (if relevant)

