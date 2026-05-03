# Unity Common Issues

## Missing API from native docs

- Confirm API exists in Unity wrapper reference, not just native SDK docs.
- Implement fallback logic for unsupported wrapper features.

## Join/session event issues

- Verify token validity and wrapper event binding order.
- Ensure scene lifecycle does not drop active handlers.

## Platform build permission problems

- Confirm microphone/camera permissions for target platform build settings.
- Re-test on clean devices with fresh permission prompts.

## Rendering/state mismatch

- Keep scene state synchronized from SDK events.
- Reset participant objects on leave/rejoin transitions.
