# Fastly Compute Local Server

Start a local testing server for Fastly Compute services using Viceroy.

**Viceroy documentation**: https://github.com/fastly/Viceroy

## Quick Start

```bash
# Start server with default settings (127.0.0.1:7676)
viceroy bin/main.wasm

# Start with configuration file
viceroy -C fastly.toml bin/main.wasm

# Start on a custom address
viceroy --addr 0.0.0.0:8080 bin/main.wasm
```

## Command Reference

```bash
viceroy serve [OPTIONS] <WASM_FILE>
```

### Required Arguments

- `<WASM_FILE>` - Path to the compiled WASM binary (usually `bin/main.wasm` after `fastly compute build`)

### Common Options

| Option                | Description                                                     |
| --------------------- | --------------------------------------------------------------- |
| `-C, --config <PATH>` | Path to `fastly.toml` configuration file                        |
| `--addr <ADDR>`       | IP address and port to bind (default: `127.0.0.1:7676`)         |
| `--log-stdout`        | Treat stdout as a logging endpoint                              |
| `--log-stderr`        | Treat stderr as a logging endpoint                              |
| `-v`                  | Increase verbosity (`-v` = INFO, `-vv` = DEBUG, `-vvv` = TRACE) |
| `--adapt`             | Auto-adapt core WASM modules to components                      |

### Profiling Options

| Option                            | Description                                                      |
| --------------------------------- | ---------------------------------------------------------------- |
| `--profile=jitdump`               | Enable JIT dump profiling (for `perf`)                           |
| `--profile=perfmap`               | Enable perf map profiling                                        |
| `--profile=vtune`                 | Enable VTune profiling                                           |
| `--profile=guest`                 | Enable guest profiling (output to `guest-profiles/`)             |
| `--profile=guest,<path>`          | Guest profiling with custom output path                          |
| `--profile=guest,<path>,<sample>` | Guest profiling with custom sample period (e.g., `250ns`, `1ms`) |

### Advanced Options

| Option                              | Description                                              |
| ----------------------------------- | -------------------------------------------------------- |
| `--experimental_modules wasi-nn`    | Enable experimental WASI-NN module                       |
| `--unknown-import-behavior <MODE>`  | Handle unknown imports: `link-error` (default) or `trap` |
| `--local-pushpin-proxy-port <PORT>` | Enable Pushpin real-time messaging support               |

## Testing the Server

Once running, test with curl:

```bash
# Simple GET request
curl http://127.0.0.1:7676/

# POST with body
curl -X POST -d '{"key": "value"}' http://127.0.0.1:7676/api

# With custom headers
curl -H "X-Custom-Header: value" http://127.0.0.1:7676/
```

## Stopping the Server

Press `Ctrl+C` to gracefully stop the server.

## Troubleshooting

### Backend not responding
The server checks backend health on startup. If you see warnings like:
```
WARN backend 'origin' on 'http://localhost:8000' is not up right now
```
Ensure your backend server is running before starting Viceroy.

### No configuration warning
```
WARN no configuration provided, invoke with `-C <TOML_FILE>` to provide a configuration
```
This means Viceroy is running without backends, dictionaries, or other services. Create a `fastly.toml` file to configure these.

### Slow execution
If tests run slowly, the WASM may be compiled in debug mode. Ensure you're using release builds:
```bash
fastly compute build --release
```
