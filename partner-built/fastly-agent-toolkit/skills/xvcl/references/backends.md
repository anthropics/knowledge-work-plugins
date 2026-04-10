# Backends and Directors Reference

## Backend Declaration

```vcl
backend origin {
  .host = "api.example.com";
  .port = "443";
  .ssl = true;
}
```

## Full Backend Configuration

```vcl
backend my_origin {
  // Host configuration
  .host = "origin.example.com";
  .port = "443";

  // SSL/TLS
  .ssl = true;
  .ssl_cert_hostname = "origin.example.com";
  .ssl_sni_hostname = "origin.example.com";
  .ssl_check_cert = always;

  // Timeouts
  .connect_timeout = 1s;
  .first_byte_timeout = 15s;
  .between_bytes_timeout = 10s;

  // Connection settings
  .max_connections = 200;

  // Health check probe
  .probe = {
    .request = "GET /health HTTP/1.1" "Host: origin.example.com" "Connection: close";
    .expected_response = 200;
    .interval = 5s;
    .timeout = 2s;
    .window = 5;
    .threshold = 3;
    .initial = 3;
  }
}
```

## Backend Properties

| Property                 | Type    | Description                                                          |
| ------------------------ | ------- | -------------------------------------------------------------------- |
| `.host`                  | STRING  | Origin hostname or IP                                                |
| `.port`                  | STRING  | Origin port (default "80")                                           |
| `.ssl`                   | BOOL    | Enable HTTPS to origin                                               |
| `.ssl_cert_hostname`     | STRING  | Hostname to verify origin cert against (must match origin cert SANs) |
| `.ssl_sni_hostname`      | STRING  | SNI hostname sent in TLS handshake (must match origin cert SANs)     |
| `.ssl_check_cert`        | STRING  | Cert validation: `always`, `never`                                   |
| `.connect_timeout`       | RTIME   | Connection timeout                                                   |
| `.first_byte_timeout`    | RTIME   | Time to first byte                                                   |
| `.between_bytes_timeout` | RTIME   | Time between bytes                                                   |
| `.max_connections`       | INTEGER | Max connections                                                      |

## Health Check Probe

```vcl
backend origin {
  .host = "api.example.com";
  .port = "443";
  .ssl = true;

  .probe = {
    // Request to send
    .request = "GET /health HTTP/1.1" "Host: api.example.com" "Connection: close";

    // Alternative: just URL
    .url = "/health";

    // Expected response
    .expected_response = 200;

    // Check frequency
    .interval = 5s;

    // Check timeout
    .timeout = 2s;

    // Window for health calculation
    .window = 5;

    // Successes needed to be healthy
    .threshold = 3;

    // Initial state (healthy checks)
    .initial = 3;
  }
}
```

## Using Backends

```vcl
sub vcl_recv {
  #FASTLY recv

  // Assign backend
  set req.backend = origin;

  // Conditional backend selection
  if (req.url.path ~ "^/api/") {
    set req.backend = api_backend;
  } else if (req.url.path ~ "^/static/") {
    set req.backend = static_backend;
  }

  return (lookup);
}
```

## Backend Health

```vcl
sub vcl_recv {
  #FASTLY recv

  // Check if backend is healthy
  if (backend.origin.healthy) {
    set req.backend = origin;
  } else {
    set req.backend = fallback;
  }

  return (lookup);
}
```

## Directors

Directors distribute requests across multiple backends.

### Round Robin Director

```vcl
director round_robin_dir round_robin {
  { .backend = origin_1; .weight = 1; }
  { .backend = origin_2; .weight = 1; }
  { .backend = origin_3; .weight = 1; }
}

sub vcl_recv {
  #FASTLY recv
  set req.backend = round_robin_dir;
  return (lookup);
}
```

### Random Director

```vcl
director random_dir random {
  { .backend = origin_1; .weight = 3; }
  { .backend = origin_2; .weight = 2; }
  { .backend = origin_3; .weight = 1; }
}
```

### Consistent Hashing Director

Distributes requests based on a hash key (sticky sessions):

```vcl
director chash_dir chash {
  { .backend = origin_1; .id = "origin_1"; }
  { .backend = origin_2; .id = "origin_2"; }
  { .backend = origin_3; .id = "origin_3"; }
}

sub vcl_recv {
  #FASTLY recv

  // Set the hash key for consistent routing
  set req.hash = req.http.Cookie:session_id;
  set req.backend = chash_dir;

  return (lookup);
}
```

### Fallback Director

```vcl
director fallback_dir fallback {
  { .backend = primary; }
  { .backend = secondary; }
  { .backend = tertiary; }
}
```

## Multi-Region Backends (XVCL)

```xvcl
#const REGIONS = [
  ("us_east", "us-east.example.com"),
  ("us_west", "us-west.example.com"),
  ("eu_west", "eu-west.example.com")
]

#for name, host in REGIONS
backend F_{{name}} {
  .host = "{{host}}";
  .port = "443";
  .ssl = true;
  .ssl_cert_hostname = "{{host}}";
  .connect_timeout = 1s;
  .first_byte_timeout = 15s;
  .between_bytes_timeout = 10s;
}
#endfor
```

## Common Patterns

### Primary/Failover

```vcl
backend primary {
  .host = "primary.example.com";
  .port = "443";
  .ssl = true;
  .probe = {
    .url = "/health";
    .interval = 5s;
  }
}

backend secondary {
  .host = "secondary.example.com";
  .port = "443";
  .ssl = true;
  .probe = {
    .url = "/health";
    .interval = 5s;
  }
}

sub vcl_recv {
  #FASTLY recv

  if (backend.primary.healthy) {
    set req.backend = primary;
  } else {
    set req.backend = secondary;
  }

  return (lookup);
}
```

### Route by Path

```vcl
backend api_origin {
  .host = "api.example.com";
  .port = "443";
  .ssl = true;
}

backend web_origin {
  .host = "www.example.com";
  .port = "443";
  .ssl = true;
}

backend static_origin {
  .host = "static.example.com";
  .port = "443";
  .ssl = true;
}

sub vcl_recv {
  #FASTLY recv

  if (req.url.path ~ "^/api/") {
    set req.backend = api_origin;
  } else if (req.url.path ~ "^/(images|css|js)/") {
    set req.backend = static_origin;
  } else {
    set req.backend = web_origin;
  }

  return (lookup);
}
```

### Route by Header

```vcl
sub vcl_recv {
  #FASTLY recv

  // Route by environment header
  if (req.http.X-Environment == "staging") {
    set req.backend = staging_origin;
  } else {
    set req.backend = production_origin;
  }

  return (lookup);
}
```

## Dynamic Backends

Dynamic backends are created at runtime rather than declared in configuration. A health check probe is required for dynamic backends.

```vcl
backend dynamic_origin {
  .host = "dynamic.example.com";
  .port = "443";
  .ssl = true;
  .dynamic = true;
  .probe = {
    .url = "/health";
    .interval = 5s;
    .timeout = 2s;
    .window = 5;
    .threshold = 3;
    .initial = 3;
  }
}
```

Without a probe configured, dynamic backends will fail to work correctly. Always include a `.probe` block when using dynamic backends.

## Backend Variables

| Variable                 | Type    | Scope            | Description           |
| ------------------------ | ------- | ---------------- | --------------------- |
| `req.backend`            | BACKEND | recv, miss, pass | Selected backend      |
| `backend.{name}.healthy` | BOOL    | recv             | Backend health status |
| `beresp.backend.name`    | STRING  | fetch            | Backend name          |
| `beresp.backend.ip`      | IP      | fetch            | Backend IP            |
