---
name: fastly-cli
description: "Executes Fastly CLI commands for managing CDN services, Compute deploys, and edge infrastructure. Use when running `fastly` CLI commands, creating or managing Fastly services from the terminal, deploying Fastly Compute applications, managing backends/domains/VCL snippets via command line, purging cache, configuring log streaming, setting up TLS certificates, managing KV/config/secret stores, checking service stats, authenticating with Fastly SSO, or working with fastly.toml. Also applies when working with Fastly service IDs in CLI context, or with `fastly service`, `fastly compute`, `fastly auth`, or any Fastly CLI subcommand. Covers service CRUD, version management, autocloning, and troubleshooting common CLI errors."
---

## Trigger and scope

CRITICAL: many subcommands have unintuitive paths (e.g. `fastly domain create` fails with 403, correct is `fastly service domain create`; logging is under `fastly service logging`; alerts under `fastly service alert`; rate limits under `fastly service rate-limit`).

Covers: services, backends, domains, VCL snippets, cache purging, Compute/WASM deploys, log streaming (S3/Datadog/Splunk/Kafka/25+ providers), NGWAF/WAF, TLS/mTLS, KV/config/secret stores, stats, alerts, rate limiting, ACLs, and auth tokens.

# Fastly CLI Overview

## References

| Topic          | File                                  | Use when...                                                                              |
| -------------- | ------------------------------------- | ---------------------------------------------------------------------------------------- |
| Authentication | [auth.md](references/auth.md)         | Login, stored tokens, service auth, CI/CD auth setup                                     |
| Compute        | [compute.md](references/compute.md)   | Building/deploying edge applications, local dev server                                   |
| Services       | [services.md](references/services.md) | Service CRUD, backends, domains, ACLs, dictionaries, VCL, purging, rate limiting         |
| Logging        | [logging.md](references/logging.md)   | Log streaming to S3, GCS, Datadog, Splunk, Kafka, 25+ providers                          |
| NGWAF          | [ngwaf.md](references/ngwaf.md)       | Next-Gen WAF workspaces, IP/country lists, rules, signals, thresholds, alerts            |
| Stats          | [stats.md](references/stats.md)       | Historical/real-time metrics, cache hit ratios, error rates, bandwidth, regional traffic |
| Stores         | [stores.md](references/stores.md)     | KV Stores, Config Stores, Secret Stores, resource links                                  |
| TLS            | [tls.md](references/tls.md)           | Platform TLS, Let's Encrypt subscriptions, custom certs, mutual TLS                      |

## Command Structure

```
fastly <command> <subcommand> [flags]
```

### Top-Level Commands

| Category     | Commands                                                                                |
| ------------ | --------------------------------------------------------------------------------------- |
| **Compute**  | `compute` - Build and deploy edge applications                                          |
| **Services** | `service` - Manage CDN services, logging, backends, VCL, ACLs, purging                  |
| **Security** | `ngwaf` - Web application firewall                                                      |
| **TLS**      | `tls-subscription`, `tls-custom`, `tls-platform`, `tls-config` - Certificate management |
| **Storage**  | `kv-store`, `config-store`, `secret-store` - Edge data stores                           |
| **Auth**     | `auth` - Login, stored tokens, active token output, revocation; `auth-token` (deprecated) |
| **Info**     | `stats`, `ip-list`, `pops`, `whoami` - Information queries                              |
| **Other**    | `dashboard`, `domain`, `products`, `object-storage`, `tools`                            |

## Global Flags

Available on most commands:

```bash
# Service targeting
--service-id SERVICE_ID    # Target service by ID
--service-name NAME        # Target service by name
-s SERVICE_ID              # Short form

# Version targeting (version-scoped commands like `fastly service domain/backend/...`)
# NOTE: `fastly domain create` does NOT accept --version (it uses a different API)
--version VERSION          # Specific version number
--version active           # Currently active version
--version latest           # Most recent version

# Authentication
--token TOKEN              # API token or stored token name (use 'default' for default)

# Output (--json is per-command, not global)
--verbose                  # Detailed output
--quiet                    # Minimal output

# Automation
--accept-defaults          # Accept default values
--auto-yes                 # Skip confirmations
--non-interactive          # No prompts
```

## Key Patterns

- Target by ID (`-s SERVICE_ID`) or name (`--service-name NAME`)
- Version targeting: `--version active`, `--version latest`, or `--version N`
- Use `--autoclone` to auto-clone locked versions
- Use `--json` for scripted output, `--non-interactive --accept-defaults` for CI/CD
- **JSON output uses PascalCase fields** (`.Name`, `.ServiceID`, `.ActiveVersion`), not lowercase
- Auth: `fastly auth login --sso` to login, or set `FASTLY_API_TOKEN` env var
- For shell substitutions or pipes that need the active API token, prefer `fastly auth token`; it prints the token only to non-terminal stdout and refuses to write it directly to a terminal
- In AI contexts, never run `fastly auth show --reveal` bare. If you specifically need a stored token by name rather than the currently active token, use `fastly auth show TOKEN_NAME --reveal --quiet | awk '/^Token:/ {print $2}'` only inside a shell substitution
- Logging is under `service logging` (e.g. `fastly service logging s3 create`)
- Config: `~/.config/fastly/config.toml` (stored tokens), `fastly.toml` (project)

## Common Flag Examples

These are the flags that cause the most confusion. Copy-paste these patterns directly.

### Autocloning (use this every time you modify a service)

```bash
# --autoclone automatically clones a locked version before making changes.
# Without it, you get "version is locked" errors and waste time cloning manually.
fastly service backend create --service-id $SID --version active --autoclone \
  --name my-origin --address origin.example.com --port 443 --use-ssl

fastly service domain create --service-id $SID --version active --autoclone \
  --name cdn.example.com
```

Always pass `--autoclone` when creating, updating, or deleting backends, domains, snippets, VCL, conditions, headers, or any other version-scoped resource. It is safe to use even on unlocked versions (it simply does nothing if the version is already editable).

### Boolean flags (--use-ssl, --use-ssl is NOT --use-ssl true)

```bash
# CORRECT - boolean flags are bare, no value
fastly service backend create --name origin --address example.com --port 443 --use-ssl

# WRONG - do not pass a value to boolean flags
fastly service backend create --name origin --address example.com --port 443 --use-ssl true
```

Other boolean flags that work the same way: `--auto-yes`, `--non-interactive`, `--verbose`, `--quiet`, `--autoclone`.

### Domain creation (requires --name flag)

```bash
# CORRECT
fastly service domain create --service-id $SID --version active --autoclone --name cdn.example.com

# WRONG - domain is not a positional argument
fastly service domain create --service-id $SID --version active cdn.example.com

# WRONG - there is no -d flag
fastly service domain create --service-id $SID --version active -d cdn.example.com
```

### Stats (historical and real-time)

```bash
# Historical stats by day for a date range (JSON output)
fastly stats historical --service-id $SID --by day \
  --from "2026-02-01" --to "2026-03-01" --json

# Real-time stats (last second)
fastly stats realtime --service-id $SID --json
```

The `--by` flag accepts: `day`, `hour`, `minute`. The `--from` and `--to` flags use quoted date strings. Use `--json` for JSON output on stats commands.

## Propagation Delays

Changes propagate across Fastly's network in seconds to minutes (up to 10 min for version activations, up to 5 min for TLS). Cache purges are 1-2 seconds. Retry with backoff when verifying changes.

**New service activation sequence**: After activating a brand new service, expect 500 "Domain Not Found" for 10-60 seconds while the domain propagates to edge POPs. This is normal — do not change configuration. Wait and retry. After version updates (e.g., fixing backend settings), allow 15-30 seconds for the new version to propagate.

## KV Store Gotchas

- **Link before use**: A KV store must be linked to a service version before Compute code can access it. Use `fastly kv-store create` then `fastly service resource-link create --resource-id STORE_ID --service-id $SID --version active --autoclone`.
- **Eventual consistency**: Read-after-write is eventually consistent. A key you just wrote may not be readable for a few seconds. Do not rely on immediate read-back in scripts; add a short delay or retry loop.
- **Entry size limit**: Individual KV store entries are limited to 25 MB. Plan accordingly for large values.
- **Listing stores**: `fastly kv-store list` lists all stores on the account, not per-service. Use `fastly service resource-link list` to see which stores are linked to a given service.

## Host Header Override Pattern

When the origin hostname differs from the desired Host header (e.g., origin is `example.com` but you want to send `Host: download.example.com`), use `--override-host` on the backend:

```bash
fastly service backend create --service-id $SID --version 1 \
  --name my-origin --address example.com --port 443 --use-ssl \
  --override-host download.example.com \
  --ssl-cert-hostname example.com --ssl-sni-hostname example.com
```

The `--override-host` value is the Host header sent to the origin. The `--ssl-cert-hostname` and `--ssl-sni-hostname` must match the origin's TLS certificate (usually the `--address` value). Getting these backwards causes 503 errors.

## Service List Completeness

When enumerating services (e.g., for bandwidth stats), always use `fastly service list --json` and check for pagination. Services with zero traffic still appear in the list. Loop over ALL service IDs from the list — do not rely on stats APIs that omit zero-traffic services.

## Troubleshooting

See [troubleshooting.md](references/troubleshooting.md) for the full list. The most common pitfalls:

- **503 SSL mismatch**: When `--override-host` differs from `--address`, always set `--ssl-cert-hostname` and `--ssl-sni-hostname` to the origin's actual hostname (the `--address` value, not the `--override-host` value).
- **403/400 on domain create**: Use `fastly service domain create`, not `fastly domain create`.
- **"version is locked"**: Use `--autoclone` or clone first. Better yet, always pass `--autoclone` on every mutation command.
- **New service setup**: Version 1 is unlocked — add domain, backend, snippets on `--version 1`, then activate once.
- **VCL commands**: Under `fastly service vcl` (e.g. `fastly service vcl snippet create`), not `fastly vcl`.
- **Token safety**: Never use `fastly auth show --reveal` bare in an AI context — it exposes tokens.
- **`--use-ssl` is a boolean flag**: Write `--use-ssl`, not `--use-ssl true`. Passing a value causes the next argument to be misinterpreted.
- **Domain requires `--name`**: The domain is passed via `--name cdn.example.com`, not as a positional argument and not with `-d`.
