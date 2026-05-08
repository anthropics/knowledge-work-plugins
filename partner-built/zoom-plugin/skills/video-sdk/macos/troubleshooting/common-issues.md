# macOS Common Issues

## Session join fails

- Verify token validity and expiration.
- Confirm app/backend use matching Video SDK credentials.

## Camera/mic/share unavailable

- Check macOS privacy permission prompts and app entitlements.
- Confirm device selection and active session state.

## Render or participant state mismatch

- Reconcile UI updates with delegate event order.
- Handle reconnect and window lifecycle transitions explicitly.

## Framework/load issues

- Validate embed/sign settings in Xcode target.
- Check architecture and minimum macOS version compatibility.
