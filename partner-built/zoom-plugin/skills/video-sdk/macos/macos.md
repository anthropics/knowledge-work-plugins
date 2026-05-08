# macOS Video SDK Overview

## What this platform skill is for

- Building custom macOS desktop video experiences
- Managing richer desktop device, windowing, and render scenarios
- Integrating session controls with native app architectures

## Primary implementation path

1. Backend issues short-lived Video SDK token.
2. macOS app initializes SDK and event/delegate bridge.
3. App joins session and activates media controls.
4. App maps participant/media events to desktop windows/views.
5. App handles leave, shutdown, and resource cleanup safely.

## Prerequisites

- Xcode macOS app setup with SDK frameworks
- Token backend service
- Audio/video/screen permissions and entitlement checks

## Important notes

- Keep app-level session state management explicit.
- Validate entitlement and privacy prompts on clean machines.

## Source links

- Docs: https://developers.zoom.us/docs/video-sdk/macos/
- API reference: https://marketplacefront.zoom.us/sdk/custom/macos/annotated.html
