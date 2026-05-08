# Common Issues

Quick diagnostics for Zoom Video SDK UI Toolkit (Web).

## CSS Not Loading / UI Looks Unstyled

**Fix**:
- Ensure you import the toolkit CSS:
  - `@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css`
- For bundlers, verify CSS handling is enabled (Vite/Next.js).

## SSR / Next.js Errors ("window is not defined")

**Fix**:
- Load UI Toolkit only on the client (dynamic import in a client component).

## Session Doesn't Join

**Common causes**:
- Missing/invalid `videoSDKJWT`
- Expired JWT
- Using Meeting SDK credentials/signature instead of Video SDK credentials/JWT
- Session name/passcode mismatch

**Fix**:
- Generate JWT server-side; keep TTL short; check clock skew.
- Log the join errors surfaced by the toolkit callbacks.

## UI Renders Blank / Cropped

**Common cause**: The container has no height (common in flex layouts).

**Fix**:
- Ensure the container has an explicit height (for example `height: 100vh`).

## "I Need Granular UI Components"

**Reality**: UI Toolkit is optimized for fast, prebuilt UI. It’s not meant to expose every internal tile/control as a first-class primitive.

**Fix**:
- If you need fully custom layout, use raw **Zoom Video SDK** and build your own UI.
