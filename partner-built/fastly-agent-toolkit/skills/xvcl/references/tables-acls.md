# Tables and ACLs Reference

## Tables

Tables are key-value stores for configuration data.

### Table Declaration

```vcl
table redirects STRING {
  "/old-page": "/new-page",
  "/legacy": "/modern",
  "/about-us": "/about",
}

table cache_ttls INTEGER {
  "html": "300",
  "json": "60",
  "image": "86400",
}

table feature_flags BOOL {
  "new_checkout": "true",
  "dark_mode": "false",
}
```

### Table Types

| Type      | Description       | Example Value       |
| --------- | ----------------- | ------------------- |
| `STRING`  | Text values       | `"value"`           |
| `INTEGER` | Whole numbers     | `"123"`             |
| `FLOAT`   | Decimal numbers   | `"3.14"`            |
| `BOOL`    | Boolean           | `"true"`, `"false"` |
| `RTIME`   | Duration          | `"60s"`, `"1h"`     |
| `IP`      | IP address        | `"192.168.1.1"`     |
| `BACKEND` | Backend reference | -                   |
| `ACL`     | ACL reference     | -                   |

### Table Lookup

```vcl
declare local var.value STRING;

// Basic lookup (returns empty string if not found)
set var.value = table.lookup(redirects, req.url.path);

// With default value
set var.value = table.lookup(redirects, req.url.path, "/404");

// Check if key exists
if (table.contains(redirects, req.url.path)) {
  // Key exists
}
```

### Typed Lookups

```vcl
declare local var.ttl INTEGER;
declare local var.flag BOOL;
declare local var.rate FLOAT;

// Integer lookup
set var.ttl = table.lookup_integer(cache_ttls, "html", 0);

// Boolean lookup
set var.flag = table.lookup_bool(feature_flags, "new_checkout", false);

// Float lookup
set var.rate = table.lookup_float(rates, "standard", 1.0);

// RTIME lookup
declare local var.duration RTIME;
set var.duration = table.lookup_rtime(timeouts, "default", 30s);

// IP lookup
declare local var.ip IP;
set var.ip = table.lookup_ip(servers, "primary", "0.0.0.0");
```

### Backend Table

```vcl
table backends BACKEND {
  "api": "api_backend",
  "web": "web_backend",
  "static": "static_backend",
}

sub vcl_recv {
  #FASTLY recv

  declare local var.backend BACKEND;
  set var.backend = table.lookup_backend(backends, req.http.X-Service);

  if (var.backend) {
    set req.backend = var.backend;
  }

  return (lookup);
}
```

### ACL Table

```vcl
table ip_lists ACL {
  "internal": "internal_ips",
  "blocklist": "blocked_ips",
}

sub vcl_recv {
  #FASTLY recv

  declare local var.acl ACL;
  set var.acl = table.lookup_acl(ip_lists, "internal");

  if (client.ip ~ var.acl) {
    set req.http.X-Internal = "true";
  }
}
```

### Regex Table Lookup

```vcl
table patterns STRING {
  "^/api/v[0-9]+/": "api",
  "^/static/": "static",
  "^/admin/": "admin",
}

sub vcl_recv {
  #FASTLY recv

  declare local var.match STRING;

  // Lookup by regex pattern matching
  set var.match = table.lookup_regex(patterns, req.url.path);

  if (var.match == "admin") {
    // Handle admin routes
  }
}
```

## ACLs (Access Control Lists)

### ACL Declaration

```vcl
acl internal_ips {
  "10.0.0.0"/8;        // Private class A
  "172.16.0.0"/12;     // Private class B
  "192.168.0.0"/16;    // Private class C
  "127.0.0.1";         // Localhost
}

acl blocked_ips {
  "1.2.3.4";           // Single IP
  "5.6.7.0"/24;        // CIDR range
  ! "5.6.7.100";       // Exclude specific IP from range
}

acl ipv6_clients {
  "2001:db8::"/32;     // IPv6 range
  "::1";               // IPv6 localhost
}
```

### ACL Matching

```vcl
sub vcl_recv {
  #FASTLY recv

  // Check if client IP matches ACL
  if (client.ip ~ internal_ips) {
    set req.http.X-Internal = "true";
  }

  // Check if client IP is blocked
  if (client.ip ~ blocked_ips) {
    error 403 "Forbidden";
  }
}
```

### Negation in ACLs

```vcl
acl allowed_ips {
  "10.0.0.0"/8;        // Allow 10.x.x.x
  ! "10.0.0.1";        // But not 10.0.0.1
  ! "10.0.0.2";        // And not 10.0.0.2
}
```

## Common Patterns

### URL Redirects

```vcl
table redirects STRING {
  "/old-page": "/new-page",
  "/legacy-path": "/modern-path",
  "/moved": "https://example.com/new-location",
}

sub vcl_recv {
  #FASTLY recv

  declare local var.redirect STRING;
  set var.redirect = table.lookup(redirects, req.url.path);

  if (var.redirect) {
    error 801 var.redirect;
  }
}

sub vcl_error {
  #FASTLY error

  if (obj.status == 801) {
    set obj.status = 301;
    set obj.http.Location = obj.response;
    return (deliver);
  }
}
```

### Feature Flags

```vcl
table features BOOL {
  "new_checkout": "true",
  "dark_mode": "false",
  "beta_api": "true",
}

sub vcl_recv {
  #FASTLY recv

  if (table.lookup_bool(features, "new_checkout", false)) {
    set req.http.X-Feature-New-Checkout = "enabled";
  }

  if (table.lookup_bool(features, "beta_api", false)) {
    set req.backend = beta_api_backend;
  }
}
```

### Rate Limits Configuration

```vcl
table rate_limits INTEGER {
  "default": "100",
  "premium": "1000",
  "api": "500",
}

sub vcl_recv {
  #FASTLY recv

  declare local var.limit INTEGER;
  declare local var.tier STRING;

  // Get user tier from header
  set var.tier = req.http.X-User-Tier;
  if (!var.tier) {
    set var.tier = "default";
  }

  set var.limit = table.lookup_integer(rate_limits, var.tier, 100);
  set req.http.X-Rate-Limit = var.limit;
}
```

### IP-Based Access Control

```vcl
acl office_ips {
  "203.0.113.0"/24;
  "198.51.100.0"/24;
}

acl vpn_ips {
  "192.0.2.0"/24;
}

sub vcl_recv {
  #FASTLY recv

  // Admin requires office or VPN
  if (req.url.path ~ "^/admin/") {
    if (!(client.ip ~ office_ips) && !(client.ip ~ vpn_ips)) {
      error 403 "Access denied";
    }
  }
}
```

### Country-Based Routing

```vcl
table country_backends BACKEND {
  "US": "us_backend",
  "EU": "eu_backend",
  "AP": "ap_backend",
}

sub vcl_recv {
  #FASTLY recv

  declare local var.region STRING;

  // Map country to region
  if (client.geo.country_code ~ "^(US|CA|MX)$") {
    set var.region = "US";
  } else if (client.geo.country_code ~ "^(GB|DE|FR|IT|ES)$") {
    set var.region = "EU";
  } else {
    set var.region = "AP";
  }

  set req.backend = table.lookup_backend(country_backends, var.region);
}
```

### Dynamic Configuration (XVCL)

```xvcl
#const REDIRECTS = [
  ("/old", "/new"),
  ("/legacy", "/modern"),
  ("/about-us", "/about"),
]

table redirects STRING {
#for old, new in REDIRECTS
  "{{old}}": "{{new}}",
#endfor
}

#const BLOCKED_IPS = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]

acl blocked {
#for ip in BLOCKED_IPS
  "{{ip}}";
#endfor
}
```

## Function Reference

| Function                                | Description               | Return  |
| --------------------------------------- | ------------------------- | ------- |
| `table.lookup(t, key)`                  | Lookup with empty default | STRING  |
| `table.lookup(t, key, default)`         | Lookup with default       | STRING  |
| `table.contains(t, key)`                | Check key exists          | BOOL    |
| `table.lookup_integer(t, key, default)` | Integer lookup            | INTEGER |
| `table.lookup_float(t, key, default)`   | Float lookup              | FLOAT   |
| `table.lookup_bool(t, key, default)`    | Boolean lookup            | BOOL    |
| `table.lookup_rtime(t, key, default)`   | Duration lookup           | RTIME   |
| `table.lookup_ip(t, key, default)`      | IP lookup                 | IP      |
| `table.lookup_backend(t, key)`          | Backend lookup            | BACKEND |
| `table.lookup_acl(t, key)`              | ACL lookup                | ACL     |
| `table.lookup_regex(t, input)`          | Regex pattern lookup      | STRING  |
