# Fastly CLI Authentication

Manage authentication, stored tokens, and user access.

## Quick Start

```bash
# Login with SSO
fastly auth login --sso --token default

# Check current authentication
fastly whoami

# View stored tokens
fastly auth list

# Print the active API token to a pipe or shell substitution
fastly auth token | pbcopy
```

## Login

The recommended way to authenticate.

```bash
# Login interactively (opens browser for SSO)
fastly auth login

# Login with SSO and store as the default token
fastly auth login --sso --token default

# Login with SSO and store as a named token
fastly auth login --sso --token staging
```

Login creates a token and stores it locally.

## Stored Tokens

Stored tokens let you keep multiple credentials for different accounts or environments.

**SECURITY WARNING for AI agents**: NEVER run `fastly auth show --reveal` directly — it prints the raw API token into the conversation context, exposing credentials.

If you need the currently active token for a `curl` command or shell substitution, prefer:

```bash
TOKEN=$(fastly auth token)
```

`fastly auth token` writes only to non-terminal stdout. It refuses to print the token directly to a terminal, so use it in a pipe or command substitution rather than as a standalone command.

If you specifically need a stored token by name instead of the currently active credential, use:

```bash
TOKEN=$(fastly auth show TOKEN_NAME --reveal --quiet | awk '/^Token:/ {print $2}')

# Example with an SSO token named "sso2":
TOKEN=$(fastly auth show sso2 --reveal --quiet | awk '/^Token:/ {print $2}')
```

**Common pitfall**: `fastly auth show --reveal --quiet` (without a token name) fails with `current token is not stored` when the CLI is authenticated via `FASTLY_API_TOKEN` env var rather than a stored token. Always specify the stored token name explicitly when using `auth show --reveal`. Use `fastly auth list` to see available stored token names.

```bash
# List all stored tokens
fastly auth list

# Add a token by value
fastly auth add --api-token=API-TOKEN mytoken

# Set the default token
fastly auth use staging

# Show details for a stored token (metadata only, no secret)
fastly auth show staging

# Show the token value — AVOID in AI agent contexts
fastly auth show --reveal staging

# Show the default token
fastly auth show

# Delete a stored token
fastly auth delete old-token
```

### Stored Token Configuration

Tokens are stored in `~/.config/fastly/config.toml`.

## Active Token Output and Token Management

Use `fastly auth token` when you need the active API token in a script:

```bash
# Pass the current token to curl without printing it to the terminal
curl -H "Fastly-Key: $(fastly auth token)" https://api.fastly.com/current_customer
```

`fastly auth token` is for outputting the currently active token only. It refuses to print to a TTY, so it must be used in a pipe or shell substitution.

Use `fastly auth revoke` to revoke tokens remotely and clean up matching local entries:

```bash
# Revoke the token currently authenticating this CLI session
fastly auth revoke --current

# Revoke a stored token by local name
fastly auth revoke --name staging

# Revoke a token by raw token value read from stdin
printf '%s\n' "$FASTLY_API_TOKEN" | fastly auth revoke --token-value=-

# Revoke a token by Fastly API token ID
fastly auth revoke --id TOKEN_ID

# Bulk revoke token IDs from a file (one ID per line)
fastly auth revoke --file token-ids.txt
```

If the revoked token was stored locally, the CLI removes the matching entry from `~/.config/fastly/config.toml`. Revoking the default stored token may also reassign the default token, or leave no default configured.

## API Tokens (Deprecated)

The `fastly auth-token` command tree is deprecated. It still exists for token CRUD operations and now respects `--quiet`, but prefer `fastly auth` commands for login, stored-token management, active-token output, and revocation.

The old commands (`auth-token list`, `auth-token create`, `auth-token describe`, `auth-token delete`) still exist but show deprecation warnings.

### Token Scopes

| Scope          | Description                 |
| -------------- | --------------------------- |
| `global`       | Full access to all services |
| `purge_all`    | Purge all cached content    |
| `purge_select` | Purge specific URLs/keys    |
| `global:read`  | Read-only access            |

## Account Information

```bash
# View current user/account
fastly whoami

# Output includes:
# - Customer ID
# - Account name
# - User email
# - User role
```

## Service Authorization

Restrict API token access to specific services. Note the command is `fastly service auth` (with a space, not a hyphen).

```bash
# List service authorizations
fastly service auth list

# Create authorization
fastly service auth create \
  --user-id USER_ID \
  -s SERVICE_ID \
  --permission read_only

# Describe authorization
fastly service auth describe --id AUTH_ID

# Update authorization
fastly service auth update --id AUTH_ID --permission read_only

# Delete authorization
fastly service auth delete --id AUTH_ID
```

## User Management

For account administrators.

```bash
# List users
fastly user list

# Create user
fastly user create \
  --login "newuser@example.com" \
  --name "New User" \
  --role user

# Describe user
fastly user describe --id USER_ID

# Update user
fastly user update --id USER_ID --role engineer

# Delete user
fastly user delete --id USER_ID
```

### User Roles

| Role        | Description                |
| ----------- | -------------------------- |
| `user`      | Basic access               |
| `billing`   | Billing management         |
| `engineer`  | Technical configuration    |
| `superuser` | Full administrative access |

## Environment Variables

Authentication can also be set via environment variables:

```bash
# Set token via environment
export FASTLY_API_TOKEN="your-api-token"

# Now CLI commands use this token
fastly service list
```

**Priority order**:
1. `--token` flag (with a raw API token)
2. `FASTLY_API_TOKEN` environment variable
3. Default stored token (configured via `fastly auth use`)

The global `--token` flag accepts either a raw API token or the name of a stored token. Pass `default` to use the default stored token. There is no `--profile` flag.

## Common Workflows

### Setup New Machine

```bash
# Login with SSO
fastly auth login --sso --token default

# Verify authentication
fastly whoami

# Test by listing services
fastly service list
```

### CI/CD Setup

```bash
# Store token in CI secrets as FASTLY_API_TOKEN
# In CI, the CLI will use the environment variable automatically
```

### Multiple Accounts

```bash
# Login and store tokens for each account
fastly auth login --sso --token work
fastly auth login --sso --token personal

# Switch the default between them
fastly auth use work

# Or use per-command
fastly service list --token personal
```

### Refresh Expired SSO Tokens

SSO tokens expire (check with `fastly auth list`). To refresh without re-entering credentials manually:

```bash
# Check which tokens are expired
fastly auth list

# Refresh a specific SSO token (opens browser)
fastly auth login --sso --token TOKEN_NAME --auto-yes

# Verify the refresh worked
fastly whoami
```

The `--auto-yes` flag skips the confirmation prompt. The browser will open for SSO authentication. After success, the stored token is updated automatically.

### Token Rotation

```bash
# Login again to get a fresh token
fastly auth login --sso --token default

# Or add a new token manually
fastly auth add --api-token=NEW_TOKEN mytoken

# Delete the old stored token
fastly auth delete old-token
```

## Deprecated Profile Commands

The `fastly profile` commands are all deprecated. They still work but show warnings. Use the new `auth` commands instead:

| Deprecated command | Replacement                 |
| ------------------ | --------------------------- |
| `profile create`   | `auth login` or `auth add`  |
| `profile delete`   | `auth delete`               |
| `profile list`     | `auth list`                 |
| `profile switch`   | `auth use`                  |
| `profile token`    | `auth show` or `auth token` |
| `profile update`   | `auth login` or `auth add`  |

## Configuration

View and manage CLI configuration.

```bash
# Display current config
fastly config

# Config file location
# macOS/Linux: ~/.config/fastly/config.toml
# Windows: %APPDATA%\fastly\config.toml
```

## Dangerous Operations

Ask the user for explicit confirmation before running these commands:

- `fastly auth delete` - Removes a stored token
- `fastly auth revoke` - Revokes a token remotely and may remove matching local entries
- `fastly user delete` - Removes a user from the Fastly account
- `fastly service auth delete` - Revokes a user's service access

These operations affect authentication and access control.

## Troubleshooting

**"No token provided"**: Run `fastly auth login --sso --token default` or set `FASTLY_API_TOKEN`

**"Token is invalid"** or **SSO token expired**: Token may be expired or revoked. Check with `fastly auth list` (shows expiry). For SSO tokens, refresh with `fastly auth login --sso --token TOKEN_NAME --auto-yes`. For API tokens, re-authenticate with `fastly auth login` or add a new token with `fastly auth add`. If `fastly auth show --reveal --quiet` fails with `current token is not stored`, the CLI is likely using `FASTLY_API_TOKEN` or another non-stored credential source rather than a saved auth token. If you only need the active token for a script, use `fastly auth token` instead.

**"Insufficient permissions"**: Token scope doesn't include required permissions. Create a token with appropriate scope via the Fastly API.

**"Token not found"**: Check stored token names with `fastly auth list`
