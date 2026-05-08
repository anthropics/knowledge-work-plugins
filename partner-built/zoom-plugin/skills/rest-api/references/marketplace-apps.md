# Zoom Marketplace API

Authoritative endpoint inventory for Marketplace. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/marketplace/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 27 |
| Path templates | 19 |
| Tags | 3 |

## Tag Index

| Tag | Operations |
|-----|------------|
| App | 23 |
| Apps | 1 |
| Manifest | 3 |

## Endpoints by Tag

### App

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/app/notifications` | Send app notifications | `Sendappnotifications` |
| GET | `/marketplace/app/custom_fields` | Get user's custom field values | `getCustomFieldValues` |
| DELETE | `/marketplace/app/event_subscription` | Unsubscribe app event subscription | `unSubscribeEventSubscription` |
| GET | `/marketplace/app/event_subscription` | Get user or account event subscription | `getUserEventSubscriptions` |
| POST | `/marketplace/app/event_subscription` | Create an event subscription | `createEventSubscription` |
| DELETE | `/marketplace/app/event_subscription/{eventSubscriptionId}` | Delete an event subscription | `deleteEventSubscription` |
| PATCH | `/marketplace/app/event_subscription/{eventSubscriptionId}` | Subscribe an event subscription | `subscribeEventSubscription` |
| GET | `/marketplace/apps` | List apps | `ListApps` |
| POST | `/marketplace/apps` | Create apps | `CreateApps` |
| DELETE | `/marketplace/apps/{appId}` | Deletes an app | `deleteApp` |
| GET | `/marketplace/apps/{appId}` | Get information about an app | `getAppInfo` |
| GET | `/marketplace/apps/{appId}/api_call_logs` | Get API call logs | `Getapicalllogs` |
| POST | `/marketplace/apps/{appId}/deeplink` | Generate Zoom App Deeplink | `GenerateZoomAppDeeplink` |
| POST | `/marketplace/apps/{appId}/preApprove` | Update app pre approval setting | `Updateapppreapprovalsetting` |
| GET | `/marketplace/apps/{appId}/requests` | Get an app's user requests | `getAppUserRequests` |
| PATCH | `/marketplace/apps/{appId}/requests` | Update app's request status | `updateAppRequestStatus` |
| POST | `/marketplace/apps/{appId}/requests` | Add app allow requests for users | `AddAppAllowRequestsForUsers` |
| POST | `/marketplace/apps/{appId}/rotate_client_secret` | Rotate client secret | `RotateClientSecret` |
| GET | `/marketplace/apps/{appId}/webhook_logs` | Get webhook logs | `getWebhookLogs` |
| GET | `/marketplace/monetization/entitlements` | Get app user entitlements | `getAppUserEntitlementRequests` |
| GET | `/marketplace/users/{userId}/apps` | Get a user's app requests | `getUserAppRequests` |
| PATCH | `/marketplace/users/{userId}/apps/{appId}/subscription` | Enable or disable user app subscription | `Enable/Disableuserappsubscription` |
| GET | `/marketplace/users/{userId}/entitlements` | Get a user's entitlements | `getUserEntitlementRequests` |

### Apps

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/zoomapp/deeplink` | Generate an app deeplink | `generateAppDeeplink` |

### Manifest

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/marketplace/apps/manifest/validate` | Validate an app manifest | `validatingManifest` |
| GET | `/marketplace/apps/{appId}/manifest` | Export an app manifest from an existing app | `getAppManifest` |
| PUT | `/marketplace/apps/{appId}/manifest` | Update an app by manifest | `updateAppByManifest` |
