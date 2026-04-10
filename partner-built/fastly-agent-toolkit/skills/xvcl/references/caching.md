# Caching Reference

## Default Behavior (No VCL Needed)

Fastly VCL services respect origin HTTP caching headers by default:
- `Cache-Control: max-age=N` and `s-maxage=N` set the cache TTL
- `Expires` headers are honored when `Cache-Control` is absent
- `Vary` headers create separate cache entries per header value
- `Cache-Control: private`, `no-store`, or `no-cache` prevent caching

If the origin already sends appropriate caching headers, you do not need any VCL to enable caching. Only use the VCL patterns below when you need to override or customize the origin's caching behavior.

## Cache Control Basics

### TTL (Time To Live)

```vcl
sub vcl_fetch {
  #FASTLY fetch

  // Set TTL
  set beresp.ttl = 1h;

  // Conditional TTL
  if (beresp.status == 200) {
    set beresp.ttl = 24h;
  } else if (beresp.status == 404) {
    set beresp.ttl = 5m;
  } else {
    set beresp.ttl = 0s;  // don't cache
  }
}
```

### Grace Period

Serve stale content while revalidating:

```vcl
sub vcl_fetch {
  #FASTLY fetch

  set beresp.ttl = 1h;
  set beresp.grace = 6h;  // serve stale for up to 6 hours if origin is down
}
```

### Stale-While-Revalidate

```vcl
sub vcl_fetch {
  #FASTLY fetch

  set beresp.ttl = 1h;
  set beresp.stale_while_revalidate = 60s;  // serve stale for 60s while fetching fresh
}
```

## Cache Key

### Default Cache Key

By default, the cache key includes:
- URL path
- Query string
- Host header

### Customizing Cache Key

```vcl
sub vcl_hash {
  #FASTLY hash

  // Add to cache key
  set req.hash += req.http.Host;
  set req.hash += req.url.path;

  // Vary by device type
  if (req.http.User-Agent ~ "Mobile") {
    set req.hash += "mobile";
  } else {
    set req.hash += "desktop";
  }

  // Vary by cookie value
  if (req.http.Cookie:user_type) {
    set req.hash += req.http.Cookie:user_type;
  }
}
```

### Ignoring Query Parameters

```vcl
sub vcl_recv {
  #FASTLY recv

  // Sort query parameters for consistent caching
  set req.url = querystring.sort(req.url);

  // Remove tracking parameters
  set req.url = querystring.filter(req.url, "utm_");
  set req.url = querystring.filter(req.url, "fbclid");
  set req.url = querystring.filter(req.url, "gclid");
}
```

### Removing All Query Parameters

```vcl
sub vcl_recv {
  #FASTLY recv

  // For static assets, ignore all query params
  if (req.url.path ~ "\.(css|js|jpg|png|gif|ico|woff2?)$") {
    set req.url = req.url.path;
  }
}
```

## Cacheability

### Force Caching

```vcl
sub vcl_fetch {
  #FASTLY fetch

  // Override origin cache headers
  if (req.url.path ~ "^/api/public/") {
    set beresp.ttl = 5m;
    set beresp.http.Cache-Control = "public, max-age=300";
  }
}
```

### Prevent Caching

```vcl
sub vcl_fetch {
  #FASTLY fetch

  // Don't cache errors
  if (beresp.status >= 400) {
    set beresp.ttl = 0s;
    set beresp.cacheable = false;
    return (pass);
  }

  // Don't cache personalized responses
  if (beresp.http.Set-Cookie) {
    set beresp.ttl = 0s;
    return (pass);
  }
}
```

### Bypass Cache Entirely

```vcl
sub vcl_recv {
  #FASTLY recv

  // Bypass cache for authenticated requests
  if (req.http.Authorization) {
    return (pass);
  }

  // Bypass cache for POST/PUT/DELETE
  if (req.method != "GET" && req.method != "HEAD") {
    return (pass);
  }

  return (lookup);
}
```

## Cache Status

### Track Cache Status

```vcl
sub vcl_deliver {
  #FASTLY deliver

  if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
    set resp.http.X-Cache-Hits = obj.hits;
  } else {
    set resp.http.X-Cache = "MISS";
  }

  // Show TTL info
  set resp.http.X-Cache-TTL = obj.ttl;
  set resp.http.X-Cache-Grace = obj.grace;
}
```

## Vary Header

Control cache variations:

```vcl
sub vcl_fetch {
  #FASTLY fetch

  // Ensure proper Vary header for compression
  if (!beresp.http.Vary) {
    set beresp.http.Vary = "Accept-Encoding";
  } else if (beresp.http.Vary !~ "Accept-Encoding") {
    set beresp.http.Vary = beresp.http.Vary + ", Accept-Encoding";
  }
}

sub vcl_deliver {
  #FASTLY deliver

  // Add Vary for device type
  if (resp.http.Vary) {
    set resp.http.Vary = resp.http.Vary + ", User-Agent";
  } else {
    set resp.http.Vary = "User-Agent";
  }
}
```

## Common Patterns

### Static Asset Caching

```vcl
sub vcl_recv {
  #FASTLY recv

  // Ignore cookies for static assets
  if (req.url.path ~ "\.(css|js|jpg|jpeg|png|gif|ico|svg|woff2?|ttf|eot)$") {
    unset req.http.Cookie;
  }

  return (lookup);
}

sub vcl_fetch {
  #FASTLY fetch

  // Long TTL for static assets
  if (req.url.path ~ "\.(css|js|jpg|jpeg|png|gif|ico|svg|woff2?|ttf|eot)$") {
    set beresp.ttl = 30d;
    set beresp.grace = 1d;
    set beresp.http.Cache-Control = "public, max-age=2592000, immutable";
    unset beresp.http.Set-Cookie;
  }
}
```

### API Caching

```vcl
sub vcl_recv {
  #FASTLY recv

  // Only cache GET requests to public endpoints
  if (req.url.path ~ "^/api/public/" && req.method == "GET") {
    return (lookup);
  }

  // Don't cache authenticated API calls
  if (req.url.path ~ "^/api/") {
    return (pass);
  }

  return (lookup);
}

sub vcl_fetch {
  #FASTLY fetch

  // Short TTL for API responses
  if (req.url.path ~ "^/api/public/") {
    set beresp.ttl = 1m;
    set beresp.grace = 5m;
  }
}
```

### Conditional Caching by Content-Type

```vcl
sub vcl_fetch {
  #FASTLY fetch

  if (beresp.http.Content-Type ~ "text/html") {
    set beresp.ttl = 5m;
  } else if (beresp.http.Content-Type ~ "application/json") {
    set beresp.ttl = 1m;
  } else if (beresp.http.Content-Type ~ "image/") {
    set beresp.ttl = 7d;
  }
}
```

### Cache Purge Marker

```vcl
sub vcl_fetch {
  #FASTLY fetch

  // Add surrogate key for targeted purging
  if (req.url.path ~ "^/products/([0-9]+)") {
    set beresp.http.Surrogate-Key = "product-" + re.group.1;
  }

  // Add global key
  set beresp.http.Surrogate-Key = beresp.http.Surrogate-Key + " all";
}
```

## Cache Variables

| Variable           | Type    | Scope        | Description   |
| ------------------ | ------- | ------------ | ------------- |
| `beresp.ttl`       | RTIME   | fetch        | Cache TTL     |
| `beresp.grace`     | RTIME   | fetch        | Grace period  |
| `beresp.cacheable` | BOOL    | fetch        | Is cacheable  |
| `obj.ttl`          | RTIME   | hit, deliver | Remaining TTL |
| `obj.grace`        | RTIME   | hit, deliver | Grace period  |
| `obj.hits`         | INTEGER | deliver      | Hit count     |
| `req.hash`         | STRING  | hash         | Cache key     |

## Cache Control Header Reference

| Directive                  | Meaning                      |
| -------------------------- | ---------------------------- |
| `public`                   | Can be cached by any cache   |
| `private`                  | Only browser can cache       |
| `no-cache`                 | Must revalidate before using |
| `no-store`                 | Don't cache at all           |
| `max-age=N`                | Cache for N seconds          |
| `s-maxage=N`               | CDN cache for N seconds      |
| `immutable`                | Content won't change         |
| `stale-while-revalidate=N` | Serve stale while fetching   |
| `stale-if-error=N`         | Serve stale on error         |
