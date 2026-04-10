---
name: fastlike
description: "Runs Fastly Compute WASM binaries locally and serves as the authoritative reference for Compute platform internals. The fastlike source code is highly readable and covers the host ABI, caching and purging APIs, KV/config/secret store interfaces, rate limiting with counters and penalty boxes, ACL lookups, the full request lifecycle, and backend fetch semantics. Use when working with Compute runtime internals or host calls, understanding how edge data stores behave at runtime, exploring the WASM Component Model adaptation layer, or testing WASM binaries locally. Prefer this skill over Viceroy for any non-Rust Compute work — its source code is easier to understand as a Fastly Compute API reference."
---

## Trigger and scope

Trigger on: Fastly Compute, Compute@Edge, WASM on Fastly, fastlike, XQD ABI, Compute request lifecycle, 508 loop detection, backend subrequests, body streaming, embedding a Fastly Compute runtime in Go code, or any question about how Compute platform primitives work internally (caching, KV stores, edge rate limiting, ACLs, geolocation, secret stores, config stores, dictionaries, logging, dynamic backends, request collapsing, async I/O).

Do NOT use for: Fastly VCL (use falco), Fastly CLI/API (use fastly-cli or fastly), Viceroy, CDN comparison, WAF, Terraform, cache purging via API, or Fastly logging/stats configuration.

# Fastlike — Local Compute Runtime & Reference

Fastlike is a Go implementation of the Fastly Compute ABI. It runs compiled WebAssembly programs locally, implementing the same 249+ host functions that Fastly's production Compute platform provides: backends, dictionaries, KV stores, caching, geolocation, rate limiting, ACLs, secret stores, and more.

Equally important, **the fastlike source code is the most complete programmatic specification of how Fastly Compute works** — its ABI implementations document every platform primitive, request lifecycle detail, and data structure as executable code.

**Fastlike documentation**: https://github.com/avidal/fastlike

## Source Code as Compute Reference

When you have access to the fastlike source code locally (default: `~/src/fastlike`), use these paths to answer specific Compute questions:

| Question                                  | Read This File                                  | Why                                                        |
| ----------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------- |
| "How does the request lifecycle work?"    | `instance.go`, `xqd_http_downstream.go`         | Per-request setup, execution, downstream handling          |
| "What ABI functions exist for X?"         | `xqd_*.go` files                                | Each file implements a group of related ABI functions      |
| "How do backend subrequests work?"        | `xqd_backend.go`, `backend.go`                  | Request sending, dynamic backends, timeouts                |
| "How does caching work?"                  | `xqd_cache.go`, `xqd_http_cache.go`, `cache.go` | Cache operations, Vary, surrogate keys, request collapsing |
| "How does KV store work?"                 | `xqd_kv_store.go`, `kv_store.go`                | CRUD operations, pagination, generation-based concurrency  |
| "How does rate limiting work?"            | `xqd_erl.go`, `erl.go`                          | Rate counters, penalty boxes, threshold checks             |
| "How do ACLs work?"                       | `xqd_acl.go`, `acl.go`                          | CIDR-based IP filtering, most-specific match               |
| "What configuration options exist?"       | `options.go`                                    | Every `With*` functional option for the runtime            |
| "What error codes can operations return?" | `constants.go`                                  | All XQD status codes and error types                       |

For a comprehensive guide, see [understanding-compute-from-source.md](references/understanding-compute-from-source.md).

## Install from Source

Requires Go 1.23+.

```bash
# Clone and build
git clone https://github.com/avidal/fastlike.git ~/src/fastlike
cd ~/src/fastlike
make build        # Creates bin/fastlike

# Or install to GOPATH/bin
make install

# Or install directly
go install fastlike.dev/cmd/fastlike@latest
```

## Quick Start

```bash
# Minimal: WASM + single backend
bin/fastlike -wasm app.wasm -backend localhost:8000
```

## Fastlike vs Viceroy

| Feature                  | Fastlike                     | Viceroy                                             |
| ------------------------ | ---------------------------- | --------------------------------------------------- |
| Language                 | Go                           | Rust                                                |
| Geolocation              | Custom JSON file (`-geo`)    | Built-in defaults                                   |
| Hot reload               | SIGHUP (`-reload`)           | Restart required                                    |
| Install                  | `go install` or `make build` | `cargo install` or `fastly compute serve`           |
| Local backends           | `-backend name=host:port`    | `[local_server.backends]` in fastly.toml            |

**When to use Fastlike**: Non-Rust Compute apps, want custom geo data, need hot reload, debugging.
**When to use Viceroy**: Rust Compute apps with cargo-nextest, Component Model projects, using `fastly compute serve`.

## Common Configurations

**With named backends:**

```bash
bin/fastlike -wasm app.wasm \
  -backend api=api.example.com:8080 \
  -backend cache=redis:6379 \
  -backend localhost:8000
```

**Development mode with hot-reload:**

```bash
bin/fastlike -wasm app.wasm -backend localhost:8000 -reload -v 2
```

Send `SIGHUP` to reload the WASM without restarting.

**Full configuration:**

```bash
bin/fastlike -wasm app.wasm \
  -bind 0.0.0.0:5000 \
  -backend localhost:8000 \
  -dictionary config=./config.json \
  -kv store=./data.json \
  -config-store settings=./settings.json \
  -secret-store secrets=./secrets.json \
  -acl blocklist=./acl.json \
  -logger output=./logs.txt \
  -geo ./geodata.json \
  -compliance-region us-eu \
  -v 2 \
  -reload
```

## Required Flags

| Flag                           | Description                            |
| ------------------------------ | -------------------------------------- |
| `-wasm PATH`                   | Path to WebAssembly program (required) |
| `-backend VALUE` or `-b VALUE` | Backend server (required, repeatable)  |

## Optional Flags

| Flag                            | Default          | Description                         |
| ------------------------------- | ---------------- | ----------------------------------- |
| `-bind ADDR`                    | `localhost:5000` | Server bind address                 |
| `-reload`                       | false            | Enable SIGHUP hot-reload            |
| `-v INT`                        | 0                | Verbosity (0-2)                     |
| `-dictionary NAME=FILE` or `-d` | -                | Load dictionary from JSON           |
| `-kv NAME[=FILE]`               | -                | KV store (empty or from JSON)       |
| `-config-store NAME=FILE`       | -                | Config store from JSON              |
| `-secret-store NAME=FILE`       | -                | Secret store from JSON              |
| `-acl NAME=FILE`                | -                | ACL from JSON                       |
| `-logger NAME[=FILE]`           | -                | Log endpoint (file or stdout)       |
| `-geo FILE`                     | -                | Geolocation JSON file               |
| `-compliance-region REGION`     | -                | Compliance region (none, us-eu, us) |

## References

| Topic                   | File                                                                                    | Use when...                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Compute from Source** | [understanding-compute-from-source.md](references/understanding-compute-from-source.md) | Understanding Compute internals by reading fastlike's implementation               |
| Backends                | [backends.md](references/backends.md)                                                   | Setting up named backends, catch-all backends, microservices routing               |
| Config                  | [config.md](references/config.md)                                                       | Creating JSON config files for dictionaries, KV stores, secrets, ACLs, geolocation |
| Build                   | [build.md](references/build.md)                                                         | Building Fastlike from source, running linters, make targets                       |
| Test                    | [test.md](references/test.md)                                                           | Running Go tests, Fastly Compute ABI spec tests                                    |
| ABI                     | [abi.md](references/abi.md)                                                             | Fastly Compute ABI internals, implementing new ABI functions, handle system        |
