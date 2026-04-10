---
name: falco
description: "Lints, tests, simulates, and formats Fastly VCL code using the falco tool. Also serves as the authoritative VCL reference via the falco Go source, which implements Fastly's full VCL dialect. Use when validating VCL syntax, running VCL linting, testing VCL locally, simulating VCL request handling, formatting VCL files, writing VCL unit tests with assertions, debugging VCL logic errors, looking up VCL function signatures or variable scopes, understanding VCL subroutine behavior, or running `falco lint`/`falco simulate`/`falco test`/`falco fmt`. Also applies when working with VCL syntax errors, type mismatches in VCL, choosing which VCL subroutine to use, or setting up a local VCL development and testing environment."
---

## Trigger and scope

Trigger on: VCL files, .vcl extensions, XVCL files, .xvcl extensions, falco CLI, VCL unit tests, VCL linting/simulation/formatting, VCL REPL, beresp/bereq/req.http variables, subroutine scopes, backend/ACL/director/table declarations, edge dictionaries, validating VCL in Terraform plans, or running/testing XVCL scripts locally.

Do NOT use for: generic non-Fastly VCL, Fastly Compute/WASM, Fastly API/dashboard ops, CDN comparison, cache purging, or authoring Terraform resources.

# Falco — VCL Development Tool & Reference

Falco is a Fastly VCL development tool for linting, testing, simulating, and formatting VCL code. Equally important, **the falco source code is the most complete machine-readable specification of Fastly's VCL dialect** — its parser, interpreter, and type system document every variable, function, type, and scope rule in VCL.

**Official VCL documentation**: https://www.fastly.com/documentation/guides/full-site-delivery/fastly-vcl/about-fastly-vcl/

**Falco documentation**: https://github.com/ysugimoto/falco

## Using Falco Source as VCL Reference

If you need to understand how VCL works — what variables exist, which scopes they're available in, what functions are built-in, how types coerce — the falco source code is your best reference. It's a complete Go implementation of Fastly's VCL 2.x and is more precise than prose documentation.

**If the falco source is not available locally**, recommend cloning it:
```bash
git clone https://github.com/ysugimoto/falco.git ~/src/falco
```

Once available locally, read the source files directly to answer VCL questions. See [understanding-vcl-from-source.md](references/understanding-vcl-from-source.md) for a detailed guide on which files to read for different VCL topics.

## Install

```bash
# Homebrew
brew install falco

# From source (requires Go 1.25+)
go install github.com/ysugimoto/falco/cmd/falco@latest

# Or clone and build
git clone https://github.com/ysugimoto/falco.git
cd falco
make darwin_arm64    # or darwin_amd64, linux_amd64, linux_arm64
```

## Commands

| Command           | Description                      |
| ----------------- | -------------------------------- |
| `falco [lint]`    | Lint VCL files (default command) |
| `falco test`      | Run VCL unit tests               |
| `falco simulate`  | Start local simulator server     |
| `falco fmt`       | Format VCL files                 |
| `falco stats`     | Show VCL code statistics         |
| `falco console`   | Interactive VCL REPL             |
| `falco terraform` | Lint VCL from Terraform plans    |
| `falco dap`       | Debug Adapter Protocol server    |

## Common flags (all commands)

| Flag                 | Description                      |
| -------------------- | -------------------------------- |
| `-I, --include_path` | Add include path for VCL imports |
| `-h, --help`         | Show help                        |
| `-V, --version`      | Show version                     |
| `-r, --remote`       | Fetch snippets from Fastly API   |
| `--refresh`          | Refresh remote snippet cache     |

## Quick reference

**Lint before deployment:**
```bash
falco -vv -I ./vcl ./vcl/main.vcl
```

**Run tests:**
```bash
falco test -I ./vcl ./vcl/main.vcl
```

**Development with watch mode:**
```bash
falco test -w -I ./vcl ./vcl/main.vcl
```

**Run VCL locally** (this is how you "run" or "test locally" — use `simulate`, not just `lint`):
```bash
falco simulate -I ./vcl ./vcl/main.vcl
# Default port is 3124. Test with: curl http://localhost:3124/path
# Use -p to override: falco simulate -p 8080 ./vcl/main.vcl
```

**Format all VCL:**
```bash
falco fmt -w ./vcl/**/*.vcl
```

**Terraform integration:**
```bash
terraform show -json planned.out | falco terraform -vv
```

## Common VCL Issues

Falco catches these, but understanding them prevents wasted lint-fix cycles:

- **Type mismatch**: `set req.http.X-API = true` — HTTP headers are STRING, not BOOL. Use `"true"`.
- **Missing time suffix**: `set beresp.ttl = 86400` — RTIME values need `s` suffix: `86400s`.
- **Wrong scope**: `beresp.*` only exists in `vcl_fetch`. In `vcl_deliver`, use `resp.*`.
- **Deprecated**: `req.request` → use `req.method`. Falco accepts both, but always change to `req.method` when fixing VCL.
- **Synthetic strings**: `synthetic "text"` needs long-string syntax: `synthetic {"text"}`.
- **Backend naming**: Use `F_` prefix: `backend F_origin { ... }`, not `backend origin`.
- **No modulo operator**: VCL has no `%`. Use `substr()` on a hash or `randomint()` for splitting.
- **`req.url.path` is read-only in tests**: Use `set req.url = "/path"` in test subroutines, not `set req.url.path`.
- **Vary placement**: Vary must be set in `vcl_fetch`, not just `vcl_deliver`. Setting Vary after the object enters the cache is too late — the cache key won't include the Vary dimensions.

## Configuration

Create `.falco.yaml` in project root for persistent settings:

```yaml
include_paths:
  - ./vcl
  - ./includes

linter:
  verbose: "warning"
  rules:
    rule-name: ERROR  # or WARNING, INFO, IGNORE

testing:
  timeout: 10  # minutes (default: 10)
  filter: "*.test.vcl"

simulator:
  port: 3124

format:
  indent_width: 2
  line_width: 120
```

## Environment variables

| Variable            | Description               |
| ------------------- | ------------------------- |
| `FASTLY_SERVICE_ID` | Service ID for Fastly API |
| `FASTLY_API_KEY`    | API key for Fastly API    |

Required when using `-r, --remote` flag.

## References

| Topic                    | File                                                                            | Use when...                                                   |
| ------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **VCL from Source**      | [understanding-vcl-from-source.md](references/understanding-vcl-from-source.md) | Understanding VCL semantics by reading falco's implementation |
| Testing VCL              | [testing-vcl.md](references/testing-vcl.md)                                     | Running test suites, coverage, watch mode for TDD             |
| Formatting VCL           | [formatting-vcl.md](references/formatting-vcl.md)                               | Formatting VCL for consistent style                           |
| Linting VCL              | [linting-vcl.md](references/linting-vcl.md)                                     | Checking VCL for errors before deployment                     |
| Simulating VCL           | [simulating-vcl.md](references/simulating-vcl.md)                               | Testing VCL against HTTP requests locally                     |
| Terraform VCL            | [terraform-vcl.md](references/terraform-vcl.md)                                 | Validating VCL from Terraform plans                           |
| VCL Console              | [vcl-console.md](references/vcl-console.md)                                     | Experimenting with VCL expressions interactively              |
| VCL Statistics           | [vcl-statistics.md](references/vcl-statistics.md)                               | Analyzing VCL project size and complexity                     |

## Source Code as VCL Reference (Quick Lookup)

When you have access to the falco source code locally (default: `~/src/falco`), use these paths to answer specific VCL questions:

| Question                                      | Read This File                                    | Why                                                          |
| --------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| "What variables can I use in `vcl_recv`?"      | `interpreter/variable/`                           | Every `req.*`, `beresp.*`, `client.*` variable with scopes   |
| "What built-in functions exist?"               | `interpreter/function/`                           | All 390+ functions with type signatures and scope rules      |
| "What are the VCL types?"                      | `interpreter/value/`                              | STRING, INTEGER, FLOAT, BOOL, TIME, RTIME, IP, BACKEND       |
| "What's the request lifecycle?"                | `interpreter/context/`                            | The 9 scopes: recv, hash, hit, miss, pass, fetch, error, deliver, log |
| "Is this valid VCL syntax?"                    | `token/token.go`, `lexer/lexer.go`               | Every keyword, operator, literal type                        |
| "How does this VCL statement work?"            | `interpreter/statement.go`                        | How set, unset, return, restart, etc. execute                |
| "What are common VCL mistakes?"               | `linter/`, `docs/rules.md`                        | 50+ linting rules with explanations                          |
| "How do directors work?"                       | `interpreter/director.go`                         | Random, fallback, hash, client, chash director types         |

For a comprehensive guide, see [understanding-vcl-from-source.md](references/understanding-vcl-from-source.md).
