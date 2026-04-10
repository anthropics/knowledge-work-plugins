# Fastlike Backend Configuration

Backends are origin servers that your Fastly Compute WASM program proxies requests to.

## Backend Syntax

```bash
# Named backend (your WASM references "api" by name)
-backend api=api.example.com:8080

# Catch-all backend (used when name doesn't match)
-backend localhost:8000

# Short form
-b api=api.example.com:8080
```

## Common Patterns

**Single origin:**
```bash
bin/fastlike -wasm app.wasm -backend localhost:3000
```

**Multiple named backends:**
```bash
bin/fastlike -wasm app.wasm \
  -backend api=localhost:3000 \
  -backend static=localhost:4000 \
  -backend auth=localhost:5001
```

**Named + catch-all fallback:**
```bash
bin/fastlike -wasm app.wasm \
  -backend api=api.internal:8080 \
  -backend localhost:8000
```
Requests to backend "api" go to `api.internal:8080`, all others to `localhost:8000`.

**Microservices setup:**
```bash
bin/fastlike -wasm gateway.wasm \
  -backend users=users-service:3001 \
  -backend orders=orders-service:3002 \
  -backend inventory=inventory-service:3003 \
  -backend payments=payments-service:3004
```

## How Backends Work

1. Your WASM calls the Fastly Compute ABI to make a backend request with a name
2. Fastlike looks up the backend by name
3. If found, proxies to that backend's address
4. If not found and a catch-all exists, uses the catch-all
5. If not found and no catch-all, returns 502 Bad Gateway

## Backend Address Format

- `hostname:port` - Standard format
- `localhost:8000` - Local development servers
- `service-name:port` - Docker Compose service names
- `192.168.1.100:8080` - Direct IP addresses

Backends create HTTP reverse proxies. HTTPS is not directly supported for local backends.

## Testing Backends

Start your backend services first, then run fastlike:

```bash
# Terminal 1: Start your backend
cd backend && npm start  # Runs on :3000

# Terminal 2: Start fastlike
bin/fastlike -wasm app.wasm -backend localhost:3000 -v 2
```

Use `-v 2` for verbose logging to see backend requests.
