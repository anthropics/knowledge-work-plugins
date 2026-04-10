# Fastly Compute Development

Build and deploy serverless applications at the edge using Fastly Compute.

## Quick Reference

| Command                   | Purpose                               |
| ------------------------- | ------------------------------------- |
| `fastly compute init`     | Create new Compute project            |
| `fastly compute build`    | Compile to WebAssembly                |
| `fastly compute deploy`   | Deploy package to service             |
| `fastly compute publish`  | Build + deploy in one step            |
| `fastly compute serve`    | Local development server              |
| `fastly compute metadata` | Control metadata collection           |
| `fastly compute update`   | Update a package on a service version |
| `fastly compute acl`      | Manage Compute ACLs                   |

## Initialize a New Project

```bash
# Interactive project creation
fastly compute init

# Non-interactive with defaults
fastly compute init --accept-defaults

# From starter kit or template
fastly compute init -f https://github.com/fastly/compute-starter-kit-rust-default

# From existing service
fastly compute init --from SERVICE_ID

# Specify language
fastly compute init -l rust
fastly compute init --language javascript
fastly compute init --language go

# Specify project directory
fastly compute init -p /path/to/project

# Specify author
fastly compute init -a "developer@example.com"
```

**Supported languages**: rust, javascript, go, other

**Key flags**:
- `-p, --directory` - Destination directory for the new project
- `-f, --from` - Git repository URL, local path, archive URL, or service ID
- `-l, --language` - Language for the project
- `-a, --author` - Author string for the project

The `--from` flag accepts:
- Git repository URLs
- Local directory paths
- URLs to .zip/.tar.gz archives
- Existing Fastly service IDs

## Build a Package

```bash
# Standard build
fastly compute build

# Build from different directory
fastly compute build -C /path/to/project

# With environment-specific manifest
fastly compute build --env stage  # Uses fastly.stage.toml

# Include source code in the package
fastly compute build --include-source

# Show what metadata would be collected
fastly compute build --metadata-show

# Disable metadata collection for this build
fastly compute build --metadata-disable

# Filter environment variables from metadata
fastly compute build --metadata-filter-envvars "SECRET_*,TOKEN_*"

# Specify a custom package name
fastly compute build --package-name my-app

# Set a build timeout
fastly compute build --timeout 300
```

**Key flags**:
- `-C, --dir` - Project directory to build from
- `--include-source` - Include source code in the package
- `--metadata-disable` - Disable metadata collection
- `--metadata-filter-envvars` - Filter environment variables from metadata
- `--metadata-show` - Show what metadata would be collected
- `--package-name` - Custom package name
- `--timeout` - Build timeout in seconds

Build output: `pkg/<project-name>.tar.gz`

## Deploy a Package

```bash
# Deploy (creates service if needed)
fastly compute deploy

# Deploy to specific service
fastly compute deploy --service-id SERVICE_ID
fastly compute deploy --service-name "My Service"

# Deploy specific package
fastly compute deploy --package pkg/myapp.tar.gz

# Deploy with custom domain
fastly compute deploy --domain myapp.edgecompute.app

# Deploy without assigning a default domain
fastly compute deploy --no-default-domain

# Deploy from a specific project directory
fastly compute deploy -C /path/to/project

# Skip status check after deploy
fastly compute deploy --status-check-off

# Set expected status code for health check
fastly compute deploy --status-check-code 200 --status-check-path /health
```

**Key flags**:
- `-C, --dir` - Project directory
- `--no-default-domain` - Do not assign a default domain to the service

## Publish (Build + Deploy)

```bash
# Build and deploy in one command
fastly compute publish

# With options
fastly compute publish --service-id SERVICE_ID --comment "Release v1.0"

# Publish without a default domain
fastly compute publish --no-default-domain

# Publish with a build timeout
fastly compute publish --timeout 300
```

**Key flags**:
- `--no-default-domain` - Do not assign a default domain to the service
- `--timeout` - Build timeout in seconds

## Local Development Server

```bash
# Start local server (uses Viceroy)
fastly compute serve

# Custom port and address
fastly compute serve --addr 127.0.0.1:7676

# Watch for changes and rebuild
fastly compute serve --watch

# Watch a specific directory
fastly compute serve --watch --watch-dir src/

# Use specific manifest environment
fastly compute serve --env staging

# Run a specific Wasm file directly (skips build)
fastly compute serve --file path/to/app.wasm

# Skip the build step
fastly compute serve --skip-build

# Enable Pushpin for Fanout local testing
fastly compute serve --experimental-enable-pushpin

# Profile the Wasm guest under Viceroy
fastly compute serve --profile-guest --profile-guest-dir ./profiles

# Use a specific Viceroy binary
fastly compute serve --viceroy-path /usr/local/bin/viceroy

# Force a check for newer Viceroy versions
fastly compute serve --viceroy-check

# Pass additional arguments to Viceroy
fastly compute serve --viceroy-args "--log-level=debug"
```

**Key flags**:
- `--file=FILE` - Run a specific Wasm file (skips build)
- `--skip-build` - Skip the build step
- `--watch-dir` - Directory to watch for changes (can be relative or absolute)
- `--experimental-enable-pushpin` - Enable Pushpin for Fanout local testing
- `--pushpin-path` - Path to Pushpin binary
- `--pushpin-proxy-port` - Pushpin proxy port
- `--pushpin-publish-port` - Pushpin publish port
- `--profile-guest` - Profile the Wasm guest under Viceroy
- `--profile-guest-dir` - Directory for per-request profiles
- `--viceroy-args` - Additional arguments passed to Viceroy
- `--viceroy-check` - Force check for a newer Viceroy version
- `--viceroy-path` - Path to a user-installed Viceroy binary

The local server uses Viceroy to emulate the Fastly Compute environment.

## Update a Package on a Service Version

```bash
# Update the package on a specific version
fastly compute update --version=VERSION

# Update with service identification
fastly compute update --version=VERSION --service-id SERVICE_ID
fastly compute update --version=VERSION --service-name "My Service"

# Autoclone the version before updating
fastly compute update --version=VERSION --autoclone

# Specify a package file
fastly compute update --version=VERSION --package pkg/myapp.tar.gz
```

**Key flags**:
- `--version=VERSION` - Service version to update (required)
- `--service-id` - Service ID
- `--service-name` - Service name
- `--autoclone` - Clone the version before updating if it is active or locked
- `--package` - Path to the package to upload

## Metadata Control

```bash
# Disable all metadata collection
fastly compute metadata --disable

# Re-enable all metadata collection
fastly compute metadata --enable

# Disable specific metadata categories
fastly compute metadata --disable-build
fastly compute metadata --disable-machine
fastly compute metadata --disable-package
fastly compute metadata --disable-script

# Re-enable specific metadata categories
fastly compute metadata --enable-build
fastly compute metadata --enable-machine
fastly compute metadata --enable-package
fastly compute metadata --enable-script
```

**Key flags**:
- `--disable` / `--enable` - Disable or enable all metadata collection
- `--disable-build` / `--enable-build` - Control build metadata
- `--disable-machine` / `--enable-machine` - Control machine metadata
- `--disable-package` / `--enable-package` - Control package metadata
- `--disable-script` / `--enable-script` - Control script metadata

## Compute ACLs

Manage ACLs for Compute services. These are distinct from service-level ACLs managed via `fastly service acl`.

```bash
# Create an ACL
fastly compute acl create --name=my-blocklist --json

# List all ACLs
fastly compute acl list-acls --json

# Describe an ACL
fastly compute acl describe --acl-id=ACL-ID --json

# Update ACL entries
fastly compute acl update --acl-id=ACL-ID --operation=create --prefix=192.168.0.0/16 --action=BLOCK
fastly compute acl update --acl-id=ACL-ID --file=entries.json

# Look up an IP address in an ACL
fastly compute acl lookup --acl-id=ACL-ID --ip=192.168.1.1 --json

# List entries in an ACL
fastly compute acl list-entries --acl-id=ACL-ID --limit=50 --json

# Delete an ACL
fastly compute acl delete --acl-id=ACL-ID --json
```

**Subcommands**:
- `create` - Create a new Compute ACL (`--name=NAME`, `--json`)
- `list-acls` - List all Compute ACLs (`--json`)
- `describe` - Describe a Compute ACL (`--acl-id=ACL-ID`, `--json`)
- `update` - Update entries in a Compute ACL (`--acl-id=ACL-ID`, `--file`, `--operation`, `--prefix`, `--action`)
- `lookup` - Look up an IP address in a Compute ACL (`--acl-id=ACL-ID`, `--ip=IP`, `--json`)
- `delete` - Delete a Compute ACL (`--acl-id=ACL-ID`, `--json`)
- `list-entries` - List entries in a Compute ACL (`--acl-id=ACL-ID`, `--cursor`, `--limit=50`, `--json`)

## Package Management

```bash
# Validate package
fastly compute validate

# Pack pre-compiled Wasm binary
fastly compute pack --wasm-binary main.wasm

# Generate file hashes
fastly compute hash-files
```

## Project Configuration (fastly.toml)

```toml
manifest_version = 3
name = "my-compute-app"
description = "My edge application"
authors = ["developer@example.com"]
language = "rust"
service_id = "YOUR_SERVICE_ID"

[scripts]
build = "cargo build --release --target wasm32-wasi"
post_init = "npm install"

[setup]
  [setup.backends]
    [setup.backends.origin]
    address = "origin.example.com"
    port = 443

  [setup.config_stores]
    [setup.config_stores.settings]
    description = "Application settings"

  [setup.kv_stores]
    [setup.kv_stores.cache]
    description = "Edge cache"
```

## Common Workflows

### New Rust Project
```bash
fastly compute init --language rust
fastly compute build
fastly compute serve  # Test locally
fastly compute publish
```

### New JavaScript Project
```bash
fastly compute init --language javascript
npm install
fastly compute build
fastly compute serve
fastly compute publish
```

### Deploy to Staging vs Production
```bash
# Create environment-specific manifests
# fastly.toml (production)
# fastly.stage.toml (staging)

# Deploy to staging
fastly compute deploy --env stage

# Deploy to production
fastly compute deploy
```

### Clone and Modify Existing Service
```bash
fastly compute init --from EXISTING_SERVICE_ID
# Make changes
fastly compute publish
```

## Propagation Delays

After deploying a Compute package, changes can take up to 10 minutes to propagate globally. The CLI performs a status check by default, but automation scripts should implement additional verification with retries if needed. Use `--status-check-timeout` to extend the post-deploy verification period.

## Troubleshooting

**Build fails**: Ensure language toolchain is installed (Rust, Node.js, or Go)

**Package too large**: Maximum size is 100MB compressed. Optimize dependencies.

**Service not available after deploy**: Wait for global propagation (usually < 60 seconds). Use `--status-check-timeout` to extend wait time.

**Viceroy not found**: Viceroy is automatically installed on first `fastly compute serve` run
