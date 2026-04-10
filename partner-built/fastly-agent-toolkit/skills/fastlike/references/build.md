# Build Fastlike

## Prerequisites

- Go 1.23 or later

## Install from Source

```bash
# Clone the repo
git clone https://github.com/avidal/fastlike.git
cd fastlike

# Option 1: Build local binary
make build        # Creates bin/fastlike

# Option 2: Install to GOPATH/bin
make install

# Option 3: Install directly (no clone needed)
go install fastlike.dev/cmd/fastlike@latest
```

## Make Targets

```bash
# Build binary to bin/fastlike
make build

# Install to GOPATH/bin
make install

# Format code
make fmt

# Run linter (golangci-lint or go vet)
make lint

# Tidy dependencies
make tidy

# Run all Go tests
make test

# Run spec tests with default WASM
make test-spec

# Run spec tests with custom WASM
make test-spec-custom WASM=path/to/app.wasm

# Build spec test runner binary
make build-spec-runner

# Build Rust test WASM programs
make build-test-wasm

# Clean build artifacts
make clean

# Show all targets
make help
```

## Build Output

After `make build`:
```
bin/fastlike  # The compiled binary
```

## Development Workflow

```bash
# 1. Make changes to Go code
# 2. Build
make build

# 3. Run with your WASM (uses go run, not the compiled binary)
make run WASM=path/to/app.wasm BACKEND=localhost:8000

# Pass extra flags via ARGS
make run WASM=app.wasm BACKEND=localhost:8000 ARGS='-v 2'
```

## Full Rebuild

```bash
make tidy && make fmt && make lint && make build
```

## Verify Installation

```bash
# After make install
which fastlike  # Should show GOPATH/bin/fastlike
fastlike -help
```
