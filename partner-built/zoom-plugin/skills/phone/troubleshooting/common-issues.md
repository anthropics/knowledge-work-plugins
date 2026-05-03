# Zoom Phone Common Issues

## Smart Embed event listener gets nothing

Checks:
- Iframe is loaded from `https://applications.zoom.us`.
- `onZoomPhoneIframeApiReady` sequence is respected.
- `postMessage` origin checks are correct.
- Approved domains configured in Zoom Phone Smart Embed app settings.

## OAuth works but API calls fail (401/403)

Checks:
- Required scopes are present and app was re-authorized.
- Access token is current (refresh flow works).
- Right app type and account context are used.

## Data fields missing after migration

Checks:
- Code expects old fields (`call_logs`, `call_path`) only.
- Endpoint path still points to legacy call log URLs.
- Webhook processor supports `call_element_id` fields.

## URI launch inconsistencies

Checks:
- Client is installed and signed in.
- Scheme is valid (`callto:`, `tel:`, `zoomphonecall://`, `zoomphonesms://`).
- Platform caveats are handled.
- Android caveat: docs explicitly note no `zoomphonecall`/`tel` support due to system limitations.

## Call handling API patch fails

Checks:
- `extensionId` target type is correct.
- Payload subsetting matches endpoint context.
- Phone numbers are E.164 where required.
- Enum/action values are valid for current API version.
