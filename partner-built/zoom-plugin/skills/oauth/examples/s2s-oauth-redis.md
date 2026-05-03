# S2S OAuth with Redis Caching (Production Pattern)

Production-ready Server-to-Server OAuth implementation with Redis token caching and auto-refresh middleware.

## Architecture

```
Express App
    ↓
tokenCheck Middleware (automatic token management)
    ↓
Redis Cache (TTL-based expiration)
    ↓
Zoom API Routes (protected)
```

## Complete Implementation

### 1. Dependencies

```bash
npm install express redis axios query-string dotenv
```

### 2. Redis Configuration

```javascript
// configs/redis.js
const redis = require('redis');

const client = redis.createClient({
  url: process.env.REDIS_URL || 'redis://YOUR_REDIS_HOST:6379'
});

client.on('error', (err) => console.error('Redis error:', err));
client.on('connect', () => console.log('Connected to Redis'));

module.exports = client;
```

### 3. Token Utilities

```javascript
// utils/token.js
const axios = require('axios');
const qs = require('query-string');

const { ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET } = process.env;

const getToken = async () => {
  try {
    const response = await axios.post(
      'https://zoom.us/oauth/token',
      qs.stringify({
        grant_type: 'account_credentials',
        account_id: ZOOM_ACCOUNT_ID
      }),
      {
        headers: {
          'Authorization': `Basic ${Buffer.from(
            `${ZOOM_CLIENT_ID}:${ZOOM_CLIENT_SECRET}`
          ).toString('base64')}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );

    return response.data; // { access_token, expires_in, scope }
  } catch (error) {
    throw new Error(`Token request failed: ${error.response?.data?.message || error.message}`);
  }
};

const setToken = async (redis, { access_token, expires_in }) => {
  // Cache with TTL (10 second buffer before actual expiration)
  await redis.setex('access_token', expires_in - 10, access_token);
};

module.exports = { getToken, setToken };
```

### 4. Token Check Middleware

```javascript
// middlewares/tokenCheck.js
const redis = require('../configs/redis');
const { getToken, setToken } = require('../utils/token');

const tokenCheck = async (req, res, next) => {
  let token = await redis.get('access_token');

  // Redis returns null if key doesn't exist
  if (!token) {
    try {
      const { access_token, expires_in, error } = await getToken();

      if (error) {
        return res.status(401).json({
          message: `Authentication failed: ${error.message}`
        });
      }

      // Cache token
      await setToken(redis, { access_token, expires_in });
      token = access_token;
    } catch (err) {
      return res.status(500).json({
        message: 'Token generation failed',
        error: err.message
      });
    }
  }

  // Attach token to request for route handlers
  req.headerConfig = {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };

  next();
};

module.exports = { tokenCheck };
```

### 5. Main Application

```javascript
// index.js
require('dotenv').config();

const express = require('express');
const redis = require('./configs/redis');
const { tokenCheck } = require('./middlewares/tokenCheck');

const app = express();
const PORT = process.env.PORT || 8080;

// Connect to Redis
(async () => {
  await redis.connect();
})();

// Add global middlewares
app.use(express.json());

// Apply tokenCheck to all API routes
app.use('/api/users', tokenCheck, require('./routes/api/users'));
app.use('/api/meetings', tokenCheck, require('./routes/api/meetings'));

const server = app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

// Graceful shutdown
const cleanup = async () => {
  console.log('Shutting down gracefully...');
  await redis.del('access_token'); // Clear cached token
  server.close(() => {
    redis.quit(() => process.exit());
  });
};

process.on('SIGTERM', cleanup);
process.on('SIGINT', cleanup);
```

### 6. Example API Route

```javascript
// routes/api/users.js
const express = require('express');
const axios = require('axios');
const router = express.Router();

const ZOOM_API_BASE = 'https://api.zoom.us/v2';

// List users
router.get('/', async (req, res) => {
  try {
    const response = await axios.get(
      `${ZOOM_API_BASE}/users`,
      req.headerConfig // Token from middleware
    );
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: 'Failed to list users',
      error: error.response?.data || error.message
    });
  }
});

// Get user
router.get('/:userId', async (req, res) => {
  try {
    const response = await axios.get(
      `${ZOOM_API_BASE}/users/${req.params.userId}`,
      req.headerConfig
    );
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: 'Failed to get user',
      error: error.response?.data || error.message
    });
  }
});

module.exports = router;
```

### 7. Environment Variables

```bash
# .env
ZOOM_ACCOUNT_ID=your_account_id
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
REDIS_URL=redis://YOUR_REDIS_HOST:6379
PORT=8080
```

## How It Works

1. **Request arrives** at protected route (e.g., GET /api/users)
2. **tokenCheck middleware** runs:
   - Checks Redis for cached token
   - If missing: Requests new token from Zoom
   - Caches token with TTL (expires_in - 10 seconds)
3. **Token attached** to `req.headerConfig`
4. **Route handler** makes API request with token
5. **Token auto-refreshes** when Redis TTL expires

## Benefits

✅ **Automatic token management** - No manual refresh logic
✅ **Single token for all requests** - Account-wide access
✅ **TTL-based expiration** - Redis handles cleanup
✅ **10-second buffer** - Prevents race conditions
✅ **Graceful shutdown** - Clears token on exit

## Testing

```bash
# Start Redis
docker run -d -p 6379:6379 redis

# Start app
npm start

# Test endpoints
API_BASE_URL="http://YOUR_API_HOST:8080"
curl "$API_BASE_URL/api/users"
```

## Docker Deployment

```dockerfile
# Dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "index.js"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ZOOM_ACCOUNT_ID=${ZOOM_ACCOUNT_ID}
      - ZOOM_CLIENT_ID=${ZOOM_CLIENT_ID}
      - ZOOM_CLIENT_SECRET=${ZOOM_CLIENT_SECRET}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
```

## Related

- **S2S OAuth flow** → [../concepts/oauth-flows.md#server-to-server-s2s-oauth](../concepts/oauth-flows.md#server-to-server-s2s-oauth)
- **Token lifecycle** → [../concepts/token-lifecycle.md](../concepts/token-lifecycle.md)
