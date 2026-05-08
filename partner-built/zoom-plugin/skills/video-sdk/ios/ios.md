# iOS Video SDK Overview

## What this platform skill is for

- Building custom iOS video experiences with UIKit or SwiftUI
- Managing session state with tokenized join and event callbacks
- Supporting camera, mic, share, chat, and optional advanced media flows

## Primary implementation path

1. Backend generates short-lived Video SDK token.
2. App initializes Video SDK and registers delegates.
3. App joins session with user identity + token.
4. App maps participant/media delegate events to UI state.
5. App handles leave/disconnect with explicit cleanup.

## Prerequisites

- iOS project with Video SDK binary integration
- Backend service for token generation
- Permissions handling for camera/mic

## Important notes

- Keep SDK key/secret on backend only.
- Prefer a deterministic session state machine to avoid UI desync.

## Source links

- Docs: https://developers.zoom.us/docs/video-sdk/ios/
- API reference: https://marketplacefront.zoom.us/sdk/custom/ios/annotated.html
