# Unity Video SDK Overview

## What this platform skill is for

- Integrating Zoom Video SDK wrapper into Unity projects
- Building custom in-scene video interaction experiences
- Mapping session lifecycle and participant events into Unity game loop/UI

## Primary implementation path

1. Backend generates short-lived Video SDK token.
2. Unity initializes wrapper objects and event bindings.
3. Unity joins session with session name and user identity.
4. Unity updates scene/UI based on SDK callbacks.
5. Unity leaves session and disposes wrapper resources cleanly.

## Prerequisites

- Unity project with packaged `ZoomVideoSDK.unitypackage`
- Backend token endpoint
- Platform-specific permissions for mic/camera on target builds

## Important notes

- Unity wrapper version may lag native SDK versions.
- Validate feature availability before promising parity with native platforms.

## Source links

- Docs: https://developers.zoom.us/docs/video-sdk/unity/
- API reference: https://marketplacefront.zoom.us/sdk/custom/unity/index.html
