# Simulating VCL with Falco

## Quick start

```bash
# Start simulator on default port 3124
falco simulate /path/to/main.vcl


# With include paths
falco simulate -I ./vcl /path/to/main.vcl

# Enable proxy mode (forward to real backends)
falco simulate --proxy /path/to/main.vcl

# With TLS
falco simulate --cert server.crt --key server.key /path/to/main.vcl
```

## Key flags

| Flag                 | Description                   |
| -------------------- | ----------------------------- |
| `-I, --include_path` | Add include path (repeatable) |
| `-p, --port`         | Listen port (default: 3124)   |
| `--proxy`            | Enable actual proxy behavior  |
| `-debug`             | Enable interactive debugger   |
| `--cert`             | TLS certificate file          |
| `--key`              | TLS key file                  |
| `--max_backends`     | Override backend limit        |
| `--max_acls`         | Override ACL limit            |
| `-request`           | Path to request config file   |

## Testing the simulator

```bash
# Start simulator
falco simulate -I ./vcl ./vcl/main.vcl &

# Send test request
curl -v http://localhost:3124/test-path \
  -H "Host: example.com" \
  -H "X-Custom-Header: value"

# Stop simulator
kill %1
```

## Debug mode

Interactive debugger for step-by-step VCL execution:

```bash
falco simulate -debug /path/to/main.vcl
```

Debugger commands:
- Set breakpoints
- Step through VCL execution
- Inspect variables
- View call stack

## Configuration file

In `.falco.yaml`:

```yaml
simulator:
  port: 3124
  key_file: ./certs/server.key
  cert_file: ./certs/server.crt

edge_dictionary:
  config:
    environment: "development"
    feature_x: "enabled"

override_backends:
  origin:
    host: "localhost:8000"
    ssl: false
```

## Request configuration

Create a request config file (JSON or YAML):

```yaml
# request.yaml
remote_ip: "192.168.1.100"
path: "/api/v1/users"
headers:
  Host: "api.example.com"
  Authorization: "Bearer token"
  User-Agent: "TestClient/1.0"
```

Use with: `falco simulate -request request.yaml main.vcl`

## Proxy mode (real backend requests)

By default, the simulator does not make actual HTTP requests to backends. Use `--proxy` to enable real backend requests:

```bash
falco simulate --proxy /path/to/main.vcl
```

This is essential for:
- Testing dynamic backends that require health check probes
- End-to-end testing with real origin servers
- Validating backend response handling

Override backend addresses for local testing in `.falco.yaml`:

```yaml
override_backends:
  origin:
    host: "localhost:8000"
    ssl: false
  api:
    host: "localhost:3000"
    ssl: false
```

Then run with proxy mode:
```bash
falco simulate --proxy -I ./vcl ./vcl/main.vcl
```

## Common patterns

**Development server:**
```bash
falco simulate -I ./vcl ./vcl/main.vcl
```

**End-to-end with real backends:**
```bash
falco simulate --proxy -I ./vcl ./vcl/main.vcl
```
