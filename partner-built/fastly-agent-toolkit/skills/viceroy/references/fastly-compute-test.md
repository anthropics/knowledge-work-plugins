# Fastly Compute Test Runner

Run Rust unit tests for Fastly Compute applications using Viceroy.

## Setup

### 1. Install Prerequisites

```bash
# Install Viceroy
cargo install --locked viceroy

# Install cargo-nextest (required for test isolation)
cargo install cargo-nextest
```

### 2. Configure Cargo

Add to `.cargo/config.toml`:

```toml
[build]
target = "wasm32-wasip1"

[target.wasm32-wasip1]
runner = "viceroy run -C fastly.toml "
```

## Running Tests

```bash
# Run all tests
cargo nextest run

# Run specific test
cargo nextest run test_name

# Run with verbose output
cargo nextest run -v
```

## Writing Tests

### Basic Test Structure

```rust
#[test]
fn test_request_handling() {
    let client_req = fastly::Request::from_client();
    assert_eq!(client_req.get_method(), Method::GET);
    assert_eq!(client_req.get_path(), "/");
}

#[test]
fn test_body_operations() {
    let mut body = fastly::Body::new();
    body.write_str("hello, world!");
    assert_eq!(body.into_string(), "hello, world!");
}

#[test]
fn test_handler() {
    let req = fastly::Request::get("http://example.com/api");
    let resp = my_handler(req).expect("handler should succeed");
    assert_eq!(resp.get_status(), StatusCode::OK);
}
```

### Testing with Backends

```rust
#[test]
fn test_backend_request() {
    // Requires backend configured in fastly.toml
    let backend_req = fastly::Request::get("http://origin/api")
        .with_header("Host", "origin.example.com");

    let resp = backend_req.send("origin").expect("backend request failed");
    assert!(resp.get_status().is_success());
}
```

### Testing with KV Store

```rust
#[test]
fn test_kv_store() {
    // Requires object_store configured in fastly.toml
    let store = fastly::ObjectStore::open("my_store")
        .expect("store should open");

    store.insert("key", "value").expect("insert should work");
    let value = store.lookup("key").expect("lookup should work");
    assert_eq!(value.into_string(), "value");
}
```

## Command Reference

```bash
viceroy run [OPTIONS] <INPUT> [WASM_ARGS]...
```

### Options

| Option                | Description                         |
| --------------------- | ----------------------------------- |
| `-C, --config <PATH>` | Path to `fastly.toml` configuration |
| `-v`                  | Increase verbosity                  |
| `--adapt`             | Auto-adapt core WASM to components  |
| `[WASM_ARGS]...`      | Arguments passed to the WASM binary |

## Why cargo-nextest?

Standard `cargo test` won't work because:
1. WASM cannot recover from panics (no stack unwinding)
2. A single test failure would halt all remaining tests
3. Each test needs its own isolated WASM instance

cargo-nextest runs each test in a separate process, allowing the test suite to continue even when individual tests fail.

## Troubleshooting

### Tests are extremely slow
Cranelift (the WASM compiler) is very slow in debug mode. Use release mode:
```bash
cargo nextest run --release
```

### Test hangs or times out
Check that all required backends are configured and reachable in your `fastly.toml`.

### "No such store" error
Ensure your KV stores are defined in `fastly.toml`:
```toml
[local_server.object_stores.my_store]
file = "data/store.json"
format = "json"
```

### Import errors
If you see unknown import errors, try:
```bash
viceroy run --unknown-import-behavior trap -C fastly.toml your_test.wasm
```
Note: Programs that require this flag may not be publishable to Fastly.
