# VCL Subroutines Reference

## Request Lifecycle

| Step | Subroutine    | Trigger                  | Next Steps                                                  |
| ---- | ------------- | ------------------------ | ----------------------------------------------------------- |
| 1    | `vcl_recv`    | Client request received  | `lookup` → vcl_hash, `pass` → vcl_hash, `error` → vcl_error |
| 2    | `vcl_hash`    | Generate cache key       | `hit` → vcl_hit, `miss` → vcl_miss                          |
| 3a   | `vcl_hit`     | Cache hit                | → vcl_deliver                                               |
| 3b   | `vcl_miss`    | Cache miss               | → fetch origin → vcl_fetch                                  |
| 4    | `vcl_fetch`   | Origin response received | → vcl_deliver                                               |
| 5    | `vcl_error`   | Error triggered          | → vcl_deliver                                               |
| 6    | `vcl_deliver` | Response ready           | → vcl_log                                                   |
| 7    | `vcl_log`     | Response sent            | → End                                                       |

**Flow summary:** Request → vcl_recv → vcl_hash → (vcl_hit OR vcl_miss → vcl_fetch) → vcl_deliver → vcl_log → Response. Any subroutine can call `error` to jump to vcl_error.

## Lifecycle Subroutines

### vcl_recv

Called when a request is received. Decide backend, caching behavior.

```vcl
sub vcl_recv {
  #FASTLY recv

  // Route requests
  if (req.url.path ~ "^/api/") {
    set req.backend = api_backend;
  } else {
    set req.backend = default_backend;
  }

  // Force cache bypass for authenticated requests
  if (req.http.Authorization) {
    return (pass);
  }

  return (lookup);
}
```

**Return actions:**
- `lookup` - Check cache
- `pass` - Bypass cache, fetch from origin
- `error` - Trigger vcl_error

### vcl_hash

Called to compute the cache key. Modify `req.hash` to customize.

```vcl
sub vcl_hash {
  #FASTLY hash

  // Add custom elements to cache key
  set req.hash += req.http.Host;
  set req.hash += req.url.path;

  // Vary by device type
  if (req.http.User-Agent ~ "Mobile") {
    set req.hash += "mobile";
  }
}
```

### vcl_hit

Called when a cached object is found.

```vcl
sub vcl_hit {
  #FASTLY hit

  // Return stale if origin is down
  if (obj.grace > 0s) {
    return (deliver);
  }
}
```

**Return actions:**
- `deliver` - Serve cached response
- `pass` - Revalidate with origin

### vcl_miss

Called when no cached object is found.

```vcl
sub vcl_miss {
  #FASTLY miss

  // Modify backend request
  set bereq.http.X-Cache-Status = "MISS";
}
```

**Return actions:**
- `fetch` - Fetch from origin
- `pass` - Fetch without caching
- `error` - Trigger error

### vcl_pass

Called when caching is bypassed.

```vcl
sub vcl_pass {
  #FASTLY pass

  set bereq.http.X-Cache-Status = "PASS";
}
```

### vcl_fetch

Called after receiving origin response. Set caching parameters.

```vcl
sub vcl_fetch {
  #FASTLY fetch

  // Set cache TTL
  if (beresp.status == 200) {
    set beresp.ttl = 1h;
    set beresp.grace = 6h;
  }

  // Don't cache errors
  if (beresp.status >= 500) {
    set beresp.ttl = 0s;
    return (pass);
  }

  // Don't cache if origin says no
  if (beresp.http.Cache-Control ~ "no-store") {
    return (pass);
  }

  return (deliver);
}
```

**Return actions:**
- `deliver` - Cache and deliver
- `pass` - Deliver without caching
- `error` - Trigger error

### vcl_deliver

Called before sending response to client.

```vcl
sub vcl_deliver {
  #FASTLY deliver

  // Add cache status header
  if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }

  // Remove internal headers
  unset resp.http.X-Internal-Debug;

  return (deliver);
}
```

**Return actions:**
- `deliver` - Send response to client

### vcl_error

Called when an error occurs or is triggered.

```vcl
sub vcl_error {
  #FASTLY error

  // Handle custom redirects
  if (obj.status == 801) {
    set obj.status = 301;
    set obj.http.Location = "https://" + req.http.Host + req.url;
    return (deliver);
  }

  // Custom error page
  if (obj.status == 503) {
    synthetic {html"
      <!DOCTYPE html>
      <html>
      <head><title>Service Unavailable</title></head>
      <body><h1>Please try again later</h1></body>
      </html>
    "html};
    return (deliver);
  }

  return (deliver);
}
```

**Return actions:**
- `deliver` - Send error response

### vcl_log

Called after response is delivered. For logging only.

```vcl
sub vcl_log {
  #FASTLY log

  log "request_time=" + time.elapsed.msec;
  log "status=" + resp.status;
  log "url=" + req.url;
}
```

## Custom Subroutines

### Basic Subroutine

```vcl
sub security_checks {
  // Block suspicious user agents
  if (req.http.User-Agent ~ "(?i)(bot|crawler|spider)") {
    if (req.http.User-Agent !~ "(?i)(googlebot|bingbot)") {
      error 403 "Forbidden";
    }
  }

  // Block requests without host header
  if (!req.http.Host) {
    error 400 "Bad Request";
  }
}

sub vcl_recv {
  #FASTLY recv
  call security_checks;
  return (lookup);
}
```

### Subroutine with Return Value

```vcl
sub is_authenticated BOOL {
  if (req.http.Authorization ~ "^Bearer ") {
    return true;
  }
  return false;
}

sub vcl_recv {
  #FASTLY recv

  declare local var.authed BOOL;
  set var.authed = is_authenticated();

  if (!var.authed && req.url.path ~ "^/admin/") {
    error 401 "Unauthorized";
  }

  return (lookup);
}
```

### Subroutine with Parameters (XVCL)

```xvcl
#def validate_origin(expected_host STRING) -> BOOL
  if (beresp.http.X-Origin-Host != expected_host) {
    return false;
  }
  return true;
#enddef

sub vcl_fetch {
  #FASTLY fetch

  declare local var.valid BOOL;
  set var.valid = validate_origin("api.example.com");

  if (!var.valid) {
    return (error);
  }

  return (deliver);
}
```

## Subroutine Scope Restrictions

Different subroutines have access to different variables:

| Variable Prefix | recv  | hash  |  hit  | miss  | pass  | fetch | deliver | error |  log  |
| --------------- | :---: | :---: | :---: | :---: | :---: | :---: | :-----: | :---: | :---: |
| `req.*`         |   ✓   |   ✓   |   ✓   |   ✓   |   ✓   |   ✓   |    ✓    |   ✓   |   ✓   |
| `bereq.*`       |   -   |   -   |   -   |   ✓   |   ✓   |   ✓   |    -    |   -   |   -   |
| `beresp.*`      |   -   |   -   |   -   |   -   |   -   |   ✓   |    -    |   -   |   -   |
| `obj.*`         |   -   |   -   |   ✓   |   -   |   -   |   -   |    ✓    |   ✓   |   -   |
| `resp.*`        |   -   |   -   |   -   |   -   |   -   |   -   |    ✓    |   -   |   ✓   |
| `client.*`      |   ✓   |   ✓   |   ✓   |   ✓   |   ✓   |   ✓   |    ✓    |   ✓   |   ✓   |

## Common Patterns

### Conditional Backend Selection

```vcl
sub select_backend {
  if (req.http.X-Region == "us") {
    set req.backend = us_backend;
  } else if (req.http.X-Region == "eu") {
    set req.backend = eu_backend;
  } else {
    set req.backend = default_backend;
  }
}

sub vcl_recv {
  #FASTLY recv
  call select_backend;
  return (lookup);
}

sub vcl_miss {
  #FASTLY miss
  call select_backend;
}

sub vcl_pass {
  #FASTLY pass
  call select_backend;
}
```

### Request/Response Logging

```vcl
sub log_request {
  log "req_method=" + req.method;
  log "req_url=" + req.url;
  log "req_host=" + req.http.Host;
  log "client_ip=" + client.ip;
}

sub log_response {
  log "resp_status=" + resp.status;
  log "resp_content_type=" + resp.http.Content-Type;
}

sub vcl_recv {
  #FASTLY recv
  call log_request;
  return (lookup);
}

sub vcl_log {
  #FASTLY log
  call log_response;
}
```
