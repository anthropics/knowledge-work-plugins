# Fastly Compute ABI Implementation Guide

Fastlike implements the Fastly Compute ABI, allowing WebAssembly programs to run locally.

## Architecture Layers

| Layer         | File             | Purpose                                               |
| ------------- | ---------------- | ----------------------------------------------------- |
| Entry Point   | `fastlike.go`    | http.Handler, manages instance pool (min(NumCPU, 16)) |
| WASM Context  | `wasmcontext.go` | Compiled WASM module, engine, linker (shared)         |
| Instance      | `instance.go`    | Per-request: store, memory, handles, state            |
| ABI Functions | `xqd_*.go`       | C-style signatures, guest memory I/O                  |

## Key Files

| File             | Purpose                                     |
| ---------------- | ------------------------------------------- |
| `fastlike.go`    | Entry point, instance pooling, http.Handler |
| `instance.go`    | Per-request state, handle management        |
| `wasmcontext.go` | Compiled WASM, engine, linker setup         |
| `memory.go`      | Guest memory read/write wrapper             |
| `options.go`     | Functional options pattern                  |
| `xqd_*.go`       | ABI function implementations                |

## Handle System

Resources are tracked via handles (int32 IDs). Handle types in `instance.go`:

- `requests` / `responses` - HTTP request/response pairs
- `bodies` - Streaming bodies
- `pendingRequests` / `requestPromises` - Async subrequests
- `kvStores` - KV store references
- `kvLookups` / `kvInserts` / `kvDeletes` / `kvLists` - Async KV operations
- `secretStoreHandles` / `secretHandles` - Secret store operations
- `cacheHandles` / `cacheBusyHandles` / `cacheReplaceHandles` - Cache operations
- `aclHandles` - ACL lookups
- `asyncItems` - Generic async I/O

## ABI Function Pattern

ABI functions follow C-style signatures (not idiomatic Go) for comparison with Fastly's Rust crate:

```go
// xqd_body.go
func (i *Instance) xqd_body_new(body_handle_out int32) int32 {
    // 1. Read input from guest memory (if any)
    // 2. Perform operation
    // 3. Write output to guest memory
    // 4. Return status code

    handle := i.bodies.New(bytes.NewBuffer(nil))
    i.memory.PutUint32(uint32(handle), int64(body_handle_out))
    return XqdStatusOK
}
```

## Error Codes

From `constants.go`:

| Constant                  | Value | Description                            |
| ------------------------- | ----- | -------------------------------------- |
| `XqdStatusOK`             | 0     | Success                                |
| `XqdError`                | 1     | Generic error                          |
| `XqdErrInvalidArgument`   | 2     | Invalid argument                       |
| `XqdErrInvalidHandle`     | 3     | Invalid handle ID                      |
| `XqdErrBufferLength`      | 4     | Buffer too small                       |
| `XqdErrUnsupported`       | 5     | Operation not supported                |
| `XqdErrBadAlignment`      | 6     | Misaligned pointer                     |
| `XqdErrHttpParse`         | 7     | HTTP parsing error                     |
| `XqdErrHttpUserInvalid`   | 8     | Invalid HTTP user input                |
| `XqdErrHttpIncomplete`    | 9     | Incomplete HTTP message                |
| `XqdErrNone`              | 10    | No value/data available (not an error) |
| `XqdErrHttpHeadTooLarge`  | 11    | HTTP header too large                  |
| `XqdErrHttpInvalidStatus` | 12    | Invalid HTTP status code               |
| `XqdErrLimitExceeded`     | 13    | Resource limit exceeded                |
| `XqdErrAgain`             | 14    | Operation would block (try again)      |

## Request Flow

1. **Setup**: Fresh store created, WASM instantiated
2. **Execute**: `_start` function called
3. **Guest Code**: Makes ABI calls (body read, backend request, etc.)
4. **Reset**: Handles closed, bodies cleaned up
5. **Reuse**: Instance returned to pool

## Adding New ABI Functions

1. Add function in appropriate `xqd_*.go` file
2. Register with linker in `wasmcontext.go`
3. Follow C-style signature conventions
4. Use `i.memory` for guest memory access
5. Return appropriate status code
6. Add tests in `*_test.go`

## Memory Access

Use the `Memory` wrapper (`memory.go`):

```go
// Read typed values from guest
val := i.memory.Uint32(offset)     // int64 offset
val := i.memory.Uint64(offset)     // int64 offset
val := i.memory.ReadUint32(offset) // int32 offset
val := i.memory.ReadUint64(offset) // int32 offset

// Write typed values to guest
i.memory.PutUint32(value, offset)  // uint32, int64 offset
i.memory.PutUint64(value, offset)  // uint64, int64 offset
i.memory.PutInt32(value, offset)   // int32, int64 offset

// Read/write raw bytes (implements io.ReaderAt/io.WriterAt)
n, err := i.memory.ReadAt(buf, offset)   // []byte, int64 offset
n, err := i.memory.WriteAt(data, offset) // []byte, int64 offset
```

## Testing Patterns

```go
func TestSomething(t *testing.T) {
    t.Parallel()

    // Create test instance with options
    fl := fastlike.New(wasmPath,
        fastlike.WithBackend("test", handler),
    )

    // Make request
    req := httptest.NewRequest("GET", "/", nil)
    rec := httptest.NewRecorder()
    fl.ServeHTTP(rec, req)

    // Assert
    assert.Equal(t, 200, rec.Code)
}
```
