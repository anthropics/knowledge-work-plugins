# Zoom GraphQL API (Beta)

Flexible data queries with GraphQL as an alternative to REST.

## Overview

Zoom GraphQL API provides a single endpoint for querying and mutating Zoom data. Unlike REST APIs with fixed endpoints, GraphQL allows you to request exactly the data you need.

**Status**: Beta (requires signup)

## Key URLs

| Resource | URL |
|----------|-----|
| **Playground** | https://nws.zoom.us/graphql/playground |
| **Beta Signup** | https://beta.zoom.us/key/GRAPHQL |
| **Endpoint** | `https://api.zoom.us/graphql` |

## GraphQL vs REST

| Feature | REST API | GraphQL API |
|---------|----------|-------------|
| Endpoints | 600+ endpoints | Single endpoint |
| Data fetching | Fixed data per endpoint | Client specifies exact fields |
| Multiple resources | Multiple requests | Single request |
| Over-fetching | Common | Eliminated |
| Schema | Optional (OpenAPI) | Mandatory, strongly typed |
| Learning curve | Lower | Higher |

## Authentication

Same OAuth 2.0 as REST API:

```javascript
const headers = {
  'Authorization': `Bearer ${accessToken}`,
  'Content-Type': 'application/json'
};
```

- Server-to-Server OAuth supported
- User-authorized OAuth supported
- Access tokens valid for 1 hour

## Available Entities

| Entity | Query | Mutation |
|--------|-------|----------|
| Users | ✅ | ✅ |
| Meetings | ✅ | Partial |
| Webinars | ✅ | Partial |
| Chat Channels | Partial | - |
| Cloud Recordings | ✅ | - |
| Dashboards | ✅ | - |
| Groups | Partial | - |
| Reports | Partial | - |

**Note**: Not all REST endpoints are available in GraphQL yet (beta).

## Query Examples

### List Users

```graphql
query ListUsers {
  users(first: 100) {
    edges {
      node {
        id
        firstName
        lastName
        email
        department
        type
        status
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Get User Details

```graphql
query GetUser($userId: ID!) {
  user(id: $userId) {
    id
    firstName
    lastName
    email
    department
    timezone
    type
    createdAt
    lastLoginTime
  }
}
```

Variables:
```json
{
  "userId": "user_abc123"
}
```

### List Meetings

```graphql
query ListMeetings($userId: ID!) {
  user(id: $userId) {
    meetings(first: 50) {
      edges {
        node {
          id
          topic
          type
          startTime
          duration
          timezone
          joinUrl
        }
      }
    }
  }
}
```

### Get Meeting with Participants

```graphql
query GetMeetingDetails($meetingId: ID!) {
  meeting(id: $meetingId) {
    id
    topic
    type
    startTime
    duration
    host {
      id
      firstName
      lastName
      email
    }
    participants {
      edges {
        node {
          id
          name
          email
          joinTime
          leaveTime
        }
      }
    }
  }
}
```

### Get Recordings

```graphql
query GetRecordings($userId: ID!, $from: DateTime!, $to: DateTime!) {
  user(id: $userId) {
    recordings(from: $from, to: $to, first: 50) {
      edges {
        node {
          id
          topic
          startTime
          duration
          totalSize
          recordingFiles {
            id
            fileType
            fileSize
            downloadUrl
          }
        }
      }
    }
  }
}
```

## Mutation Examples

### Create User

```graphql
mutation CreateUser($input: UserCreateInput!) {
  createUser(input: $input) {
    id
    email
    firstName
    lastName
    type
  }
}
```

Variables:
```json
{
  "input": {
    "action": "CUST_CREATE",
    "userInfo": {
      "email": "newuser@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "type": "BASIC"
    }
  }
}
```

### Update User

```graphql
mutation UpdateUser($userId: ID!, $input: UserUpdateInput!) {
  updateUser(id: $userId, input: $input) {
    id
    firstName
    lastName
    department
  }
}
```

Variables:
```json
{
  "userId": "user_abc123",
  "input": {
    "firstName": "Jonathan",
    "department": "Engineering"
  }
}
```

## Making Requests

### JavaScript/Node.js

```javascript
async function graphqlQuery(query, variables = {}) {
  const response = await fetch('https://api.zoom.us/graphql', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: query,
      variables: variables
    })
  });
  
  const result = await response.json();
  
  if (result.errors) {
    throw new Error(result.errors[0].message);
  }
  
  return result.data;
}

// Usage
const users = await graphqlQuery(`
  query {
    users(first: 10) {
      edges {
        node {
          id
          email
          firstName
          lastName
        }
      }
    }
  }
`);

console.log(users.users.edges);
```

### Python

```python
import requests

def graphql_query(query, variables=None):
    response = requests.post(
        'https://api.zoom.us/graphql',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={
            'query': query,
            'variables': variables or {}
        }
    )
    
    result = response.json()
    
    if 'errors' in result:
        raise Exception(result['errors'][0]['message'])
    
    return result['data']

# Usage
users = graphql_query('''
    query {
        users(first: 10) {
            edges {
                node {
                    id
                    email
                }
            }
        }
    }
''')
```

### cURL

```bash
curl -X POST https://api.zoom.us/graphql \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { users(first: 10) { edges { node { id email } } } }"
  }'
```

## Pagination

GraphQL uses cursor-based pagination:

```graphql
query PaginatedUsers($cursor: String) {
  users(first: 100, after: $cursor) {
    edges {
      node {
        id
        email
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Fetching all pages:

```javascript
async function fetchAllUsers() {
  let allUsers = [];
  let cursor = null;
  let hasNextPage = true;
  
  while (hasNextPage) {
    const result = await graphqlQuery(
      `query($cursor: String) {
        users(first: 100, after: $cursor) {
          edges {
            node { id email firstName lastName }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }`,
      { cursor }
    );
    
    allUsers.push(...result.users.edges.map(e => e.node));
    hasNextPage = result.users.pageInfo.hasNextPage;
    cursor = result.users.pageInfo.endCursor;
  }
  
  return allUsers;
}
```

## Error Handling

GraphQL always returns HTTP 200. Errors are in the response body:

```json
{
  "data": null,
  "errors": [
    {
      "message": "User not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND"
      }
    }
  ]
}
```

Handle errors:

```javascript
async function safeQuery(query, variables) {
  const response = await fetch('https://api.zoom.us/graphql', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query, variables })
  });
  
  const result = await response.json();
  
  if (result.errors && result.errors.length > 0) {
    const error = result.errors[0];
    console.error(`GraphQL Error: ${error.message}`);
    console.error(`Code: ${error.extensions?.code}`);
    throw new Error(error.message);
  }
  
  return result.data;
}
```

## When to Use GraphQL vs REST

### Use GraphQL When:
- Fetching specific fields from complex nested data
- Making multiple related queries in one request
- Building mobile apps where bandwidth matters
- Working with interconnected user, meeting, webinar data
- Prototyping and exploring the API

### Use REST When:
- Need access to all 600+ endpoints (GraphQL coverage incomplete)
- Building simple CRUD applications
- Require HTTP caching
- Team is unfamiliar with GraphQL
- Production stability is critical (GraphQL is beta)

## Playground

The GraphQL Playground at https://nws.zoom.us/graphql/playground provides:
- Interactive query editor
- Auto-complete and syntax highlighting
- Query history
- Embedded documentation
- Schema explorer

**Note**: Requires beta access.

## Limitations (Beta)

| Limitation | Notes |
|------------|-------|
| Coverage | Not all REST endpoints available |
| Stability | Beta - features may change |
| Access | Requires explicit beta signup |
| Documentation | Less comprehensive than REST |

## Resources

- **Playground**: https://nws.zoom.us/graphql/playground
- **Beta Signup**: https://beta.zoom.us/key/GRAPHQL
- **Postman Collection**: https://www.postman.com/zoom-developer/zoom-public-workspace/collection/2ub5ygf/zoom-graphql-collection-beta
- **Blog Post**: https://dev.to/zoom/the-zoom-graphql-api-playground-your-new-favorite-development-tool-59n5
