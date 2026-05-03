# Scopes Architecture

Zoom OAuth uses scopes to limit API access. Understanding Classic vs Granular scopes is critical.

## Scope Types

| Type | Format | Example | Status |
|------|--------|---------|--------|
| **Classic** | `resource:level` | `meeting:write:admin` | Active |
| **Granular** | `service:action:data_claim:access` | `meeting:write:meeting:admin` | Active (newer) |

## Classic Scopes

### Format

```
{resource}:{action}:{level}
```

**Examples:**
- `meeting:read` - Read user's own meetings
- `meeting:write:admin` - Create/update meetings for all account users
- `recording:read:master` - Read recordings across all sub-accounts

### Scope Levels

| Level | Access | Who Can Authorize | Example |
|-------|--------|-------------------|---------|
| **(none)** | Own data only | Any user | `meeting:read` |
| `:admin` | Account-wide | Admin role required | `meeting:write:admin` |
| `:master` | Multi-account | Account owner only | `user:master` |

### Common Classic Scopes

```
meeting:read               # View own meetings
meeting:write              # Create/edit own meetings  
meeting:write:admin        # Manage all account meetings

user:read                  # View own profile
user:write:admin           # Manage account users

recording:read             # View own recordings
recording:write:admin      # Manage account recordings

webinar:read               # View own webinars
webinar:write:admin        # Manage account webinars

imchat:bot                 # Team Chat bot access
```

## Granular Scopes

### Format

```
{service}:{action}:{data_claim}:{access_level}
```

**Examples:**
- `meeting:read:meeting:user` - Read user's own meetings
- `meeting:write:invite_links:admin` - Create invite links for account
- `recording:delete:recording_file:admin` - Delete recording files account-wide

### Components

1. **service**: API category (meeting, user, recording, etc.)
2. **action**: Operation (read, write, delete, etc.)
3. **data_claim**: Specific data type (meeting, participant, invite_links, etc.)
4. **access_level**: Scope of access (user, admin, account, etc.)

### Access Levels (Granular)

| Level | Access | Example |
|-------|--------|---------|
| `user` | Own data | `meeting:read:meeting:user` |
| `admin` | Account-wide | `meeting:write:meeting:admin` |
| `account` | Account settings | `account:read:settings:account` |

## Classic vs Granular Comparison

### Meetings Scope Example

| Classic | Granular Equivalent |
|---------|---------------------|
| `meeting:read` | `meeting:read:meeting:user` + `meeting:read:list_meetings:user` |
| `meeting:write:admin` | `meeting:write:meeting:admin` + `meeting:write:settings:admin` + more |

### Why Granular Scopes Exist

**Classic scopes** are broad:
- `meeting:write:admin` grants ALL meeting write permissions account-wide
- Includes create, update, delete, settings, etc.

**Granular scopes** are specific:
- `meeting:write:meeting:admin` - Only create/update meetings
- `meeting:delete:meeting:admin` - Only delete meetings  
- `meeting:write:settings:admin` - Only update settings

**Principle of Least Privilege:** Request only the granular scopes you need.

## Choosing Between Classic and Granular

### Use Classic When:
- You need broad access (e.g., full meeting management)
- Simpler scope management preferred
- Legacy app migration

### Use Granular When:
- You need specific permissions only
- Implementing principle of least privilege
- Building security-sensitive apps

### Can You Mix?

✅ **Yes**, you can request both Classic and Granular scopes in the same app.

```
scope=meeting:read user:write:admin meeting:write:invite_links:admin
```

## Requesting Scopes

### During App Creation (S2S OAuth, Chatbot)

Scopes are configured in Zoom Marketplace:
1. Go to your app in https://marketplace.zoom.us
2. Click "Scopes" tab
3. Select required scopes (Classic or Granular)
4. Click "Continue"

Token will include all configured scopes.

### During Authorization (User OAuth, Device Flow)

Scopes are requested in authorization URL:

```javascript
const authURL = new URL('https://zoom.us/oauth/authorize');
authURL.searchParams.set('response_type', 'code');
authURL.searchParams.set('client_id', CLIENT_ID);
authURL.searchParams.set('redirect_uri', REDIRECT_URI);

// Request specific scopes (space-separated)
authURL.searchParams.set('scope', 'meeting:read user:read recording:read');

// User sees consent screen listing these scopes
```

## Scope Consent Screen

When user authorizes your app, they see:

```
[Your App Name] wants to:

✓ View your meetings (meeting:read)
✓ View your profile (user:read)  
✓ View your recordings (recording:read)

[Deny] [Authorize]
```

## Scope Errors

### Error 4711: Scope Mismatch

**Cause:** Token's scopes don't include required scope for API endpoint.

**Example:**
```javascript
// Token has: meeting:read
// API requires: meeting:write
await axios.post('https://api.zoom.us/v2/users/me/meetings', {...}, {
  headers: { Authorization: `Bearer ${token}` }
});
// Error 4711: Insufficient scope
```

**Solution:**
1. Add required scope in Zoom Marketplace (S2S/Chatbot)
2. OR request scope in authorization URL (User/Device)
3. Re-authorize user to grant new scopes

## Checking Token Scopes

### Decode Access Token Scopes

```javascript
// S2S OAuth: scopes returned in token response
const { access_token, scope } = tokenResponse.data;
console.log('Scopes:', scope); // "meeting:read user:read recording:write"

// User OAuth: scopes returned during token exchange
const { access_token, scope } = tokenResponse.data;
console.log('Granted scopes:', scope.split(' ')); // ['meeting:read', 'user:read', ...]
```

### API to Get Token Scopes

```bash
curl -H "Authorization: Bearer {access_token}" \
  https://zoom.us/oauth/token
```

## Best Practices

### 1. Request Minimum Scopes Needed

```javascript
// ❌ AVOID: Requesting broad admin access when not needed
scope: "meeting:write:admin user:write:admin recording:write:admin"

// ✅ PREFER: Request only what you need
scope: "meeting:read user:read"
```

### 2. Use Granular Scopes for Specific Operations

```javascript
// ❌ Classic (broad)
scope: "meeting:write:admin" // Includes create, update, delete, settings, etc.

// ✅ Granular (specific)
scope: "meeting:write:meeting:admin" // Only create/update meetings
```

### 3. Document Required Scopes

```javascript
/**
 * Create a meeting for a user
 * Required scope: meeting:write:admin (Classic) or meeting:write:meeting:admin (Granular)
 */
async function createMeeting(userId, meetingData) {
  // ...
}
```

## Reference Documentation

- **Classic Scopes** → [../references/classic-scopes.md](../references/classic-scopes.md)
- **Granular Scopes** → [../references/granular-scopes.md](../references/granular-scopes.md)
- **Scope Errors** → [../troubleshooting/scope-issues.md](../troubleshooting/scope-issues.md)
