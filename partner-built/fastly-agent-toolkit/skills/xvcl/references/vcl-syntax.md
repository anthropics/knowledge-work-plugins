# VCL Syntax Reference

## Data Types

### Primitive Types

| Type      | Description             | Example                      |
| --------- | ----------------------- | ---------------------------- |
| `STRING`  | Text, UTF-8 encoded     | `"hello"`, `{"long string"}` |
| `INTEGER` | 64-bit signed integer   | `123`, `0x5a5a`              |
| `FLOAT`   | IEEE 754 floating point | `3.14`, `1.5e-3`             |
| `BOOL`    | Boolean                 | `true`, `false`              |
| `TIME`    | Unix timestamp          | `now`                        |
| `RTIME`   | Duration                | `10s`, `5m`, `1h`, `1d`      |
| `IP`      | IP address              | `"192.168.1.1"`              |

### Duration Units

```vcl
declare local var.ttl RTIME;
set var.ttl = 100ms;  // milliseconds
set var.ttl = 30s;    // seconds
set var.ttl = 5m;     // minutes
set var.ttl = 1h;     // hours
set var.ttl = 1d;     // days
set var.ttl = 1w;     // weeks
set var.ttl = 1y;     // years
```

### String Formats

```vcl
// Double-quoted (escape sequences work)
set var.s = "hello\nworld";

// Long string (no escape processing)
set var.s = {"raw string with "quotes" inside"};

// Heredoc (custom delimiter for complex content)
set var.json = {json"{"key": "value"}"json};
```

## Operators

### Comparison

| Operator | Description           |
| -------- | --------------------- |
| `==`     | Equal                 |
| `!=`     | Not equal             |
| `<`      | Less than             |
| `>`      | Greater than          |
| `<=`     | Less than or equal    |
| `>=`     | Greater than or equal |
| `~`      | Regex match           |
| `!~`     | Regex non-match       |

### Logical

| Operator | Description         |
| -------- | ------------------- |
| `&&`     | AND (short-circuit) |
| `\|\|`   | OR (short-circuit)  |
| `!`      | NOT                 |

### String

| Operator | Description   |
| -------- | ------------- |
| `+`      | Concatenation |

```vcl
set var.path = req.url.path + "?v=1";
set var.host = "api." + req.http.Host;
```

### Assignment

```vcl
set var.x = 10;       // assign
set var.x += 5;       // add
set var.x -= 2;       // subtract
set var.x *= 3;       // multiply
set var.x /= 2;       // divide
set var.x %= 7;       // modulo
```

## Control Flow

### If/Else

```vcl
if (condition) {
  // statements
} else if (other_condition) {
  // statements
} else {
  // statements
}
```

### Switch/Case

```vcl
switch (req.url.path) {
  case ~ "^/api/":
    set req.backend = api_backend;
    break;
  case ~ "^/static/":
    set req.backend = static_backend;
    break;
  default:
    set req.backend = default_backend;
    break;
}
```

### Regex Matching

```vcl
if (req.url.path ~ "^/products/([0-9]+)$") {
  set req.http.X-Product-ID = re.group.1;
}

// Case-insensitive
if (req.http.Accept ~ "(?i)image/webp") {
  set req.http.X-Format = "webp";
}
```

## Variable Declaration

```vcl
declare local var.name TYPE;

// Examples
declare local var.user_id STRING;
declare local var.count INTEGER;
declare local var.enabled BOOL;
declare local var.start_time TIME;
declare local var.cache_ttl RTIME;
declare local var.rate FLOAT;
```

## Statements

### Set

```vcl
set var.x = value;
set req.http.X-Custom = "value";
set beresp.ttl = 1h;
```

### Unset/Remove

```vcl
unset req.http.Cookie;
remove resp.http.X-Internal;  // alias for unset
```

### Add (append header)

```vcl
add resp.http.Set-Cookie = "session=abc; Path=/";
add resp.http.Set-Cookie = "user=123; Path=/";
```

### Return

```vcl
return (lookup);   // in vcl_recv
return (deliver);  // in vcl_fetch, vcl_deliver
return (pass);     // bypass cache
return (error);    // trigger error
```

### Error

```vcl
error 404 "Not Found";
error 503 "Service Unavailable";
error 901 "Custom Error";  // custom status for internal handling
```

### Restart

```vcl
if (req.restarts < 2) {
  restart;
}
```

### Synthetic

```vcl
synthetic {"<html><body>Error</body></html>"};
synthetic {json"{"error": "not_found"}"json};
```

### Log

```vcl
log "Request: " + req.method + " " + req.url;
log "Client IP: " + client.ip;
```

### Call

```vcl
call my_subroutine;
```

## Regular Expressions

PCRE2 (Perl-compatible) syntax:

| Pattern   | Matches             |
| --------- | ------------------- |
| `^`       | Start of string     |
| `$`       | End of string       |
| `.`       | Any character       |
| `*`       | Zero or more        |
| `+`       | One or more         |
| `?`       | Zero or one         |
| `\d`      | Digit               |
| `\w`      | Word character      |
| `\s`      | Whitespace          |
| `[abc]`   | Character class     |
| `(...)`   | Capture group       |
| `(?:...)` | Non-capturing group |
| `(?i)`    | Case-insensitive    |

### Capture Groups

```vcl
if (req.url.path ~ "^/users/([0-9]+)/posts/([0-9]+)$") {
  set req.http.X-User-ID = re.group.1;
  set req.http.X-Post-ID = re.group.2;
}
```

## Comments

```vcl
// Single-line comment
# Alternative single-line

/* Multi-line
   comment */
```

## Key Variables

### Request (`req.*`)

| Variable       | Type    | Description                |
| -------------- | ------- | -------------------------- |
| `req.method`   | STRING  | HTTP method                |
| `req.url`      | STRING  | Full URL with query string |
| `req.url.path` | STRING  | URL path only              |
| `req.url.qs`   | STRING  | Query string only          |
| `req.http.*`   | STRING  | Request headers            |
| `req.backend`  | BACKEND | Selected backend           |
| `req.restarts` | INTEGER | Restart count              |
| `req.is_ssl`   | BOOL    | HTTPS request              |
| `req.hash`     | STRING  | Cache hash key             |

### Response (`resp.*`)

| Variable      | Type    | Description      |
| ------------- | ------- | ---------------- |
| `resp.status` | INTEGER | HTTP status code |
| `resp.http.*` | STRING  | Response headers |

### Backend Request (`bereq.*`)

| Variable       | Type   | Description       |
| -------------- | ------ | ----------------- |
| `bereq.method` | STRING | Method to origin  |
| `bereq.url`    | STRING | URL to origin     |
| `bereq.http.*` | STRING | Headers to origin |

### Backend Response (`beresp.*`)

| Variable           | Type    | Description        |
| ------------------ | ------- | ------------------ |
| `beresp.status`    | INTEGER | Origin status code |
| `beresp.http.*`    | STRING  | Origin headers     |
| `beresp.ttl`       | RTIME   | Cache TTL          |
| `beresp.grace`     | RTIME   | Grace period       |
| `beresp.cacheable` | BOOL    | Is cacheable       |

### Client (`client.*`)

| Variable                  | Type    | Description       |
| ------------------------- | ------- | ----------------- |
| `client.ip`               | IP      | Client IP address |
| `client.geo.country_code` | STRING  | Country code      |
| `client.geo.city`         | STRING  | City name         |
| `client.as.number`        | INTEGER | ASN               |

### Object (`obj.*`)

| Variable     | Type    | Description           |
| ------------ | ------- | --------------------- |
| `obj.status` | INTEGER | Cached object status  |
| `obj.http.*` | STRING  | Cached object headers |
| `obj.ttl`    | RTIME   | Remaining TTL         |
| `obj.grace`  | RTIME   | Grace period          |

### Server (`server.*`)

| Variable            | Type   | Description     |
| ------------------- | ------ | --------------- |
| `server.datacenter` | STRING | Data center ID  |
| `server.region`     | STRING | Region          |
| `server.hostname`   | STRING | Server hostname |

### Time

| Variable | Type | Description  |
| -------- | ---- | ------------ |
| `now`    | TIME | Current time |
