# Fastlike Configuration Files

Create JSON configuration files for fastlike's various data stores.

## Dictionary Files (`-dictionary NAME=FILE`)

String key-value pairs for Fastly Edge Dictionaries.

```json
{
  "api_key": "sk-abc123",
  "feature_flag": "enabled",
  "rate_limit": "100"
}
```

All values must be strings.

## KV Store Files (`-kv NAME=FILE`)

Two formats supported:

**Simple strings:**
```json
{
  "user:123": "active",
  "config:theme": "dark"
}
```

**Objects with body and metadata:**
```json
{
  "user:123": {
    "body": "{\"name\": \"Alice\", \"role\": \"admin\"}",
    "metadata": "created=2024-01-01"
  },
  "cache:key": {
    "body": "cached-value"
  }
}
```

Use `-kv name` (no file) for an empty store.

## Config Store Files (`-config-store NAME=FILE`)

String key-value configuration:

```json
{
  "log_level": "debug",
  "max_retries": "3",
  "timeout_ms": "5000"
}
```

## Secret Store Files (`-secret-store NAME=FILE`)

String key-value secrets (same format as config):

```json
{
  "database_url": "postgres://user:pass@host/db",
  "jwt_secret": "your-secret-key",
  "api_token": "token-value"
}
```

## ACL Files (`-acl NAME=FILE`)

Access Control Lists with prefix/action entries:

```json
{
  "entries": [
    {"prefix": "192.168.1.0/24", "action": "ALLOW"},
    {"prefix": "10.0.0.0/8", "action": "ALLOW"},
    {"prefix": "0.0.0.0/1", "action": "BLOCK"},
    {"prefix": "128.0.0.0/1", "action": "BLOCK"}
  ]
}
```

Actions: `ALLOW` or `BLOCK`. Most specific match wins (longest prefix length). On ties, later entries take precedence.

**Important:** CIDR mask must be in range [1, 32] for IPv4 and [1, 128] for IPv6. A `/0` mask is invalid — to match all IPs, use two entries: `0.0.0.0/1` and `128.0.0.0/1`.

## Geolocation File (`-geo FILE`)

IP/CIDR to geo data mapping:

```json
{
  "192.168.1.0/24": {
    "city": "San Francisco",
    "country_code": "US",
    "region": "CA",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "10.0.0.1": {
    "city": "New York",
    "country_code": "US",
    "region": "NY"
  }
}
```

Supports exact IPs and CIDR ranges. Most specific CIDR match wins. Default geo (Austin, TX) returned for unknown IPs.

All available geo fields:

| Field             | JSON key            | Type   |
| ----------------- | ------------------- | ------ |
| AS Name           | `as_name`           | string |
| AS Number         | `as_number`         | int    |
| Area Code         | `area_code`         | int    |
| City              | `city`              | string |
| Connection Speed  | `conn_speed`        | string |
| Connection Type   | `conn_type`         | string |
| Continent         | `continent`         | string |
| Country Code      | `country_code`      | string |
| Country Code (3)  | `country_code3`     | string |
| Country Name      | `country_name`      | string |
| Latitude          | `latitude`          | float  |
| Longitude         | `longitude`         | float  |
| Metro Code        | `metro_code`        | int    |
| Postal Code       | `postal_code`       | string |
| Proxy Description | `proxy_description` | string |
| Proxy Type        | `proxy_type`        | string |
| Region            | `region`            | string |
| UTC Offset        | `utc_offset`        | int    |

## Example: Complete Setup

```bash
# Create config directory
mkdir -p config

# Create files
echo '{"feature_x": "enabled"}' > config/dictionary.json
echo '{"session:abc": "user-data"}' > config/kv.json
echo '{"log_level": "info"}' > config/settings.json
echo '{"api_key": "secret123"}' > config/secrets.json

# Run with all stores
bin/fastlike -wasm app.wasm -backend localhost:8000 \
  -dictionary features=config/dictionary.json \
  -kv sessions=config/kv.json \
  -config-store settings=config/settings.json \
  -secret-store secrets=config/secrets.json
```
