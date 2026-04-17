# OAuth Scopes

OAuth scopes define what your app can access.

## Overview

Scopes are permissions requested during OAuth authorization. Request only the scopes you need.

## IMPORTANT: Scope Types

**Different OAuth types have different scopes available:**

| OAuth Type | Scope Suffix | Access Level | Example |
|------------|--------------|--------------|---------|
| **User OAuth** | (none) | Current user's data only | `meeting:read` |
| **Admin OAuth** | `:admin` | All users in account | `meeting:read:admin` |
| **Server-to-Server (S2S)** | `:admin` | All users in account (no user consent) | `meeting:read:admin` |

### Key Differences

- **User scopes** (`meeting:read`): Access only the authenticated user's data
- **Admin scopes** (`meeting:read:admin`): Access data for ALL users in the account
- **S2S OAuth**: Uses admin-level scopes but doesn't require user login - intended for backend integrations

### Choosing the Right Scope Type

| Use Case | OAuth Type | Scope Example |
|----------|------------|---------------|
| User manages their own meetings | User OAuth | `meeting:write` |
| Admin dashboard for all users | Admin OAuth | `meeting:read:admin` |
| Backend automation (no user login) | Server-to-Server | `meeting:write:admin` |
| Bot that creates meetings for users | Server-to-Server | `meeting:write:admin` |

## Common Scopes

### Meetings

| User Scope | Admin Scope | Description |
|------------|-------------|-------------|
| `meeting:read` | `meeting:read:admin` | View meeting details |
| `meeting:write` | `meeting:write:admin` | Create, update, delete meetings |
| `meeting:master` | `meeting:master:admin` | Full meeting access |

### Users

| User Scope | Admin Scope | Description |
|------------|-------------|-------------|
| `user:read` | `user:read:admin` | View user profile |
| `user:write` | `user:write:admin` | Update user settings |
| `user:master` | `user:master:admin` | Full user access |

### Recordings

| User Scope | Admin Scope | Description |
|------------|-------------|-------------|
| `recording:read` | `recording:read:admin` | View/download recordings |
| `recording:write` | `recording:write:admin` | Delete recordings |
| `recording:master` | `recording:master:admin` | Full recording access |

### Webinars

| User Scope | Admin Scope | Description |
|------------|-------------|-------------|
| `webinar:read` | `webinar:read:admin` | View webinar details |
| `webinar:write` | `webinar:write:admin` | Create, update webinars |
| `webinar:master` | `webinar:master:admin` | Full webinar access |

### Reports

| User Scope | Admin Scope | Description |
|------------|-------------|-------------|
| `report:read` | `report:read:admin` | View reports and analytics |
| `report:master` | `report:master:admin` | Full report access |

## Scope Patterns

| Pattern | Meaning |
|---------|---------|
| `resource:read` | Read-only access (current user) |
| `resource:write` | Read and write access (current user) |
| `resource:master` | Full access including delete (current user) |
| `resource:read:admin` | Read-only access (all account users) |
| `resource:write:admin` | Read and write access (all account users) |
| `resource:master:admin` | Full access including delete (all account users) |

## Best Practices

1. **Request minimum scopes** - Only what you need
2. **Explain to users** - Why you need each scope
3. **Handle denied scopes** - Graceful fallback

## Resources

- **Scopes reference**: https://developers.zoom.us/docs/integrations/oauth-scopes/
