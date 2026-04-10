# HTTP Headers Reference

## Reading Headers

```vcl
// Access header value
declare local var.auth STRING;
set var.auth = req.http.Authorization;

// Check if header exists
if (req.http.X-Custom) {
  // header exists and has value
}

// Check header value
if (req.http.Accept ~ "application/json") {
  // contains json
}
```

## Setting Headers

### Request Headers

```vcl
sub vcl_recv {
  #FASTLY recv

  // Set header
  set req.http.X-Forwarded-For = client.ip;
  set req.http.X-Request-ID = uuid.version4();

  // Set from another header
  set req.http.X-Original-Host = req.http.Host;
}
```

### Response Headers

```vcl
sub vcl_deliver {
  #FASTLY deliver

  set resp.http.X-Cache = "HIT";
  set resp.http.X-Served-By = server.hostname;
  set resp.http.Cache-Control = "public, max-age=3600";
}
```

### Backend Request Headers

```vcl
sub vcl_miss {
  #FASTLY miss

  set bereq.http.X-Forwarded-Proto = if(req.is_ssl, "https", "http");
  set bereq.http.X-Real-IP = client.ip;
}
```

## Removing Headers

```vcl
// Remove single header
unset req.http.Cookie;
unset resp.http.Server;

// Remove is alias for unset
remove resp.http.X-Powered-By;
```

## Adding Multiple Values

Use `add` to append headers (for headers like Set-Cookie):

```vcl
sub vcl_deliver {
  #FASTLY deliver

  add resp.http.Set-Cookie = "session=abc123; Path=/; HttpOnly";
  add resp.http.Set-Cookie = "user=john; Path=/";

  add resp.http.Link = "</styles.css>; rel=preload; as=style";
  add resp.http.Link = "</script.js>; rel=preload; as=script";
}
```

## Header Subfields

Access and modify specific parts of structured headers:

```vcl
// Cache-Control subfields
set resp.http.Cache-Control:max-age = "3600";
set resp.http.Cache-Control:public = "";

// Result: Cache-Control: max-age=3600, public

// Content-Type subfields
set resp.http.Content-Type:charset = "utf-8";
```

## Header Functions

### header.get

Get the first value of a header:

```vcl
declare local var.cookie STRING;
set var.cookie = header.get(req, "Cookie");
```

### header.set

Set a header value:

```vcl
call header.set(resp, "X-Custom", "value");
```

### header.filter

Remove headers matching pattern:

```vcl
// Remove all X- headers from response
call header.filter(resp, "^X-");

// Remove internal headers
call header.filter(resp, "^X-Internal-");
```

### header.filter_except

Keep only headers matching pattern:

```vcl
// Keep only specified response headers
call header.filter_except(resp, "^(Content-Type|Content-Length|Cache-Control)$");
```

## Cookie Handling

### Reading Cookies

```vcl
// Full cookie header
declare local var.cookies STRING;
set var.cookies = req.http.Cookie;

// Parse specific cookie using subfield
declare local var.session STRING;
set var.session = subfield(req.http.Cookie, "session", ";");
```

### Setting Cookies

```vcl
sub vcl_deliver {
  #FASTLY deliver

  // Basic cookie
  add resp.http.Set-Cookie = "name=value";

  // With attributes
  add resp.http.Set-Cookie = "session=abc123; Path=/; HttpOnly; Secure; SameSite=Strict";

  // With expiry
  add resp.http.Set-Cookie = "remember=1; Path=/; Max-Age=2592000";
}
```

### Deleting Cookies

```vcl
sub vcl_deliver {
  #FASTLY deliver

  // Expire the cookie
  add resp.http.Set-Cookie = "session=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT";
}
```

### setcookie Functions

```vcl
// Get cookie value from Set-Cookie header
declare local var.val STRING;
set var.val = setcookie.get_value_by_name(resp, "session");

// Delete specific Set-Cookie by name
call setcookie.delete_by_name(resp, "unwanted");
```

## Common Patterns

### Forwarding Client Information

```vcl
sub vcl_recv {
  #FASTLY recv

  // Standard forwarding headers
  set req.http.X-Forwarded-For = client.ip;
  set req.http.X-Forwarded-Proto = if(req.is_ssl, "https", "http");
  set req.http.X-Forwarded-Host = req.http.Host;

  // True-Client-IP (single IP)
  set req.http.True-Client-IP = client.ip;
}
```

### Security Headers

```vcl
sub vcl_deliver {
  #FASTLY deliver

  set resp.http.X-Content-Type-Options = "nosniff";
  set resp.http.X-Frame-Options = "DENY";
  set resp.http.X-XSS-Protection = "1; mode=block";
  set resp.http.Referrer-Policy = "strict-origin-when-cross-origin";
  set resp.http.Strict-Transport-Security = "max-age=31536000; includeSubDomains";

  // CSP
  set resp.http.Content-Security-Policy = "default-src 'self'";
}
```

### CORS Headers

```vcl
sub vcl_deliver {
  #FASTLY deliver

  // Simple CORS
  set resp.http.Access-Control-Allow-Origin = "*";

  // Specific origin
  if (req.http.Origin ~ "^https://(www\.)?example\.com$") {
    set resp.http.Access-Control-Allow-Origin = req.http.Origin;
    set resp.http.Access-Control-Allow-Methods = "GET, POST, OPTIONS";
    set resp.http.Access-Control-Allow-Headers = "Content-Type, Authorization";
    set resp.http.Access-Control-Max-Age = "86400";
    set resp.http.Vary = "Origin";
  }
}

sub vcl_recv {
  #FASTLY recv

  // Handle preflight
  if (req.method == "OPTIONS") {
    error 204 "No Content";
  }
}

sub vcl_error {
  #FASTLY error

  if (obj.status == 204) {
    set obj.http.Access-Control-Allow-Origin = req.http.Origin;
    set obj.http.Access-Control-Allow-Methods = "GET, POST, OPTIONS";
    set obj.http.Access-Control-Allow-Headers = "Content-Type, Authorization";
    return (deliver);
  }
}
```

### Vary Header Management

```vcl
sub vcl_fetch {
  #FASTLY fetch

  // Add to Vary header for proper caching
  if (!beresp.http.Vary) {
    set beresp.http.Vary = "Accept-Encoding";
  } else if (beresp.http.Vary !~ "Accept-Encoding") {
    set beresp.http.Vary = beresp.http.Vary + ", Accept-Encoding";
  }
}
```

### Stripping Headers for Privacy

```vcl
sub vcl_deliver {
  #FASTLY deliver

  // Remove server info
  unset resp.http.Server;
  unset resp.http.X-Powered-By;
  unset resp.http.X-AspNet-Version;
  unset resp.http.X-AspNetMvc-Version;

  // Remove debugging headers
  unset resp.http.X-Debug;
  unset resp.http.X-Request-Id;
}
```

## Header Variable Reference

| Prefix          | Scope                                              | Description              |
| --------------- | -------------------------------------------------- | ------------------------ |
| `req.http.*`    | recv, hash, miss, pass, fetch, deliver, error, log | Request headers          |
| `bereq.http.*`  | miss, pass, fetch                                  | Backend request headers  |
| `beresp.http.*` | fetch                                              | Backend response headers |
| `resp.http.*`   | deliver, log                                       | Final response headers   |
| `obj.http.*`    | hit, error                                         | Cached object headers    |
