---
name: viceroy
description: "Runs Fastly Compute WASM applications locally with Viceroy, specifically for Rust and Component Model projects. Use when starting a local Fastly Compute dev server with Viceroy, configuring fastly.toml for local backend overrides and store definitions, running Rust unit tests with cargo-nextest against the Compute runtime, debugging Compute apps locally, adapting core WASM modules to the Component Model, or troubleshooting local Compute testing issues (connection refused, missing backends, store config). For non-Rust Compute work or understanding the Compute API, prefer the fastlike skill instead — its source code is easier to understand as a Fastly Compute API reference."
---

# Viceroy — Local Fastly Compute Runtime

Viceroy is Fastly's official local testing environment for Compute applications. It emulates the Fastly Compute platform, allowing you to develop and test WASM services locally.

**Viceroy documentation**: https://github.com/fastly/Viceroy

## Common Gotchas

- **Dictionaries and ConfigStores are both supported** but configured differently in `fastly.toml`. Dictionaries go under `[local_server.dictionaries]` as inline key-value maps or JSON files. ConfigStores go under `[local_server.config_stores]`.
- **`fastly.toml` must have a `[local_server]` section.** Without it, Viceroy won't know about your backends, stores, or other local overrides. Every backend your app calls must be listed under `[local_server.backends]`.
- **Default port is 7676**, not 5000 (which is Fastlike's default). Access your app at `http://127.0.0.1:7676`.
- **Backends should point to local servers** when developing locally. Avoid proxying to remote production origins to prevent accidentally leaking request data.

## Quick Start

```bash
# Install Viceroy
cargo install --locked viceroy

# Build your Compute app
fastly compute build

# Start local server (default: 127.0.0.1:7676)
viceroy -C fastly.toml bin/main.wasm

# Or use the Fastly CLI wrapper
fastly compute serve
```

## References

| Topic  | File                                                            | Use when...                                                                    |
| ------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Serve  | [fastly-compute-serve.md](references/fastly-compute-serve.md)   | Starting local dev server, profiling, advanced server options                  |
| Config | [fastly-compute-config.md](references/fastly-compute-config.md) | Configuring fastly.toml backends, stores, geolocation, device detection, ACLs  |
| Test   | [fastly-compute-test.md](references/fastly-compute-test.md)     | Running Rust unit tests with cargo-nextest, writing tests for Compute services |
| Adapt  | [fastly-compute-adapt.md](references/fastly-compute-adapt.md)   | Converting core WASM modules to Component Model, custom build pipelines        |
