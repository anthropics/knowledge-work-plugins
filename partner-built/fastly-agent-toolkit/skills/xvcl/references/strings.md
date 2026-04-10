# String Functions Reference

## Basic String Operations

### Length

```vcl
declare local var.len INTEGER;
set var.len = std.strlen("hello");  // 5
set var.len = std.strlen(req.url);
```

### Case Conversion

```vcl
declare local var.lower STRING;
declare local var.upper STRING;

set var.lower = std.tolower("Hello World");  // "hello world"
set var.upper = std.toupper("Hello World");  // "HELLO WORLD"
```

### Substring

```vcl
declare local var.sub STRING;

// substr(string, start, length)
set var.sub = substr("hello world", 0, 5);   // "hello"
set var.sub = substr("hello world", 6, 5);   // "world"

// Negative start counts from end
set var.sub = substr("hello", -2, 2);  // "lo"
```

### String Reversal

```vcl
declare local var.rev STRING;
set var.rev = std.strrev("hello");  // "olleh"
```

### Padding

```vcl
declare local var.padded STRING;

// strpad(string, length, padding, position)
// position: "left", "right", "both"
set var.padded = std.strpad("42", 5, "0", "left");   // "00042"
set var.padded = std.strpad("hi", 6, "-", "right");  // "hi----"
set var.padded = std.strpad("x", 5, "*", "both");    // "**x**"
```

## Search and Replace

### Simple Replace

```vcl
declare local var.result STRING;

// Replace first occurrence
set var.result = std.replace("hello world", "world", "there");  // "hello there"

// Replace prefix
set var.result = std.replace_prefix("/api/v1/users", "/api/v1", "/api/v2");

// Replace suffix
set var.result = std.replace_suffix("file.txt", ".txt", ".json");

// Replace all occurrences
set var.result = std.replaceall("a-b-c-d", "-", "_");  // "a_b_c_d"
```

### Regex Replace

```vcl
declare local var.result STRING;

// Replace first match
set var.result = regsub("hello 123 world 456", "[0-9]+", "XXX");  // "hello XXX world 456"

// Replace all matches
set var.result = regsuball("hello 123 world 456", "[0-9]+", "XXX");  // "hello XXX world XXX"

// Using capture groups
set var.result = regsub("John Smith", "(\w+) (\w+)", "\2, \1");  // "Smith, John"
```

### Search

```vcl
declare local var.found BOOL;
declare local var.pos INTEGER;

// Find substring position
set var.pos = std.strstr("hello world", "world");  // 6 (0-indexed)
set var.pos = std.strstr("hello", "xyz");  // -1 (not found)

// Check prefix/suffix
set var.found = std.prefixof(req.url.path, "/api/");
set var.found = std.suffixof(req.url.path, ".json");
```

## Parsing and Conversion

### String to Number

```vcl
declare local var.num INTEGER;
declare local var.dec FLOAT;

// String to integer
set var.num = std.atoi("42");       // 42
set var.num = std.atoi("invalid");  // 0

// String to integer with base
set var.num = std.strtol("ff", 16);  // 255 (hex)
set var.num = std.strtol("777", 8);  // 511 (octal)

// String to float
set var.dec = std.atof("3.14");
set var.dec = std.strtof("1.5e-3");
```

### Number to String

```vcl
declare local var.str STRING;

// Integer to string
set var.str = std.itoa(42);  // "42"

// Integer to string with custom charset
set var.str = std.itoa_charset(255, "0123456789abcdef");  // "ff"
```

### IP Conversion

```vcl
declare local var.ip IP;
declare local var.str STRING;

// String to IP
set var.ip = std.ip("192.168.1.1", "0.0.0.0");

// IP to string
set var.str = std.ip2str(client.ip);
```

## URL and Query String Functions

### Query String Operations

```vcl
declare local var.result STRING;

// Get query parameter value
set var.result = querystring.get(req.url, "page");

// Set query parameter
set var.result = querystring.set(req.url, "page", "2");

// Add query parameter
set var.result = querystring.add(req.url, "sort", "asc");

// Remove query parameters matching pattern
set var.result = querystring.filter(req.url, "utm_");

// Keep only specified parameters
set var.result = querystring.filter_except(req.url, "page,sort");

// Sort query parameters
set var.result = querystring.sort(req.url);

// Clean (remove empty params)
set var.result = querystring.clean(req.url);

// Remove all query parameters
set var.result = querystring.remove(req.url);
```

### URL Encoding

```vcl
declare local var.encoded STRING;
declare local var.decoded STRING;

// URL encode
set var.encoded = urlencode("hello world?");  // "hello%20world%3F"

// URL decode
set var.decoded = urldecode("hello%20world");  // "hello world"
```

### Path Operations

```vcl
declare local var.result STRING;

// Get basename (filename)
set var.result = std.basename("/path/to/file.txt");  // "file.txt"

// Get dirname (directory)
set var.result = std.dirname("/path/to/file.txt");  // "/path/to"
```

## Subfield Parsing

Parse structured header values:

```vcl
declare local var.value STRING;

// Parse semicolon-separated values
set var.value = subfield(req.http.Cookie, "session", ";");

// Parse comma-separated values
set var.value = subfield(req.http.Accept, "text/html", ",");
```

## Collection and Joining

```vcl
// Collect header values (for multi-value headers)
declare local var.values STRING;
set var.values = std.collect(req.http.Accept);
```

## JSON Escape

```vcl
declare local var.escaped STRING;
set var.escaped = json.escape("hello \"world\"");  // "hello \\\"world\\\""
```

## XML Escape

```vcl
declare local var.escaped STRING;
set var.escaped = xml.escape("<script>alert('xss')</script>");
// "&lt;script&gt;alert('xss')&lt;/script&gt;"
```

## UUID Generation

```vcl
declare local var.uuid STRING;

// Random UUID (v4)
set var.uuid = uuid.version4();

// Name-based UUID (v5)
set var.uuid = uuid.version5(uuid.dns(), "example.com");

// Time-based UUID (v7)
set var.uuid = uuid.version7();
```

## Common Patterns

### Normalize URL Path

```vcl
sub normalize_url {
  declare local var.path STRING;
  set var.path = std.tolower(req.url.path);
  set var.path = regsuball(var.path, "//+", "/");
  set var.path = regsub(var.path, "/$", "");
  set req.url = var.path + if(req.url.qs, "?" + req.url.qs, "");
}
```

### Extract File Extension

```vcl
sub vcl_recv {
  #FASTLY recv

  declare local var.ext STRING;
  if (req.url.path ~ "\.([a-z0-9]+)$") {
    set var.ext = std.tolower(re.group.1);
    set req.http.X-File-Extension = var.ext;
  }
}
```

### Parse Accept-Language

```vcl
sub vcl_recv {
  #FASTLY recv

  declare local var.lang STRING;

  // Use accept.language_lookup for proper q-value handling
  set var.lang = accept.language_lookup("en:de:fr:es", "en", req.http.Accept-Language);
  set req.http.X-Language = var.lang;
}
```

### Validate Email Format

```vcl
sub vcl_recv {
  #FASTLY recv

  if (req.http.X-Email) {
    if (req.http.X-Email !~ "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") {
      error 400 "Invalid email format";
    }
  }
}
```

## Function Reference

| Function                       | Description         | Return  |
| ------------------------------ | ------------------- | ------- |
| `std.strlen(s)`                | String length       | INTEGER |
| `std.tolower(s)`               | To lowercase        | STRING  |
| `std.toupper(s)`               | To uppercase        | STRING  |
| `substr(s, start, len)`        | Substring           | STRING  |
| `std.strrev(s)`                | Reverse string      | STRING  |
| `std.strpad(s, len, pad, pos)` | Pad string          | STRING  |
| `std.replace(s, old, new)`     | Replace first       | STRING  |
| `std.replaceall(s, old, new)`  | Replace all         | STRING  |
| `regsub(s, regex, repl)`       | Regex replace first | STRING  |
| `regsuball(s, regex, repl)`    | Regex replace all   | STRING  |
| `std.strstr(s, needle)`        | Find position       | INTEGER |
| `std.prefixof(s, prefix)`      | Has prefix          | BOOL    |
| `std.suffixof(s, suffix)`      | Has suffix          | BOOL    |
| `std.atoi(s)`                  | String to int       | INTEGER |
| `std.atof(s)`                  | String to float     | FLOAT   |
| `std.itoa(n)`                  | Int to string       | STRING  |
| `urlencode(s)`                 | URL encode          | STRING  |
| `urldecode(s)`                 | URL decode          | STRING  |
| `json.escape(s)`               | JSON escape         | STRING  |
| `xml.escape(s)`                | XML escape          | STRING  |
