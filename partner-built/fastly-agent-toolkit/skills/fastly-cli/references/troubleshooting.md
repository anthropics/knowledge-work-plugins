# Fastly CLI Troubleshooting

## 503 "hostname doesn't match against certificate"

When `--override-host` differs from `--address`, you MUST set `--ssl-cert-hostname` and `--ssl-sni-hostname` to the origin's actual hostname (the one its TLS certificate covers), NOT the override-host value. Without these flags, Fastly validates the cert against the override-host and fails. **Always set all four flags together**: `--address`, `--override-host`, `--ssl-cert-hostname`, `--ssl-sni-hostname`. Check the origin's certificate SANs with: `echo | openssl s_client -connect ORIGIN:443 2>/dev/null | openssl x509 -noout -text | grep -A1 "Subject Alternative Name"`

## 403/400 on domain create

Use `fastly service domain create` (version-scoped API), not `fastly domain create`. The versionless `fastly domain create` returns 403 for most accounts, and returns 400 for `*.global.ssl.fastly.net` / `*.edgecompute.app` test domains with "Invalid value for fqdn". Always use `fastly service domain create`.

## "version is locked"

Use `--autoclone` or clone first with `fastly service version clone`.

## New service setup

Version 1 is unlocked — add domain, backend, and snippets all on `--version 1`, then activate once. Do NOT use `--autoclone` or `--version latest` on a new service — it causes unnecessary version cloning and scattered configuration.

## VCL commands

Snippet/custom VCL commands are under `fastly service vcl` (e.g. `fastly service vcl snippet create`, `fastly service vcl custom create`), NOT `fastly vcl snippet create`.

## `--content` is inline

The `--content` flag on snippet/custom VCL commands takes inline VCL code, not a file path. To load from a file: `--content "$(cat file.vcl)"`.

On `fastly service vcl snippet describe`, `--content` means "print only the raw VCL body". It cannot be combined with `--json` or `--verbose`.

## Test domains

Use a name you choose (e.g. `my-app.global.ssl.fastly.net`), not the service ID. `SERVICE_ID.global.ssl.fastly.net` does NOT work. Adding `foo.global.ssl.fastly.net` automatically makes `foo.freetls.fastly.net` available (HTTP/2).

## `--json` not supported on all commands

`fastly service create` does not support `--json`. Parse the text output (e.g. `SUCCESS: Created service XXXXX`) instead. Always check if `--json` is accepted before relying on JSON output.

## Propagation error sequence

After activating a new service, expect this progression: 500 "Domain Not Found" (10-30s, domain not yet known at edge) -> 503 backend errors (if backend config is wrong) -> 200 (working). If you see 503 right after 500 clears, check the backend configuration. If you see 503 "hostname doesn't match against certificate", fix the SSL hostname settings. A 503 that appears after a working 200 usually means a backend issue, not propagation.

## TLS subscription flags

The CLI flag for certificate authority is `--cert-auth` (not `--certificate-authority`). Always check CAA records with `dig CAA DOMAIN +short` before choosing a CA — mismatched CAA records cause `blocked` authorization state. To get DNS challenge details, you must use `--include tls_authorizations --json` — without `--include`, challenges are null. The `--include` flag only affects JSON output; text output always omits challenges.

## Token safety for REST API calls

NEVER use `fastly auth show --reveal` in an AI agent context — it exposes the API token in the conversation. Use `$(fastly auth show TOKEN_NAME --reveal --quiet | awk '/^Token:/ {print $2}')` with an explicit stored token name. Without a name, it fails when the CLI is authenticated via `FASTLY_API_TOKEN` or another non-stored source. Similarly, `--debug-mode` prints secrets to stdout — avoid it unless the user requests it.

## Debug mode

`fastly --debug-mode <command>` or `FASTLY_DEBUG_MODE=true` — prints API token in output, use with caution.
