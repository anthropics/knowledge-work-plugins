# Understanding Fastly Compute by Reading Fastlike Source Code

Fastlike is a complete Go implementation of the Fastly Compute XQD ABI — the interface between WebAssembly guest programs and the Fastly host runtime. Its source code documents every platform primitive (backends, caching, KV stores, rate limiting, ACLs, geolocation, and more) as executable code, making it the most precise reference for understanding how Fastly Compute works programmatically.

**Default local path**: `~/src/fastlike`

If not available locally, clone it:
```bash
git clone https://github.com/avidal/fastlike.git ~/src/fastlike
```

## Table of Contents

- [Understanding Fastly Compute by Reading Fastlike Source Code](#understanding-fastly-compute-by-reading-fastlike-source-code)
  - [Table of Contents](#table-of-contents)
  - [How to Use This Guide](#how-to-use-this-guide)
  - [Architecture Overview](#architecture-overview)
  - [Request Lifecycle](#request-lifecycle)
    - [Loop Detection](#loop-detection)
  - [Request and Response Manipulation](#request-and-response-manipulation)
    - [Common lookup patterns](#common-lookup-patterns)
  - [Body Handling and Streaming](#body-handling-and-streaming)
  - [Backend Subrequests](#backend-subrequests)
    - [Common lookup patterns](#common-lookup-patterns-1)
  - [Caching](#caching)
    - [Core Cache API (`xqd_cache.go`)](#core-cache-api-xqd_cachego)
    - [HTTP Cache API (`xqd_http_cache.go`)](#http-cache-api-xqd_http_cachego)
    - [Common lookup patterns](#common-lookup-patterns-2)
  - [KV Store](#kv-store)
    - [Common lookup patterns](#common-lookup-patterns-3)
  - [Dictionaries and Config Stores](#dictionaries-and-config-stores)
  - [Secret Stores](#secret-stores)
  - [Geolocation](#geolocation)
  - [Edge Rate Limiting](#edge-rate-limiting)
  - [Access Control Lists](#access-control-lists)
  - [Logging](#logging)
  - [Async Patterns](#async-patterns)
  - [Configuration via Options](#configuration-via-options)
  - [Tips for Agents](#tips-for-agents)

---

## How to Use This Guide

When you need to understand how a Fastly Compute feature works — how requests flow, what a backend subrequest does, how caching behaves, what KV store operations are available — **read the relevant source file directly** rather than guessing. The fastlike source mirrors Fastly's production ABI exactly, so the behavior you see in the code is the behavior you get on the platform.

The code uses C-style function signatures (not idiomatic Go) to match Fastly's Rust reference implementation, making it easy to cross-reference with Fastly's official documentation. Each `xqd_*.go` file implements a group of related ABI functions.

---

## Architecture Overview

**Location**: `fastlike.go`, `instance.go`, `wasmcontext.go`

| Layer           | File                                          | Purpose                                                      |
| --------------- | --------------------------------------------- | ------------------------------------------------------------ |
| Entry Point     | `fastlike.go`                                 | `http.Handler` interface, instance pooling (up to 16)        |
| WASM Context    | `wasmcontext.go`                              | Compiled WASM module, engine, linker with 249+ ABI functions |
| Instance        | `instance.go`                                 | Per-request state: store, memory, handles, execution         |
| ABI Functions   | `xqd_*.go`                                    | Host function implementations the guest WASM calls           |
| Data Structures | `backend.go`, `cache.go`, `kv_store.go`, etc. | Platform primitive implementations                           |
| Memory          | `memory.go`                                   | Read/write wrapper around WASM linear memory                 |
| Constants       | `constants.go`                                | XQD error codes, status codes, flags                         |
| Handles         | `handles.go`                                  | Handle allocation/deallocation for all resource types        |

**How to read `wasmcontext.go`**: This file links every ABI function name to its Go implementation. Search for a function name (e.g., `fastly_http_req`) to find which Go method implements it.

---

## Request Lifecycle

**Location**: `instance.go`, `xqd_http_downstream.go`

The per-request lifecycle in Fastly Compute:

1. **Setup** (`instance.go` → `setup()`): Fresh WASM store created, module instantiated, WASI configured
2. **Execute** (`instance.go` → `ServeHTTP()`): Guest's `_start` export called via `entry.Call()`
3. **Guest gets downstream request**: Calls `xqd_req_body_downstream_get` → receives handle to the incoming HTTP request
4. **Guest processes**: Manipulates request/response via ABI calls (headers, body, backend fetches, cache lookups, etc.)
5. **Guest sends response**: Calls `xqd_resp_send_downstream` → writes response back to client
6. **Reset** (`instance.go` → `reset()`): Handles closed, bodies cleaned up, instance returned to pool

**How to read `instance.go`**: The `setup()` method shows exactly what state is initialized per-request. The handle maps (`requests`, `responses`, `bodies`, `pendingRequests`, `kvStores`, `cacheHandles`, etc.) show every resource type available to guest code.

### Loop Detection

Fastlike adds `"fastlike"` to the `cdn-loop` header on every request. If a request arrives with `"fastlike"` already in `cdn-loop`, it returns 508 Loop Detected — the same mechanism Fastly uses in production.

---

## Request and Response Manipulation

**Location**: `xqd_request.go` (1,795 lines), `xqd_response.go`

These are the largest ABI files because HTTP manipulation is the core of Compute. They implement:

- **Headers**: Get, set, append, remove individual headers; get all header names/values
- **Method**: Get/set HTTP method
- **URI**: Get/set URL, including individual components (path, query string)
- **Version**: Get/set HTTP version
- **Auto-decompression**: Transparent gzip handling (`xqd_req_auto_decompress_response_set`)
- **Framing headers**: Control how `Content-Length` and `Transfer-Encoding` are handled
- **TLS info**: Client certificate, cipher suite, protocol version (in `xqd_request.go`)

### Common lookup patterns

**"How does header manipulation work in Compute?"** → Read `xqd_request.go`, search for `xqd_req_header_*` functions. Each one shows exactly how headers are read from and written to guest memory.

**"What request properties can I access?"** → Search `xqd_request.go` for all `xqd_req_*` function definitions — each one corresponds to a property or operation available to guest code.

**"How does auto-decompression work?"** → Read `xqd_request.go`, find `xqd_req_auto_decompress_response_set` — it sets flags on the request handle that affect how backend responses are processed.

---

## Body Handling and Streaming

**Location**: `xqd_body.go`

Bodies in Compute are independent resources with their own handles. Operations:

- `xqd_body_new` — Create empty body
- `xqd_body_read` — Read bytes from body
- `xqd_body_write` — Write/append bytes to body
- `xqd_body_append` — Append one body to another
- `xqd_body_close` — Close body (finalizes writes)
- `xqd_body_known_length` — Get body length if known
- `xqd_body_trailer_*` — HTTP trailer manipulation

**Streaming**: Bodies support streaming through a pipe mechanism — the writer and reader can be different goroutines, enabling streaming responses without buffering the entire body.

---

## Backend Subrequests

**Location**: `xqd_backend.go` (566 lines), `backend.go`

This is how Compute programs make origin fetches. Key functions:

- `xqd_req_send` — Send request to named backend, get response (blocking)
- `xqd_req_send_async` — Send request asynchronously, get a pending request handle
- `xqd_pending_req_poll` / `xqd_pending_req_wait` — Check/wait for async request completion
- `xqd_req_send_async_streaming` — Send with streaming body

**How to read `backend.go`**: The `Backend` struct shows all configurable properties:
- `Name`, `URL`, `Handler` — Identity and routing
- `ConnectTimeoutMs`, `FirstByteTimeoutMs`, `BetweenBytesTimeoutMs` — Timeout configuration
- `UseSSL`, `SSLMinVersion`, `SSLMaxVersion` — TLS settings
- `MaxConnections`, `MaxUse`, `MaxLifetimeMs` — Connection pooling
- `TCPKeepalive*` — Keep-alive settings
- `PreferIPv6` — IP version preference

**Dynamic backends**: `xqd_req_register_dynamic_backend` allows guest code to create backends at runtime rather than requiring them to be pre-configured.

### Common lookup patterns

**"How do backend timeouts work?"** → Read `backend.go` for the `Backend` struct fields, then `xqd_backend.go` for how they're applied during request sending.

**"How does backend selection work?"** → Read `xqd_backend.go` → `xqd_req_send` — it looks up the backend by name from the configured map, falls back to catch-all.

---

## Caching

**Location**: `xqd_cache.go` (853 lines), `xqd_http_cache.go` (930 lines), `cache.go`

Fastly Compute has two caching APIs:

### Core Cache API (`xqd_cache.go`)
Low-level cache operations:
- `xqd_cache_lookup` — Look up a cache key
- `xqd_cache_insert` — Insert/replace a cached object
- `xqd_cache_get_*` — Read cached object properties (body, age, TTL, hits, etc.)
- `xqd_cache_replace` / `xqd_cache_delete` — Modify/remove cached entries

### HTTP Cache API (`xqd_http_cache.go`)
Higher-level HTTP-aware caching with:
- **Vary support**: Cache variants based on request headers (e.g., `Accept-Encoding`)
- **Surrogate keys**: Tag cached objects for bulk invalidation
- **Request collapsing**: Only one backend request for concurrent cache misses on the same key
- **Stale-while-revalidate**: Serve stale content while refreshing in background

**How to read `cache.go`**: The `CachedObject` struct shows all properties of a cached entry:
- `Body`, `Length` — The cached content
- `MaxAgeNs`, `InitialAgeNs`, `StaleWhileRevalidateNs` — TTL configuration
- `VaryRule` — Which headers create cache variants
- `SurrogateKeys` — Tags for cache invalidation
- `UserMetadata` — Arbitrary metadata attached to cached objects
- `HitCount` — How many times this object has been served

### Common lookup patterns

**"How does request collapsing work?"** → Read `cache.go` → the `transactions` map and `CacheTransaction` type show how concurrent lookups for the same key are coalesced.

**"How does Vary work in Fastly's cache?"** → Read `xqd_http_cache.go`, search for `vary` — the code shows how variant keys are computed from request headers.

**"What cache properties can I set?"** → Read `xqd_cache.go`, find `xqd_cache_insert` and the `CacheWriteOptions` — they list every configurable cache property.

---

## KV Store

**Location**: `xqd_kv_store.go` (553 lines), `kv_store.go` (512 lines)

Fastly KV Store provides persistent key-value storage. Operations:

- `xqd_object_store_lookup` — Look up a key (async)
- `xqd_object_store_insert` — Insert/update a key (async)
- `xqd_object_store_delete` — Delete a key (async)
- `xqd_object_store_list` — List keys with cursor-based pagination

**How to read `kv_store.go`**: The `ObjectValue` struct shows what's stored per key:
- `Body` — The value bytes
- `Metadata` — Arbitrary metadata string
- `Generation` — Version number for optimistic concurrency
- `Expiration` — Optional TTL

All KV operations are async — the guest gets a pending handle and must poll/wait for completion. This mirrors production behavior where KV operations involve network I/O.

### Common lookup patterns

**"What KV operations are available?"** → List all `xqd_object_store_*` functions in `xqd_kv_store.go`.

**"How does KV pagination work?"** → Read `xqd_kv_store.go` → `xqd_object_store_list` — shows cursor-based iteration with configurable page size and prefix filtering.

**"How does generation-based concurrency work?"** → Read `kv_store.go` → `Insert()` method — shows how generation numbers enable compare-and-swap semantics.

---

## Dictionaries and Config Stores

**Location**: `xqd_dictionary.go`, `xqd_config_store.go`, `dictionary.go`, `config_store.go`

These are read-only key-value stores available to Compute programs:

- **Dictionaries** (legacy): `xqd_dictionary_open` + `xqd_dictionary_get` — Simple string→string lookup. Same as VCL `table` lookups.
- **Config Stores** (current): `xqd_config_store_open` + `xqd_config_store_get` — Same concept, newer API.

Both are configured at startup and are immutable during request processing.

---

## Secret Stores

**Location**: `xqd_secret_store.go`, `secret_store.go`

Separate from config stores to maintain security boundaries:

- `xqd_secret_store_open` — Open a named secret store
- `xqd_secret_store_get` — Retrieve a secret by name
- `xqd_secret_lookup_plaintext` — Read the secret's plaintext value

In production, secrets are encrypted at rest and only decrypted when accessed by authorized services.

---

## Geolocation

**Location**: `xqd_geo.go`, `geo.go`

IP-to-location lookups — the same data available as `client.geo.*` in VCL:

- `xqd_geo_lookup` — Takes an IP address, returns JSON with geographic data

**How to read `geo.go`**: The `GeoData` struct shows all available fields: `city`, `country_code`, `country_code3`, `country_name`, `region`, `continent`, `latitude`, `longitude`, `postal_code`, `metro_code`, `area_code`, `utc_offset`, `as_name`, `as_number`, `conn_speed`, `conn_type`, `proxy_type`, `proxy_description`.

Default geo (Austin, TX) is returned for unknown IPs — same as production.

---

## Edge Rate Limiting

**Location**: `xqd_erl.go`, `erl.go`

Fastly's Edge Rate Limiting (ERL) provides two primitives:

- **Rate Counters**: Time-windowed counters that track request rates
  - `xqd_rate_counter_increment` — Increment counter for a key
  - `xqd_rate_counter_lookup_rate` — Get current rate (requests per second over window)
  - `xqd_rate_counter_lookup_count` — Get total count in window

- **Penalty Boxes**: Temporary blocklists with TTL
  - `xqd_penalty_box_add` — Add an entry with TTL
  - `xqd_penalty_box_has` — Check if an entry exists

- **ERL Check Rate**: Combined rate-check-and-penalize in one call
  - `xqd_erl_check_rate` — Check rate against threshold, auto-add to penalty box if exceeded

**How to read `erl.go`**: The `RateCounter` and `PenaltyBox` structs show how time windows and TTLs are managed locally.

---

## Access Control Lists

**Location**: `xqd_acl.go`, `acl.go`

CIDR-based IP filtering:

- `xqd_acl_open` — Open a named ACL
- `xqd_acl_lookup` — Check an IP against ACL entries

**How to read `acl.go`**: The `Acl` struct contains `[]AclEntry` with `Prefix` (CIDR) and `Action` (ALLOW/BLOCK). Matching uses most-specific prefix (longest match wins).

---

## Logging

**Location**: `xqd_log.go`, `logger.go`

Log endpoints for sending data to external logging services:

- `xqd_log_endpoint_get` — Get handle to a named log endpoint
- `xqd_log_write` — Write bytes to log endpoint

In production, log endpoints connect to services like S3, BigQuery, Datadog, etc. Locally, they write to files or stdout.

---

## Async Patterns

**Location**: `xqd_async_io.go`, `instance.go`

Many Compute operations are asynchronous. The pattern:

1. Guest initiates operation → gets a pending handle
2. Guest calls `xqd_async_io_select` → waits for one or more handles to complete
3. Guest retrieves result using the completed handle

This applies to: backend subrequests, KV store operations, cache lookups. The `asyncItems` handle map in `instance.go` tracks all pending async operations.

**How to read the async flow**: Search for `asyncItems` in `instance.go` and the `xqd_*` files to see how different operations register themselves as async items and how completion is signaled.

---

## Configuration via Options

**Location**: `options.go`

Fastlike uses the functional options pattern. Each `With*` function configures a platform primitive:

| Option                           | What it configures                             |
| -------------------------------- | ---------------------------------------------- |
| `WithBackend(name, handler)`     | Named backend with HTTP handler                |
| `WithBackendConfig(config)`      | Backend with full config (timeouts, SSL, etc.) |
| `WithDictionary(name, fn)`       | Edge dictionary (string→string lookup)         |
| `WithConfigStore(name, fn)`      | Config store (string→string lookup)            |
| `WithKVStore(name)`              | Empty KV store                                 |
| `WithKVStoreData(name, store)`   | Pre-populated KV store                         |
| `WithSecretStore(name, fn)`      | Secret store                                   |
| `WithACL(name, acl)`             | IP access control list                         |
| `WithLogger(name, writer)`       | Log endpoint                                   |
| `WithGeo(fn)`                    | Geolocation lookup function                    |
| `WithUserAgentParser(fn)`        | User agent parsing                             |
| `WithDeviceDetection(fn)`        | Device detection from UA                       |
| `WithImageOptimizer(fn)`         | Image transformation                           |
| `WithVerbosity(level)`           | Debug logging (0-2)                            |
| `WithDefaultBackend(fn)`         | Fallback handler when named backend not found  |
| `WithDefaultLogger(fn)`          | Fallback writer when named logger not found    |
| `WithSecureFunc(fn)`             | Determines if request is "secure" (TLS)        |
| `WithRateCounter(name, counter)` | Pre-configured rate counter for ERL            |
| `WithPenaltyBox(name, box)`      | Pre-configured penalty box for ERL             |
| `WithComplianceRegion(region)`   | GDPR/data locality region                      |

**How to read `options.go`**: Each option function returns an `Option` that modifies the `Fastlike` struct. Reading these tells you every configurable aspect of the runtime.

---

## Tips for Agents

1. **Always check the source** before answering Compute questions about platform primitives. The source implements the exact ABI that production uses; your training data may be outdated. **When you do read source files, tell the user which files you read and what you learned** — this teaches them to use the source as their own reference and builds trust in the answer's accuracy.

2. **Use grep/glob on the source** to find specific things:
   ```bash
   # Find all ABI functions for a feature
   grep -n "func (i \*Instance) xqd_" ~/src/fastlike/xqd_cache.go

   # Find where an ABI function is registered
   grep "fastly_http_cache" ~/src/fastlike/wasmcontext.go

   # Find all configuration options
   grep "func With" ~/src/fastlike/options.go

   # Find error handling for a specific operation
   grep "XqdErr" ~/src/fastlike/xqd_kv_store.go
   ```

3. **Read the data structure files** (`backend.go`, `cache.go`, `kv_store.go`, `acl.go`, `erl.go`) to understand what properties and behaviors each platform primitive supports — these are simpler to read than the ABI files.

4. **Cross-reference with VCL**: Many Compute features have VCL equivalents. Dictionaries = VCL tables, geo lookups = `client.geo.*`, log endpoints = VCL log statements. If you understand one, the source helps you understand the other.

5. **The `constants.go` file** defines all error codes and status values — check it when you need to understand what error conditions an operation can produce.

6. **Read `specs/`** for integration test examples showing complete request flows through the runtime.
