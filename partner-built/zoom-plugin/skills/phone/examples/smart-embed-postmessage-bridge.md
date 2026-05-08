# Smart Embed postMessage Bridge Pattern

## Why this pattern

Smart Embed event/control flow is `window.postMessage` based. Reliability depends on strict initialization order and origin validation.

## Pattern

```javascript
const ZOOM_ORIGIN = 'https://applications.zoom.us';
const iframe = document.querySelector('#zoom-embeddable-phone-iframe');

function initSmartEmbed(config) {
  iframe?.contentWindow?.postMessage({
    type: 'zp-init-config',
    data: config,
  }, ZOOM_ORIGIN);
}

function makeCall(number, callerId) {
  iframe?.contentWindow?.postMessage({
    type: 'zp-make-call',
    data: { number, callerId, autoDial: true },
  }, ZOOM_ORIGIN);
}

window.addEventListener('message', (event) => {
  if (event.origin !== ZOOM_ORIGIN) return;
  const payload = event.data;
  if (!payload?.type) return;

  switch (payload.type) {
    case 'zp-call-ringing-event':
    case 'zp-call-connected-event':
    case 'zp-call-ended-event':
    case 'zp-call-log-completed-event':
      handlePhoneEvent(payload);
      break;
    default:
      break;
  }
});
```

## Operational notes

- Call APIs only after iframe readiness callback.
- Persist `event.id` (if present) for idempotency.
- Keep event dispatcher tolerant to new event types.
