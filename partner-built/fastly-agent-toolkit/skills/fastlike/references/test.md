# Test Fastlike

## Run All Tests

```bash
go test -v ./...
```

## Spec Tests

Spec tests validate the Fastly Compute ABI contract with guest WASM programs.

```bash
# Run with default WASM
cd specs && go test -v

# Run with custom WASM
cd specs && go test -v -wasm path/to/app.wasm

# Build a reusable spec runner
cd specs && go test -c . -o spec-runner
./spec-runner -test.v -wasm app.wasm
```

## Required Spec Endpoints

Your WASM must implement these endpoints for spec tests. Return 502 for unimplemented endpoints (they will be skipped, not failed).

| Endpoint                           | Expected Behavior                                   |
| ---------------------------------- | --------------------------------------------------- |
| `GET /simple-response`             | Return 200 with body "Hello, world!"                |
| `GET /no-body`                     | Return 204 No Content                               |
| `GET /append-body`                 | Return 200 with body "original\nappended"           |
| `GET /proxy`                       | Forward request to backend, return its response     |
| `GET /append-header`               | Add "test-header: test-value" to backend request    |
| `GET /user-agent`                  | Parse UA, return formatted like "Firefox 76.1.15"   |
| `GET /geo`                         | Geo lookup on client IP, return JSON with `as_name` |
| `GET /log`                         | Write to "default" log endpoint, return 204         |
| `GET /dictionary/testdict/testkey` | Look up "testkey" in "testdict", return value       |
| `GET /panic!`                      | Trigger wasm trap (tests error handling)            |

See `specs/README.md` for the reference Rust implementation.

## Test Patterns

Tests use `t.Parallel()` for concurrent execution. Follow this pattern for new tests:

```go
func TestSomething(t *testing.T) {
    t.Parallel()
    // test implementation
}
```

## Common Test Issues

**Backend not reachable:** Ensure your test backend is running before running proxy tests.

**WASM not found:** Check the `-wasm` path is correct and the file exists.

**Handle leaks:** Tests should clean up handles properly. Check for unclosed bodies.
