# REST API - Reports

Usage reports and analytics endpoints.

## Overview

Access meeting statistics, usage reports, and analytics data.

## Endpoints

### Daily Usage Report

```bash
GET /report/daily
```

Query parameters:
- `year` - Year (required)
- `month` - Month (required)

### Meeting Participants Report

```bash
GET /report/meetings/{meetingId}/participants
```

### Meeting Details Report

```bash
GET /report/meetings/{meetingId}
```

### Webinar Participants Report

```bash
GET /report/webinars/{webinarId}/participants
```

### Active/Inactive Host Report

```bash
GET /report/users
```

## Response Data

### Daily Usage

```json
{
  "dates": [
    {
      "date": "2024-01-15",
      "new_users": 5,
      "meetings": 25,
      "participants": 150,
      "meeting_minutes": 3600
    }
  ]
}
```

### Meeting Participants

```json
{
  "participants": [
    {
      "id": "user_id",
      "name": "User Name",
      "user_email": "user@example.com",
      "join_time": "2024-01-15T10:00:00Z",
      "leave_time": "2024-01-15T11:00:00Z",
      "duration": 3600
    }
  ]
}
```

## Required Scopes

- `report:read` - View reports

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Reports
