# User and Meeting Creation Chain

Create a user account and immediately schedule a meeting for that user.

## Overview

A common provisioning pattern: create a new Zoom user via REST API, wait for activation, then create a meeting for that user. This requires understanding user states and proper sequencing.

## Skills Needed

| Order | Skill | Purpose |
|-------|-------|---------|
| 1 | **zoom-rest-api** | Create user account |
| 2 | **zoom-rest-api** | Create meeting for user |
| (Optional) | **webhooks** | Receive user activation event |

## Skill Chaining Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER + MEETING CREATION FLOW                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Create User (zoom-rest-api)                                          │
│    └── POST /users                                                      │
│    └── action: "create" | "autoCreate" | "custCreate" | "ssoCreate"     │
│    └── Returns: user_id, status                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. Wait for User Activation                                             │
│    └── Option A: Poll GET /users/{userId} until status = "active"       │
│    └── Option B: Listen for user.activated webhook                      │
│    └── Option C: Use autoCreate (auto-activates)                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. Create Meeting (zoom-rest-api)                                       │
│    └── POST /users/{userId}/meetings                                    │
│    └── Returns: meeting_id, join_url, start_url                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Zoom app with Server-to-Server OAuth (recommended) or OAuth
- Scopes: `user:write:admin`, `meeting:write:admin`
- Admin privileges on the Zoom account
- **See [Authorization Patterns](../references/authorization-patterns.md)** for RBAC and permission validation middleware

## User Action Types

| Action | Description | Activation | Best For |
|--------|-------------|------------|----------|
| `create` | Sends activation email to user | User clicks email link | Standard provisioning |
| `autoCreate` | Creates pre-activated user | Immediate | Automated systems |
| `custCreate` | Creates user without email | Manual activation | Custom workflows |
| `ssoCreate` | Creates SSO user | SSO login | Enterprise SSO |

## Step 1: Create User

### Option A: Standard Creation (with email activation)

```javascript
const axios = require('axios');

/**
 * Create a new Zoom user
 * @param {Object} userInfo - User information
 * @param {string} accessToken - Valid OAuth access token
 * @returns {Promise<Object>} Created user details
 */
async function createUser(userInfo, accessToken) {
  try {
    const response = await axios.post(
      'https://api.zoom.us/v2/users',
      {
        action: 'create',  // Sends activation email
        user_info: {
          email: userInfo.email,
          type: userInfo.type || 1,  // 1=Basic, 2=Licensed
          first_name: userInfo.firstName,
          last_name: userInfo.lastName,
          password: userInfo.password  // Optional
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return {
      id: response.data.id,
      email: response.data.email,
      first_name: response.data.first_name,
      last_name: response.data.last_name,
      type: response.data.type,
      status: 'pending'  // User needs to activate via email
    };
  } catch (error) {
    if (error.response?.status === 409) {
      throw new Error(`User ${userInfo.email} already exists`);
    }
    if (error.response?.status === 400) {
      throw new Error(`Invalid user data: ${error.response.data.message}`);
    }
    throw error;
  }
}
```

### Option B: Auto-Create (Immediate activation)

```javascript
/**
 * Create a pre-activated Zoom user (no email required)
 * Recommended for automated provisioning
 */
async function createUserAutoActivate(userInfo, accessToken) {
  try {
    const response = await axios.post(
      'https://api.zoom.us/v2/users',
      {
        action: 'autoCreate',  // User is immediately active
        user_info: {
          email: userInfo.email,
          type: userInfo.type || 2,  // 2=Licensed (required for autoCreate)
          first_name: userInfo.firstName,
          last_name: userInfo.lastName,
          password: userInfo.password || generateSecurePassword()
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return {
      id: response.data.id,
      email: response.data.email,
      first_name: response.data.first_name,
      last_name: response.data.last_name,
      type: response.data.type,
      status: 'active'  // Ready immediately
    };
  } catch (error) {
    handleUserCreationError(error, userInfo.email);
  }
}

function generateSecurePassword() {
  const crypto = require('crypto');
  return crypto.randomBytes(16).toString('base64') + '!Aa1';
}
```

## Step 2: Wait for User Activation

### Option A: Polling (Simple)

```javascript
/**
 * Wait for user to become active by polling
 * @param {string} userId - User ID to check
 * @param {string} accessToken - OAuth token
 * @param {number} maxWaitMs - Maximum wait time (default 5 minutes)
 * @param {number} pollIntervalMs - Poll interval (default 5 seconds)
 */
async function waitForUserActivation(userId, accessToken, maxWaitMs = 300000, pollIntervalMs = 5000) {
  const startTime = Date.now();
  
  while (Date.now() - startTime < maxWaitMs) {
    const user = await getUser(userId, accessToken);
    
    if (user.status === 'active') {
      console.log(`User ${userId} is now active`);
      return user;
    }
    
    console.log(`User ${userId} status: ${user.status}, waiting...`);
    await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
  }
  
  throw new Error(`User ${userId} did not activate within ${maxWaitMs}ms`);
}

async function getUser(userId, accessToken) {
  const response = await axios.get(
    `https://api.zoom.us/v2/users/${userId}`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  return response.data;
}
```

### Option B: Webhook (Production recommended)

```javascript
const express = require('express');
const app = express();
app.use(express.json());

// Store pending user creations
const pendingUsers = new Map();

/**
 * Create user and wait for webhook activation
 */
async function createUserAndWait(userInfo, accessToken) {
  // Create user
  const user = await createUser(userInfo, accessToken);
  
  // Set up promise that resolves when webhook fires
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      pendingUsers.delete(user.id);
      reject(new Error(`User ${user.id} activation timeout`));
    }, 300000); // 5 minute timeout
    
    pendingUsers.set(user.id, { resolve, reject, timeout, user });
  });
}

// Webhook handler for user activation
app.post('/webhooks/zoom', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'user.activated') {
    const userId = payload.object.id;
    const pending = pendingUsers.get(userId);
    
    if (pending) {
      clearTimeout(pending.timeout);
      pendingUsers.delete(userId);
      pending.resolve({ ...pending.user, status: 'active' });
    }
  }
  
  res.status(200).send();
});
```

## Step 3: Create Meeting for User

```javascript
/**
 * Create a meeting for a specific user
 * @param {string} userId - User ID or email
 * @param {Object} meetingInfo - Meeting details
 * @param {string} accessToken - OAuth token
 */
async function createMeetingForUser(userId, meetingInfo, accessToken) {
  try {
    const response = await axios.post(
      `https://api.zoom.us/v2/users/${userId}/meetings`,
      {
        topic: meetingInfo.topic,
        type: meetingInfo.type || 2,  // 2 = Scheduled
        start_time: meetingInfo.startTime,
        duration: meetingInfo.duration || 60,
        timezone: meetingInfo.timezone || 'UTC',
        agenda: meetingInfo.agenda,
        settings: {
          host_video: true,
          participant_video: true,
          join_before_host: false,
          mute_upon_entry: true,
          waiting_room: true,
          ...meetingInfo.settings
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return {
      id: response.data.id,
      topic: response.data.topic,
      start_time: response.data.start_time,
      join_url: response.data.join_url,
      start_url: response.data.start_url,
      password: response.data.password,
      host_id: response.data.host_id,
      host_email: response.data.host_email
    };
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error(`User ${userId} not found or not active`);
    }
    if (error.response?.status === 429) {
      throw new Error('Rate limit exceeded. Try again later.');
    }
    throw error;
  }
}
```

## Complete Chained Operation

```javascript
/**
 * Complete example: Create user and schedule their first meeting
 * 
 * This demonstrates skill chaining:
 * 1. zoom-rest-api (users) - Create user
 * 2. zoom-rest-api (meetings) - Create meeting
 */

async function provisionUserWithMeeting(userInfo, meetingInfo) {
  console.log('Starting user provisioning...');
  
  // Get access token
  const accessToken = await getAccessToken();
  
  try {
    // Step 1: Create user (autoCreate for immediate activation)
    console.log(`Creating user: ${userInfo.email}`);
    const user = await createUserAutoActivate({
      email: userInfo.email,
      firstName: userInfo.firstName,
      lastName: userInfo.lastName,
      type: 2  // Licensed user
    }, accessToken);
    
    console.log(`User created: ${user.id} (status: ${user.status})`);
    
    // Step 2: Verify user is active (should be immediate with autoCreate)
    if (user.status !== 'active') {
      console.log('Waiting for user activation...');
      await waitForUserActivation(user.id, accessToken);
    }
    
    // Step 3: Create meeting for the new user
    console.log(`Creating meeting for user: ${user.id}`);
    const meeting = await createMeetingForUser(user.id, {
      topic: meetingInfo.topic || `${user.first_name}'s Meeting`,
      type: 2,
      startTime: meetingInfo.startTime || new Date(Date.now() + 3600000).toISOString(),
      duration: meetingInfo.duration || 60,
      timezone: meetingInfo.timezone || 'America/Los_Angeles'
    }, accessToken);
    
    console.log(`Meeting created: ${meeting.id}`);
    
    // Return complete provisioning result
    return {
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: `${user.first_name} ${user.last_name}`
      },
      meeting: {
        id: meeting.id,
        topic: meeting.topic,
        join_url: meeting.join_url,
        start_url: meeting.start_url,
        start_time: meeting.start_time
      }
    };
    
  } catch (error) {
    console.error('Provisioning failed:', error.message);
    
    // Cleanup: If user was created but meeting failed, optionally delete user
    // await deleteUser(user.id, accessToken);
    
    return {
      success: false,
      error: error.message
    };
  }
}

// Helper: Get access token (Server-to-Server OAuth)
async function getAccessToken() {
  const credentials = Buffer.from(
    `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
  ).toString('base64');
  
  const response = await axios.post(
    `https://zoom.us/oauth/token?grant_type=account_credentials&account_id=${process.env.ZOOM_ACCOUNT_ID}`,
    null,
    { headers: { 'Authorization': `Basic ${credentials}` } }
  );
  
  return response.data.access_token;
}

// Usage
const result = await provisionUserWithMeeting(
  {
    email: 'newuser@example.com',
    firstName: 'John',
    lastName: 'Doe'
  },
  {
    topic: 'Onboarding Meeting',
    startTime: '2024-02-01T10:00:00Z',
    duration: 30
  }
);

console.log(result);
// {
//   success: true,
//   user: { id: 'abc123', email: 'newuser@example.com', name: 'John Doe' },
//   meeting: { id: '123456789', topic: 'Onboarding Meeting', join_url: '...', ... }
// }
```

## Error Handling

### Error Recovery Pattern

```javascript
/**
 * Robust provisioning with rollback capability
 */
async function provisionUserWithMeetingSafe(userInfo, meetingInfo) {
  const accessToken = await getAccessToken();
  let createdUser = null;
  
  try {
    // Step 1: Create user
    createdUser = await createUserAutoActivate(userInfo, accessToken);
    
    // Step 2: Create meeting
    const meeting = await createMeetingForUser(createdUser.id, meetingInfo, accessToken);
    
    return { success: true, user: createdUser, meeting };
    
  } catch (error) {
    // Rollback: Delete user if meeting creation failed
    if (createdUser && error.message.includes('meeting')) {
      console.log(`Rolling back: deleting user ${createdUser.id}`);
      try {
        await deleteUser(createdUser.id, accessToken);
      } catch (deleteError) {
        console.error('Rollback failed:', deleteError.message);
      }
    }
    
    throw error;
  }
}

async function deleteUser(userId, accessToken) {
  await axios.delete(
    `https://api.zoom.us/v2/users/${userId}?action=delete`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 409 Conflict | User email already exists | Use existing user or different email |
| 400 Bad Request | Invalid user data | Check email format, required fields |
| 404 Not Found | User not active/found | Wait for activation or verify user ID |
| 429 Rate Limit | Too many requests | Implement backoff, batch operations |
| 201 but pending | User needs to activate | Use autoCreate or wait for activation |

## User Types Reference

| Type | Value | Description | Can Host? |
|------|-------|-------------|-----------|
| Basic | 1 | Free user | Limited |
| Licensed | 2 | Paid license | Yes |
| On-prem | 3 | On-premise deployment | Yes |
| None | 99 | No license | No |

## Best Practices

1. **Use autoCreate for automation** - Avoids waiting for email activation
2. **Implement rollback logic** - Clean up if later steps fail
3. **Cache access tokens** - Tokens are valid for 1 hour
4. **Handle rate limits** - Implement exponential backoff
5. **Validate input early** - Check email format before API calls
6. **Log all operations** - Aids debugging and audit

## Related Use Cases

- **[Authorization Patterns](../references/authorization-patterns.md)** - RBAC, permission validation, and scope checking for multi-step workflows
- **[Meeting Automation](meeting-automation.md)** - More meeting management patterns
- **[Meeting Details with Events](meeting-details-with-events.md)** - Track meeting events
- **[Recording & Transcription](recording-transcription.md)** - Handle recordings

## Resources

- **Users API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Users
- **Meetings API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Meetings
- **User Types**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/userCreate
