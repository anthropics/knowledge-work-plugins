# Common Errors - HTTP Status Codes and Zoom Error Codes

Complete reference for Zoom REST API error codes, HTTP status codes, and solutions.

## HTTP Status Codes

### 2XX - Success

| Status | Description | Action |
|--------|-------------|--------|
| `200 OK` | Request succeeded | Parse response body |
| `201 Created` | Resource created | Check `Location` header for new resource URL |
| `204 No Content` | Request succeeded, no body | Common for UPDATE/DELETE operations |

### 4XX - Client Errors

| Status | Description | Common Causes | Solution |
|--------|-------------|---------------|----------|
| `400 Bad Request` | Invalid request | Missing required fields, invalid JSON, validation errors | Check request body format and required fields |
| `401 Unauthorized` | Authentication failed | Invalid/expired token, missing `Authorization` header | Refresh access token, check token format |
| `403 Forbidden` | Permission denied | Missing scopes, user lacks permission, shared access not granted | Add required scopes, check user role |
| `404 Not Found` | Resource doesn't exist | Invalid userId/meetingId, wrong `me` keyword usage | Verify resource ID, check `me` keyword rules |
| `409 Conflict` | Resource conflict | Email already exists, duplicate operation | Use unique identifiers |
| `429 Too Many Requests` | Rate limit exceeded | Too many requests per second/day | Implement exponential backoff, throttle requests |

### 5XX - Server Errors

| Status | Description | Action |
|--------|-------------|--------|
| `500 Internal Server Error` | Zoom server error | Retry with exponential backoff |
| `502 Bad Gateway` | Gateway error | Retry after delay |
| `503 Service Unavailable` | Zoom service down | Check [status.zoom.us](https://status.zoom.us), retry later |

## Zoom Error Codes

When an API call fails, Zoom returns an error response:

```json
{
  "code": 300,
  "message": "Request Body should be a valid JSON object."
}
```

### Common Zoom Error Codes

| Code | HTTP | Message | Cause | Solution |
|------|------|---------|-------|----------|
| `300` | 400 | Invalid request | Bad JSON, validation error | Check request body structure |
| `124` | 400 | Invalid parameter | Wrong parameter type/value | Validate parameters against API docs |
| `200` | 401 | Invalid credentials | Incorrect OAuth token | Refresh access token |
| `201` | 401 | Access token expired | Token expired | Request new token |
| `1001` | 404 | User does not exist | Invalid userId or wrong `me` usage | Check userId, review `me` keyword rules |
| `300` | 404 | Meeting not found | Invalid meetingId | Verify meeting exists |
| `3000` | 404 | Cannot access webinar info | Webinar doesn't exist or no access | Check webinarId and scopes |
| `200` | 429 | Rate limit exceeded | Too many requests | Implement rate limiting |
| `4700` | 401 | Invalid access token | Token missing scopes | Add required scopes in app config |
| `3001` | 403 | Not allowed to access | Missing permission | Upgrade user role or add scope |

## Detailed Error Scenarios

### 401 Unauthorized

#### Scenario 1: Token Expired

```json
{
  "code": 201,
  "message": "Access token is expired."
}
```

**Solution:**
```javascript
async function apiCallWithRetry(url, options) {
  try {
    const response = await fetch(url, options);
    
    if (response.status === 401) {
      const error = await response.json();
      
      if (error.code === 201) {
        // Token expired - refresh and retry
        const newToken = await refreshAccessToken();
        options.headers['Authorization'] = `Bearer ${newToken}`;
        return await fetch(url, options);
      }
    }
    
    return response;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}
```

#### Scenario 2: Missing/Invalid Token

```json
{
  "code": 200,
  "message": "Invalid credentials."
}
```

**Solution:**
- Check `Authorization` header is present: `Authorization: Bearer ACCESS_TOKEN`
- Verify token format (should be JWT)
- Ensure token is for the correct account

#### Scenario 3: Missing Scopes

```json
{
  "code": 4700,
  "message": "Invalid access token, does not contain scopes."
}
```

**Solution:**
1. Go to your app on Zoom Marketplace
2. Add required scopes (e.g., `meeting:write:admin`)
3. Request new access token with updated scopes

### 403 Forbidden

#### Scenario 1: Missing Permission

```json
{
  "code": 3001,
  "message": "This user is not allowed to access this resource."
}
```

**Solution:**
- Verify user has appropriate role (Admin, Owner)
- Check if endpoint requires admin-level scopes
- Use account-level scope (e.g., `meeting:write:admin` instead of `meeting:write`)

#### Scenario 2: Shared Access Permissions

```json
{
  "code": 3001,
  "message": "Authenticated user has not permitted access to the targeted resource."
}
```

**Cause:** User hasn't authorized shared access permissions for your app.

**Solution:** Direct user to: [Allowing Apps Access to Shared Access Permissions](https://support.zoom.us/hc/en-us/articles/4413265586189)

### 404 Not Found

#### Scenario 1: User Not Found (Wrong `me` Usage)

```json
{
  "code": 1001,
  "message": "User does not exist: user@example.com"
}
```

**Cause:** Using `userId` with User OAuth app (should use `me`).

**Solution:**
```javascript
// WRONG (User OAuth app)
fetch('https://api.zoom.us/v2/users/user@example.com', {
  headers: { 'Authorization': `Bearer ${userToken}` }
});

// CORRECT (User OAuth app)
fetch('https://api.zoom.us/v2/users/me', {
  headers: { 'Authorization': `Bearer ${userToken}` }
});
```

#### Scenario 2: Meeting/Resource Not Found

```json
{
  "code": 300,
  "message": "Meeting not found."
}
```

**Causes:**
- Meeting deleted
- Meeting expired (30 days after last use)
- Invalid meetingId
- Wrong UUID encoding

**Solution for UUID:**
```javascript
// UUID starts with / or contains // → double-encode
const uuid = '/xyzAbC123==';
const encoded = encodeURIComponent(encodeURIComponent(uuid));
fetch(`https://api.zoom.us/v2/meetings/${encoded}`, { headers });
```

### 429 Too Many Requests

```json
{
  "code": 200,
  "message": "You have reached the maximum per-second rate limit for this API."
}
```

**Solution:** Implement exponential backoff

```javascript
async function apiCallWithBackoff(url, options, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const response = await fetch(url, options);

    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After') || Math.pow(2, attempt);
      console.log(`Rate limited. Retrying after ${retryAfter}s`);
      await sleep(retryAfter * 1000);
      continue;
    }

    return response;
  }

  throw new Error('Max retries exceeded');
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

**Check rate limit headers:**
```javascript
const remaining = response.headers.get('X-RateLimit-Remaining');
const type = response.headers.get('X-RateLimit-Type');

console.log(`Rate limit remaining: ${remaining} (${type})`);
```

## Validation Error Responses

### Field Validation Errors

```json
{
  "code": 300,
  "message": "Validation Failed.",
  "errors": [
    {
      "field": "start_time",
      "message": "Invalid field."
    },
    {
      "field": "type",
      "message": "Invalid field."
    }
  ]
}
```

**Solution:**
- Check each field's format in API documentation
- Verify required fields are present
- Ensure data types match (number vs string)

### Common Field Errors

| Field | Error | Cause | Fix |
|-------|-------|-------|-----|
| `start_time` | Invalid field | Wrong format | Use `yyyy-MM-ddTHH:mm:ssZ` |
| `type` | Invalid field | Invalid meeting type | Use 1, 2, 3, or 8 |
| `email` | Invalid field | Invalid email format | Check email format |
| `duration` | Invalid field | Duration too long | Max duration varies by plan |

## Error Response Structure

### Standard Error

```json
{
  "code": 300,
  "message": "Descriptive error message"
}
```

### Validation Error

```json
{
  "code": 300,
  "message": "Validation Failed.",
  "errors": [
    {
      "field": "field_name",
      "message": "Error description"
    }
  ]
}
```

## Error Handling Best Practices

### 1. Parse Error Response

```javascript
async function handleApiResponse(response) {
  if (!response.ok) {
    const error = await response.json();
    
    console.error(`API Error ${response.status}:`, error);
    
    // Check for validation errors
    if (error.errors && Array.isArray(error.errors)) {
      error.errors.forEach(err => {
        console.error(`- Field "${err.field}": ${err.message}`);
      });
    }
    
    throw new Error(`${error.code}: ${error.message}`);
  }
  
  return await response.json();
}
```

### 2. Retry with Exponential Backoff

```javascript
async function retryWithBackoff(fn, maxRetries = 3, baseDelay = 1000) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      const isRetryable = error.status >= 500 || error.status === 429;
      
      if (!isRetryable || attempt === maxRetries) {
        throw error;
      }
      
      const delay = baseDelay * Math.pow(2, attempt - 1);
      const jitter = Math.random() * 1000;  // Add randomness
      
      console.log(`Retry attempt ${attempt} after ${delay + jitter}ms`);
      await sleep(delay + jitter);
    }
  }
}
```

### 3. Log Errors with Context

```javascript
function logApiError(error, context) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    status: error.status,
    code: error.code,
    message: error.message,
    context: {
      endpoint: context.endpoint,
      method: context.method,
      userId: context.userId
    }
  };
  
  console.error('API Error:', JSON.stringify(logEntry, null, 2));
  
  // Send to monitoring service
  // monitoring.track(logEntry);
}
```

### 4. User-Friendly Error Messages

```javascript
function getUserFriendlyError(error) {
  const errorMap = {
    1001: 'User not found. Please check the email address.',
    300: 'Invalid request. Please check your input.',
    201: 'Your session has expired. Please sign in again.',
    4700: 'Permission denied. Please contact your administrator.',
    200: 'Too many requests. Please try again in a few moments.'
  };
  
  return errorMap[error.code] || 'An unexpected error occurred. Please try again.';
}
```

## Troubleshooting Checklist

### Quick Diagnostic Steps

1. **Check HTTP status code** - Indicates error category (auth, validation, server)
2. **Read error message** - Provides specific details
3. **Check Zoom error code** - Maps to specific issue
4. **Verify authentication** - Token valid, scopes present
5. **Check rate limits** - Monitor `X-RateLimit-Remaining` header
6. **Test with Postman** - Isolate code vs API issue
7. **Check Zoom Status** - Visit [status.zoom.us](https://status.zoom.us)

### Common Fixes

| Symptom | Check | Fix |
|---------|-------|-----|
| 401 Unauthorized | Token expiry | Refresh access token |
| 404 User not found | `me` keyword usage | Use `me` for User OAuth |
| 404 Meeting not found | UUID encoding | Double-encode UUIDs starting with `/` |
| 403 Forbidden | Scopes | Add required scopes in app config |
| 429 Rate limit | Request rate | Implement throttling |
| 400 Validation error | Request body | Check field formats in docs |

## Related Documentation

- **[API Architecture](../concepts/api-architecture.md)** - `me` keyword, UUID encoding, time formats
- **[Rate Limiting Strategy](../concepts/rate-limiting-strategy.md)** - Handle 429 errors
- **[Authentication Flows](../concepts/authentication-flows.md)** - Token refresh patterns
- **[Common Issues](common-issues.md)** - Practical troubleshooting

## Resources

- [Error Codes Documentation](https://developers.zoom.us/docs/api/errors/)
- [Zoom Status Page](https://status.zoom.us/)
- [Developer Forum](https://devforum.zoom.us/)
