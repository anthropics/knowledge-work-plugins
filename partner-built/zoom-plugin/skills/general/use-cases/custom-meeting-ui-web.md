# Custom Meeting UI (Web)

Build a custom video user interface around a real Zoom meeting in a web application.

## Correct Skill Path

- Primary skill: [../../meeting-sdk/web/component-view/SKILL.md](../../meeting-sdk/web/component-view/SKILL.md)
- Supporting auth guidance: [../../oauth/SKILL.md](../../oauth/SKILL.md)

Do not route this use case to Video SDK unless the user is building a non-meeting custom
session product.

## Why Component View

Use Meeting SDK Component View when:
- the app must join a real Zoom meeting
- the meeting should render inside your page layout
- you need custom placement and styling around the Zoom meeting UI
- you still want Zoom meeting semantics such as real meeting join/start behavior

Do not use Video SDK when:
- the requirement is specifically a Zoom meeting
- the user expects Meeting SDK auth, meeting numbers, passwords, ZAK/OBF rules, or webinar behavior

## Minimal Architecture

```text
Browser UI
  -> fetch signature from backend
  -> ZoomMtgEmbedded.createClient()
  -> client.init({ zoomAppRoot })
  -> client.join({ signature, sdkKey, meetingNumber, userName, password })
```

## Minimal Flow

1. Create a backend signature endpoint.
2. In the browser, create one `ZoomMtgEmbedded` client instance.
3. Initialize it with a real DOM container.
4. Join using backend-generated signature plus meeting credentials.
5. Handle join/init errors explicitly in UI state.

## Minimal Example

```javascript
import ZoomMtgEmbedded from '@zoom/meetingsdk/embedded';

const client = ZoomMtgEmbedded.createClient();

export async function joinEmbeddedMeeting({
  meetingNumber,
  userName,
  password,
}) {
  const res = await fetch('/api/signature', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ meetingNumber, role: 0 }),
  });

  if (!res.ok) {
    throw new Error(`signature_fetch_failed:${res.status}`);
  }

  const { signature, sdkKey } = await res.json();

  await client.init({
    zoomAppRoot: document.getElementById('meetingSDKElement'),
    language: 'en-US',
    patchJsMedia: true,
    leaveOnPageUnload: true,
  });

  await client.join({
    signature,
    sdkKey,
    meetingNumber,
    userName,
    password,
  });
}
```

## Common Failure Points

- Wrong route: using Video SDK instead of Meeting SDK Component View
- Missing backend signature generation
- Wrong password field name in the wrong view (`password` here, not `passWord`)
- Missing OBF/ZAK requirements for meetings outside the app account
- Missing SharedArrayBuffer headers when higher-end web meeting features are expected

## References

- [../../meeting-sdk/web/SKILL.md](../../meeting-sdk/web/SKILL.md)
- [../../meeting-sdk/web/component-view/SKILL.md](../../meeting-sdk/web/component-view/SKILL.md)
- [../../meeting-sdk/web/troubleshooting/error-codes.md](../../meeting-sdk/web/troubleshooting/error-codes.md)
