# REST API - Webinars

Webinar management endpoints.

## Overview

Create and manage Zoom webinars programmatically.

## Endpoints

### Create Webinar

```bash
POST /users/{userId}/webinars
```

```json
{
  "topic": "My Webinar",
  "type": 5,
  "start_time": "2024-01-15T10:00:00Z",
  "duration": 60,
  "settings": {
    "host_video": true,
    "panelists_video": true,
    "registration_type": 1
  }
}
```

### Get Webinar

```bash
GET /webinars/{webinarId}
```

### Update Webinar

```bash
PATCH /webinars/{webinarId}
```

### Delete Webinar

```bash
DELETE /webinars/{webinarId}
```

### List Webinar Registrants

```bash
GET /webinars/{webinarId}/registrants
```

### Add Registrant

```bash
POST /webinars/{webinarId}/registrants
```

## Webinar Types

| Type | Value | Description |
|------|-------|-------------|
| Webinar | 5 | Single webinar |
| Recurring (no fixed time) | 6 | Recurring, no schedule |
| Recurring (fixed time) | 9 | Recurring with schedule |

## Required Scopes

- `webinar:read` - View webinars
- `webinar:write` - Create/update/delete webinars

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Webinars
