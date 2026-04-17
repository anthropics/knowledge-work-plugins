# OpenAPI / Swagger Specifications

Zoom provides OpenAPI specifications for API client generation and tooling integration.

## Official Specifications

### Zoom API v2 (Current)

| Property | Value |
|----------|-------|
| Format | Swagger 2.0 (JSON) |
| Status | **Deprecated** - Last updated November 2018 |
| Coverage | ~103 endpoints (subset of full API) |
| Download | [openapi.v2.json](https://raw.githubusercontent.com/zoom/api/442998230a148f403c3d1de1fe7aa54937354fa9/openapi.v2.json) |
| Repository | [github.com/zoom/api](https://github.com/zoom/api) |

### Zoom API v1 (Legacy)

| Property | Value |
|----------|-------|
| Format | Swagger 2.0 (JSON) |
| Status | **Deprecated** |
| Coverage | ~93 endpoints |
| Download | [openapi.v2.json](https://raw.githubusercontent.com/zoom/api-v1/5478bfe304a827f97acfed9aa5a0ba840b8d1aa9/openapi.v2.json) |
| Repository | [github.com/zoom/api-v1](https://github.com/zoom/api-v1) |

## Coverage Limitations

The official OpenAPI specs only cover a **small subset** of Zoom's 600+ endpoints:

| Covered | NOT Covered |
|---------|-------------|
| Meetings | Phone API |
| Users | Team Chat API |
| Accounts | Mail API |
| Groups | Calendar API |
| Reports | Rooms API |
| Webinars | Clips API |
| H.323 Devices | Whiteboard API |
| IM Groups | Contact Center API |
| | AI Companion API |
| | 20+ other modern APIs |

## Recommended Alternative: Zoom Rivet

Instead of using the outdated OpenAPI specs, Zoom recommends using **Zoom Rivet** - their official API client library.

### Installation

```bash
npm install @zoom/rivet
```

### Usage

```typescript
import Zoom from '@zoom/rivet';

const zoom = new Zoom({
  accountId: process.env.ZOOM_ACCOUNT_ID,
  clientId: process.env.ZOOM_CLIENT_ID,
  clientSecret: process.env.ZOOM_CLIENT_SECRET,
});

// Create a meeting
const meeting = await zoom.meetings.create({
  userId: 'me',
  body: {
    topic: 'My Meeting',
    type: 2,
    duration: 60,
  },
});

// List users
const users = await zoom.users.list();

// Get recordings
const recordings = await zoom.cloudRecordings.list({
  userId: 'me',
  from: '2024-01-01',
  to: '2024-01-31',
});
```

### Why Rivet Over OpenAPI?

| Aspect | OpenAPI Specs | Zoom Rivet |
|--------|---------------|------------|
| Coverage | ~103 endpoints | Full API |
| Maintenance | Deprecated (2018) | Actively maintained |
| Type Safety | Requires codegen | Built-in TypeScript |
| Auth Handling | Manual | Automatic token management |
| Pagination | Manual | Built-in helpers |
| Rate Limiting | Manual | Built-in retry logic |

## Using OpenAPI Specs Anyway

If you still need the OpenAPI specs (e.g., for custom tooling), here's how to use them:

### Download the Spec

```bash
# Download Zoom API v2 spec
curl -o zoom-api-v2.json \
  https://raw.githubusercontent.com/zoom/api/442998230a148f403c3d1de1fe7aa54937354fa9/openapi.v2.json
```

### Generate TypeScript Client

```bash
# Using openapi-generator
npm install @openapitools/openapi-generator-cli -g

openapi-generator-cli generate \
  -i zoom-api-v2.json \
  -g typescript-fetch \
  -o ./zoom-client
```

### Generate Python Client

```bash
openapi-generator-cli generate \
  -i zoom-api-v2.json \
  -g python \
  -o ./zoom-client-python
```

### Known Issues with Code Generation

The Zoom OpenAPI specs have known issues that may cause errors during code generation:

| Issue | Workaround |
|-------|------------|
| Enum type mismatches | Manually fix integer/string enum definitions |
| Missing required fields | Add required fields to generated models |
| Invalid syntax | Validate and fix JSON before generation |
| Outdated endpoints | Supplement with manual API calls for new endpoints |

## Postman Collection

For interactive API exploration, Zoom provides a Postman collection:

- **Postman Collection**: https://marketplace.zoom.us/docs/api-reference/postman

```bash
# Import to Postman
# 1. Open Postman
# 2. Click Import
# 3. Enter URL: https://www.postman.com/zoom-developer/zoom-developer-api
```

## API Reference Documentation

For the most up-to-date API documentation, use the official reference:

- **REST API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/
- **API Changelog**: https://developers.zoom.us/changelog/

## Resources

- [Zoom Rivet (Official SDK)](https://github.com/zoom/rivet-javascript)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Swagger Editor](https://editor.swagger.io/)
- [Postman Collection](https://marketplace.zoom.us/docs/api-reference/postman)
