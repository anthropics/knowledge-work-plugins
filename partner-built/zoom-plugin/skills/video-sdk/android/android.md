# Android Video SDK Overview

## What this platform skill is for

- Building fully custom Android video session UI (not Zoom Meeting UI)
- Managing join/leave and participant state via Video SDK events
- Handling camera, mic, share, chat, command, and optional raw data paths

## Primary implementation path

1. Backend generates short-lived Video SDK token using Video SDK Key/Secret.
2. Android initializes SDK and joins a session by `sessionName` + token.
3. App binds SDK events to UI state (user join/leave, video/audio/share changes).
4. App starts/stops media explicitly and cleans up SDK resources on leave.

## Prerequisites

- Android Studio + supported Gradle/AGP stack
- Video SDK Android package (`mobilertc.aar`)
- Backend token endpoint for Video SDK JWT generation
- Camera/microphone permissions flow and runtime handling

## Important notes

- Video SDK session auth is token-based and server-generated.
- Do not use Meeting SDK payload fields (`meetingNumber`, `passWord`) in Video SDK flows.
- Keep token generation and key/secret handling server-side only.

## Source links

- Docs: https://developers.zoom.us/docs/video-sdk/android/
- API reference: https://marketplacefront.zoom.us/sdk/custom/android/index.html
