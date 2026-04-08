# Electron Meeting Embed

Use this flow when you need Zoom meetings embedded inside a desktop Electron application.

## When to Use

- You ship a desktop app with Electron.
- You need native-like meeting controls in app workflows.
- You need meeting modules beyond basic join/leave (recording, participants, share, raw data).

## Skill Chain

1. [meeting-sdk/electron](../../meeting-sdk/electron/SKILL.md)
2. [zoom-oauth](../../oauth/SKILL.md)

## Typical Flow

1. Backend signs short-lived Meeting SDK JWT.
2. Electron app initializes SDK and authenticates.
3. App joins/starts meeting and binds controllers.
4. Optional advanced modules (raw data, webinar, whiteboard) are enabled as needed.
5. App leaves and performs explicit SDK cleanup.

## References

- [Electron Meeting SDK Skill](../../meeting-sdk/electron/SKILL.md)
- [Lifecycle Workflow](../../meeting-sdk/electron/concepts/lifecycle-workflow.md)
- [Deprecated and Contradictions](../../meeting-sdk/electron/troubleshooting/deprecated-and-contradictions.md)
