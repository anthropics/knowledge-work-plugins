# XVCL Directives — Complete Reference

All XVCL directives are resolved at compile time. The compiler runs 6 passes:
1. Join multi-line directives (unbalanced brackets auto-join lines)
2. Extract `#const` declarations
3. Process `#include` files
4. Extract `#inline` macros
5. Extract `#def` functions
6. Process `#for`, `#if`, `#let`, template expressions `{{ }}`

## Table of Contents

- [Constants — #const](#constants)
- [Template Expressions — {{ }}](#template-expressions)
- [For Loops — #for](#for-loops)
- [Conditionals — #if](#conditionals)
- [Variable Shorthand — #let](#variable-shorthand)
- [Functions — #def](#functions)
- [Inline Macros — #inline](#inline-macros)
- [Includes — #include](#includes)
- [Multi-line Directives](#multi-line-directives)
- [Error Messages](#error-messages)

---

## Constants

```xvcl
#const NAME = value              // type auto-inferred
#const NAME TYPE = value         // explicit type
```

### Supported Types
- `INTEGER` — whole numbers: `#const PORT INTEGER = 8080`
- `STRING` — text: `#const HOST STRING = "example.com"`
- `FLOAT` — decimals: `#const VERSION FLOAT = 1.5`
- `BOOL` — `true`/`false` (case-insensitive, `True`/`False` also work): `#const DEBUG BOOL = false`

### Type Inference
When type is omitted, it's inferred from the value:
```xvcl
#const PORT = 8080            // INTEGER
#const HOST = "example.com"   // STRING
#const ENABLED = true         // BOOL
#const RATIO = 1.5            // FLOAT
#const ITEMS = ["a", "b"]     // LIST
#const PAIRS = [("a", 1)]     // LIST of tuples
```

### Expressions in Constants
```xvcl
#const BASE_TTL = 3600
#const DOUBLE_TTL = BASE_TTL * 2    // 7200
#const LABEL = "v" + str(VERSION)   // string concatenation
```

### Lists and Tuples
```xvcl
#const REGIONS = ["us-east", "us-west", "eu-west"]
#const BACKENDS = [("api", "api.example.com", 443), ("web", "www.example.com", 80)]
```

Multi-line lists are supported (lines auto-join when brackets are unbalanced):
```xvcl
#const BACKENDS = [
  ("api", "api.example.com", 443),
  ("web", "www.example.com", 80),
  ("static", "static.example.com", 443)
]
```

### Scope
Constants defined in any file (including included files) are available globally. Constants must be defined before use.

---

## Template Expressions

Embed compile-time expressions anywhere in code using `{{ }}`:

```xvcl
{{CONST_NAME}}                        // constant value
{{PORT * 2}}                          // arithmetic
{{value if condition else other}}     // ternary
```

### Built-in Functions

| Function            | Description              | Example                                  |
| ------------------- | ------------------------ | ---------------------------------------- |
| `range(n)`          | Integers 0 to n-1        | `range(5)` → 0,1,2,3,4                   |
| `range(start, end)` | Integers start to end-1  | `range(2, 5)` → 2,3,4                    |
| `len(x)`            | Length of list or string | `len(REGIONS)` → 3                       |
| `enumerate(list)`   | (index, value) tuples    | `enumerate(["a","b"])` → (0,"a"),(1,"b") |
| `str(x)`            | Convert to string        | `str(8080)` → "8080"                     |
| `int(x)`            | Convert to integer       | `int("42")` → 42                         |
| `hex(n)`            | Integer to hex string    | `hex(255)` → "0xff"                      |
| `format(x, fmt)`    | Format with Python spec  | `format(42, '05d')` → "00042"            |
| `min(a, b, ...)`    | Minimum value            | `min(5, 3)` → 3                          |
| `max(a, b, ...)`    | Maximum value            | `max(5, 3)` → 5                          |
| `abs(n)`            | Absolute value           | `abs(-42)` → 42                          |
| `true` / `false`    | Boolean literals (also `True`/`False` in expressions) |                     |

### Operators in Expressions
- Arithmetic: `+`, `-`, `*`, `/`, `//` (integer division), `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Boolean: `and`, `or`, `not`
- String: `+` (concatenation)

### Examples
```xvcl
#const PORT = 8080
set req.http.X-Port = "{{PORT}}";
set req.http.X-Double = "{{PORT * 2}}";
set req.http.X-Hex = "{{hex(PORT)}}";
set req.http.X-Padded = "{{format(42, '05d')}}";
set req.http.X-Debug = "{{ENV if ENV != 'prod' else 'disabled'}}";

// In backend names
#for i in range(3)
backend web_{{i}} { .port = "{{8080 + i}}"; }
#endfor
```

---

## For Loops

```xvcl
#for variable in iterable
  // body
#endfor
```

### Iteration Sources

```xvcl
// Range (single argument)
#for i in range(5)
  // i = 0, 1, 2, 3, 4
#endfor

// Range (two arguments)
#for i in range(2, 8)
  // i = 2, 3, 4, 5, 6, 7
#endfor

// List constant
#const REGIONS = ["us", "eu", "ap"]
#for region in REGIONS
  backend F_{{region}} { .host = "{{region}}.example.com"; }
#endfor

// Tuple unpacking
#const BACKENDS = [("api", "api.example.com"), ("web", "www.example.com")]
#for name, host in BACKENDS
  backend F_{{name}} { .host = "{{host}}"; }
#endfor

// Triple unpacking
#const SERVICES = [("api", "api.example.com", 443), ("web", "www.example.com", 80)]
#for name, host, port in SERVICES
  backend F_{{name}} {
    .host = "{{host}}";
    .port = "{{port}}";
  }
#endfor

// Enumerate (index + value)
#for idx, region in enumerate(REGIONS)
  set req.http.X-Region-{{idx}} = "{{region}}";
#endfor
```

### Nested Loops
```xvcl
#const REGIONS = ["us", "eu"]
#const ENVS = ["prod", "staging"]
#for region in REGIONS
  #for env in ENVS
    backend {{region}}_{{env}} {
      .host = "{{region}}-{{env}}.example.com";
    }
  #endfor
#endfor
// Generates: us_prod, us_staging, eu_prod, eu_staging
```

### Loop Variables in Expressions
Loop variables are available in `{{ }}` template expressions within the loop body:
```xvcl
#for i in range(3)
set req.http.X-Index-{{i}} = "{{i * 10}}";
#endfor
```

---

## Conditionals

```xvcl
#if condition
  // code
#endif

#if condition
  // code
#else
  // fallback
#endif

#if condition1
  // ...
#elif condition2
  // ...
#else
  // ...
#endif
```

### Supported Conditions
```xvcl
#if PRODUCTION                    // boolean constant
#if VERSION == 2                  // equality
#if PORT > 8000                   // comparison
#if DEBUG and ENV == "prod"       // boolean operators
#if not ENABLED                   // negation
#if VERSION >= 2 or LEGACY        // combined
```

### Nesting
```xvcl
#if PRODUCTION
  #if VERSION >= 2
    set req.http.X-Feature = "new";
  #else
    set req.http.X-Feature = "legacy";
  #endif
#endif
```

### Dead Code Elimination
False branches are completely excluded from the compiled output — no runtime cost.

---

## Variable Shorthand

`#let` is shorthand for `declare local` + `set`:

```xvcl
#let cache_key STRING = req.url.path;
#let counter INTEGER = 42;
#let is_cached BOOL = true;
```

Expands to:
```vcl
declare local var.cache_key STRING;
set var.cache_key = req.url.path;
declare local var.counter INTEGER;
set var.counter = 42;
declare local var.is_cached BOOL;
set var.is_cached = true;
```

Supported types: `STRING`, `INTEGER`, `FLOAT`, `BOOL`

---

## Functions

Reusable functions with typed parameters and return values. Compiled to VCL subroutines with parameters passed via `req.http.X-Func-*` headers.

### Single Return Value
```xvcl
#def function_name(param1 TYPE, param2 TYPE) -> RETURN_TYPE
  // VCL body
  return value;
#enddef
```

Example:
```xvcl
#def normalize_path(path STRING) -> STRING
  declare local var.result STRING;
  set var.result = std.tolower(path);
  set var.result = regsuball(var.result, "//+", "/");
  return var.result;
#enddef

sub vcl_recv {
  #FASTLY recv
  #let clean STRING = normalize_path(req.url.path);
}
```

### Tuple Return (Multiple Values)
```xvcl
#def function_name(params) -> (TYPE1, TYPE2)
  // body
  return val1, val2;
#enddef
```

Example:
```xvcl
#def parse_pair(s STRING) -> (STRING, STRING)
  declare local var.key STRING;
  declare local var.value STRING;
  set var.key = regsub(s, ":.*", "");
  set var.value = regsub(s, "^[^:]*:", "");
  return var.key, var.value;
#enddef

sub vcl_recv {
  #FASTLY recv
  declare local var.k STRING;
  declare local var.v STRING;
  set var.k, var.v = parse_pair("host:example.com");
}
```

### How Functions Compile

A function call like `set var.result = normalize_path(req.url.path);` expands to:
```vcl
set req.http.X-Func-normalize_path-path = req.url.path;
call normalize_path;
set var.result = req.http.X-Func-normalize_path-Return;
```

Type conversions are automatic:
- `INTEGER` ↔ STRING via `std.itoa()` / `std.atoi()`
- `FLOAT` ↔ STRING via string concatenation / `std.atof()`
- `BOOL` ↔ STRING via `"true"`/`"false"` strings

### Functions with Logic
```xvcl
#def should_cache(url STRING) -> BOOL
  declare local var.cacheable BOOL;
  if (url ~ "^/api/") {
    set var.cacheable = false;
  } else if (url ~ "\.(jpg|png|css|js)$") {
    set var.cacheable = true;
  } else {
    set var.cacheable = false;
  }
  return var.cacheable;
#enddef
```

### Parameters Without Types
Parameters without explicit types default to `STRING`:
```xvcl
#def concat(a, b) -> STRING
  declare local var.result STRING;
  set var.result = a + b;
  return var.result;
#enddef
```

---

## Inline Macros

Zero-overhead compile-time text substitution. Use for simple expressions; use `#def` for complex logic.

```xvcl
#inline macro_name(param1, param2, ...)
expression
#endinline
```

### Basic Usage
```xvcl
#inline cache_key(url, host)
digest.hash_md5(url + "|" + host)
#endinline

#inline normalize_host(host)
std.tolower(regsub(host, "^www\.", ""))
#endinline

sub vcl_hash {
  #FASTLY hash
  set req.hash += cache_key(req.url, normalize_host(req.http.Host));
}
```

### Auto-Parenthesization
When macro arguments contain operators, they are automatically wrapped in parentheses during expansion. This prevents precedence bugs when a macro's result is used inside a function call:

```xvcl
#inline cache_key(url, host)
digest.hash_md5(url + "|" + host)
#endinline

// Calling with a complex expression as argument:
set req.hash += cache_key(req.url, std.tolower(req.http.Host));
// Arguments are safely substituted into the digest.hash_md5() call
```

**Note:** Fastly VCL does not support parenthesized grouped expressions in string concatenation (e.g., `("a") + ("b")` is invalid). Macros work best when their body uses VCL function calls like `digest.hash_md5()`, `std.tolower()`, or `regsub()` rather than raw `+` operators.

### Nested Macros
Macros can call other macros (up to 10 levels of nesting):
```xvcl
#inline normalize_host(host)
std.tolower(regsub(host, "^www\.", ""))
#endinline

#inline cache_key(url, host)
digest.hash_md5(url + "|" + host)
#endinline

// Nested call:
set req.hash += cache_key(req.url, normalize_host(req.http.Host));
// Inner macro expands first, then outer
```

### Macros vs Functions

|           | Macro (`#inline`)              | Function (`#def`)                |
| --------- | ------------------------------ | -------------------------------- |
| Expansion | Compile-time text substitution | Runtime subroutine call          |
| Overhead  | None                           | Subroutine call + header passing |
| Body      | Single expression only         | Full VCL statements              |
| Return    | Expression result              | Explicit `return`                |
| Use case  | Simple expressions, wrappers   | Complex logic, conditionals      |

---

## Includes

```xvcl
#include "relative/path/file.xvcl"   // relative to current file
#include <path/file.xvcl>            // searches -I include paths
```

### Include Path Resolution
1. Relative to the directory of the current file
2. Relative to paths specified with `-I` flag on the command line

### Include-Once Semantics
Each file is included at most once. Duplicate includes are silently skipped:
```xvcl
#include "shared.xvcl"    // processed
#include "shared.xvcl"    // skipped (already included)
```

### Circular Include Detection
Circular includes produce an error:
```
Error: Circular include detected: main.xvcl -> util.xvcl -> main.xvcl
```

### Shared Constants
Constants defined in included files are available to the parent file and all subsequent includes.

### Typical Project Layout
```
main.xvcl                  // entry point
includes/
  config.xvcl              // #const definitions (shared across all files)
  backends.xvcl            // backend declarations
  security.xvcl            // security headers, ACLs
  routing.xvcl             // request routing logic
  caching.xvcl             // cache rules
```

```xvcl
// main.xvcl
#include "includes/config.xvcl"
#include "includes/backends.xvcl"
#include "includes/security.xvcl"
#include "includes/routing.xvcl"
#include "includes/caching.xvcl"
```

Compile with: `uvx xvcl main.xvcl -o main.vcl -I ./includes`

---

## Multi-line Directives

Lines with unbalanced brackets/parentheses are automatically joined. This allows readable multi-line declarations:

```xvcl
#const BACKENDS = [
  ("api", "api.example.com", 443),
  ("web", "www.example.com", 80),
  ("static", "static.example.com", 443)
]

#for name, port in [
  ("api", 8080),
  ("web", 80)
]
backend {{name}} { .port = "{{port}}"; }
#endfor
```

Multi-line function calls are also auto-joined:
```xvcl
set var.result = some_function(
  arg1,
  arg2,
  arg3
);
```

---

## Error Messages

Errors use a rustc-style structured format with rule IDs, source lines, carets, and actionable help. Use `--error-format json` for machine-readable output.

### Format
```
error[undefined-function]: Function 'normlize_path' is not defined
  --> main.xvcl:12
    |
 12 | set var.clean = normlize_path(req.url.path);
    |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   = did you mean: normalize_path?
   = note: defined functions: normalize_path, parse_pair
```

Each error includes a `rule` ID (e.g., `undefined-function`, `unclosed-block`, `return-count-mismatch`) that identifies the kind of problem.

### Common Errors

| Rule ID                    | Cause                              | Fix                                                     |
| -------------------------- | ---------------------------------- | ------------------------------------------------------- |
| `compile-error`            | Undefined constant or variable     | Check spelling; use `--debug` to list available names   |
| `invalid-for`              | Malformed `#for` syntax            | Use `#for VARIABLE in EXPRESSION`                       |
| `unclosed-block`           | Missing `#endfor` or `#endif`      | Add the matching closing directive                      |
| `undefined-function`       | Call to undefined XVCL function    | Check spelling; VCL builtins like `regsub` are ignored  |
| `return-count-mismatch`    | Wrong number of return variables   | Match variable count to function's return type          |
| `func-arg-count`           | Wrong number of arguments          | Check function/macro signature                          |
| `macro-recursion`          | Infinite macro expansion           | Remove circular macro references                        |
| `unpack-count-mismatch`    | Tuple size mismatch in `#for`      | Match variable count to tuple size                      |
| `file-not-found`           | Missing include or input file      | Check path; add `-I` flag                               |

### Name Suggestions
When an undefined name or function is used, xvcl suggests similar defined names:
```
error[compile-error]: Name 'PROT' is not defined
  --> main.xvcl:5
   = did you mean: PORT?
   = note: available: PRODUCTION, PORT, MAX_AGE
```

### JSON Error Output
Use `--error-format json` for structured diagnostics (useful for editor integrations):
```bash
uvx xvcl main.xvcl -o main.vcl --error-format json
```

### Debugging Tips
- Use `--debug` / `-v` to see expansion traces for each pass
- Use `--source-maps` to track which include file generated which output lines
- Use `--error-format json` for machine-readable diagnostics
- Start with a minimal file and add complexity incrementally
