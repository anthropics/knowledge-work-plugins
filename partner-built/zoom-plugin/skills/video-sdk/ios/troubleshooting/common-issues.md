# iOS Common Issues

## Join fails with token/auth error

- Validate token issuer, expiry, and Video SDK key pairing.
- Ensure backend and app use the same environment/project credentials.

## Media controls appear stuck

- Verify delegate callback sequencing and app state transitions.
- Confirm camera/mic permission prompts were accepted.

## Participant list/video tiles desync

- Rebuild UI from delegate events, not cached arrays only.
- Handle reconnect and app foreground/background transitions.

## Build/runtime binary issues

- Confirm framework embedding/signing setup.
- Reconcile architecture slices and deployment target requirements.
