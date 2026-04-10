# Fastly Edge Data Stores

Manage data stores for edge applications: KV Stores, Config Stores, and Secret Stores.

## Store Types Overview

| Store Type   | Purpose                   | Size Limit      | Updates        |
| ------------ | ------------------------- | --------------- | -------------- |
| KV Store     | General key-value storage | 25 MB per value | Real-time      |
| Config Store | Configuration data        | 8 KB per value  | Near real-time |
| Secret Store | Sensitive data (API keys) | 64 KB per value | Near real-time |

## KV Stores

KV Stores provide fast, globally distributed key-value storage.

### Store Management

```bash
# List all KV stores
fastly kv-store list

# Create store
fastly kv-store create --name my-cache

# Create store in a specific region
fastly kv-store create --name my-cache --location=US

# Describe store
fastly kv-store describe --store-id STORE_ID

# Delete store
fastly kv-store delete --store-id STORE_ID

# Delete all entries in a store (keeps the store itself)
fastly kv-store delete --store-id STORE_ID --all --concurrency=100 --max-errors=100
```

### Entry Management

```bash
# List keys in store
fastly kv-store-entry list --store-id STORE_ID

# List keys with a prefix filter
fastly kv-store-entry list --store-id STORE_ID --prefix="user:"

# List keys with eventual consistency (uses caching, better performance)
fastly kv-store-entry list --store-id STORE_ID --consistency=eventual

# Create/update entry
fastly kv-store-entry create --store-id STORE_ID --key "user:123" --value '{"name":"John"}'

# Create entry (fail if key already exists)
fastly kv-store-entry create --store-id STORE_ID --key "user:123" --value '{"name":"John"}' --add

# Append or prepend to existing value
fastly kv-store-entry create --store-id STORE_ID --key "log:1" --value "new line" --append
fastly kv-store-entry create --store-id STORE_ID --key "log:1" --value "first line" --prepend

# Create with metadata (up to 2000 bytes)
fastly kv-store-entry create --store-id STORE_ID --key "user:123" --value '...' --metadata='{"type":"user"}'

# Conditional update (only if generation marker matches)
fastly kv-store-entry create --store-id STORE_ID --key "user:123" --value '...' --if-generation-match=42

# Allow stale reads during update (background fetch)
fastly kv-store-entry create --store-id STORE_ID --key "user:123" --value '...' --background-fetch

# Bulk create from a directory (filename becomes key, contents become value)
fastly kv-store-entry create --store-id STORE_ID --dir=./data --dir-concurrency=50

# Bulk create from directory including hidden files
fastly kv-store-entry create --store-id STORE_ID --dir=./data --dir-allow-hidden

# Bulk create from newline-delimited JSON file
fastly kv-store-entry create --store-id STORE_ID --file=entries.jsonl

# Bulk create from STDIN (newline-delimited JSON)
fastly kv-store-entry create --store-id STORE_ID --stdin

# Get entry value
fastly kv-store-entry get --store-id STORE_ID --key "user:123"

# Get entry with generation marker comparison
fastly kv-store-entry get --store-id STORE_ID --key "user:123" --if-generation-match=42

# Describe entry (metadata)
fastly kv-store-entry describe --store-id STORE_ID --key "user:123"

# Delete entry
fastly kv-store-entry delete --store-id STORE_ID --key "user:123"

# Delete entry (return success even if key not found)
fastly kv-store-entry delete --store-id STORE_ID --key "user:123" --force

# Conditional delete (only if generation marker matches)
fastly kv-store-entry delete --store-id STORE_ID --key "user:123" --if-generation-match=42

# Delete all entries in a store
fastly kv-store-entry delete --store-id STORE_ID --all --concurrency=100 --max-errors=100
```

### Link KV Store to Service

```bash
# Link store to service
fastly service resource-link create \
  --service-id SERVICE_ID \
  --version 1 \
  --resource-id STORE_ID \
  --name my-cache

# List linked resources
fastly service resource-link list --service-id SERVICE_ID --version 1
```

## Config Stores

Config Stores hold configuration data that can be updated without redeploying.

### Store Management

```bash
# List all config stores
fastly config-store list

# Create store
fastly config-store create --name app-settings

# Describe store
fastly config-store describe --store-id STORE_ID

# Describe store with metadata
fastly config-store describe --store-id STORE_ID --metadata

# Update store name
fastly config-store update --store-id STORE_ID --name new-name

# List services using this store
fastly config-store list-services --store-id STORE_ID

# Delete store
fastly config-store delete --store-id STORE_ID
```

### Entry Management

```bash
# List entries
fastly config-store-entry list --store-id STORE_ID

# Create entry
fastly config-store-entry create --store-id STORE_ID --key "feature_flag" --value "true"

# Create entry reading value from STDIN (--value ignored)
fastly config-store-entry create --store-id STORE_ID --key "feature_flag" --stdin

# Describe entry
fastly config-store-entry describe --store-id STORE_ID --key "feature_flag"

# Update entry
fastly config-store-entry update --store-id STORE_ID --key "feature_flag" --value "false"

# Update entry reading value from STDIN
fastly config-store-entry update --store-id STORE_ID --key "feature_flag" --stdin

# Upsert entry (insert or update)
fastly config-store-entry update --store-id STORE_ID --key "feature_flag" --value "false" --upsert

# Delete entry
fastly config-store-entry delete --store-id STORE_ID --key "feature_flag"

# Delete all entries
fastly config-store-entry delete --store-id STORE_ID --all --batch-size=50 --concurrency=10
```

### Link Config Store to Service

```bash
fastly service resource-link create \
  --service-id SERVICE_ID \
  --version 1 \
  --resource-id STORE_ID \
  --name settings
```

## Secret Stores

Secret Stores securely hold sensitive data like API keys and credentials.

### Store Management

```bash
# List all secret stores
fastly secret-store list

# List with pagination
fastly secret-store list --cursor=CURSOR --limit=50

# Create store
fastly secret-store create --name api-keys

# Describe store
fastly secret-store describe --store-id STORE_ID

# Delete store
fastly secret-store delete --store-id STORE_ID
```

### Secret Management

```bash
# List secrets (keys only, not values)
fastly secret-store-entry list --store-id STORE_ID

# List with pagination
fastly secret-store-entry list --store-id STORE_ID --cursor=CURSOR --limit=50

# Create secret (prompted for value interactively)
fastly secret-store-entry create --store-id STORE_ID --name "stripe_key"

# Create secret from file
fastly secret-store-entry create --store-id STORE_ID --name "certificate" --file=./cert.pem

# Create secret from STDIN
echo "sk_live_..." | fastly secret-store-entry create --store-id STORE_ID --name "stripe_key" --stdin

# Recreate an existing secret (errors if secret doesn't exist)
fastly secret-store-entry create --store-id STORE_ID --name "stripe_key" --file=./new-key.txt --recreate

# Create or recreate (works whether secret exists or not)
fastly secret-store-entry create --store-id STORE_ID --name "stripe_key" --file=./key.txt --recreate-allow

# Describe secret (metadata only)
fastly secret-store-entry describe --store-id STORE_ID --name "stripe_key"

# Delete secret
fastly secret-store-entry delete --store-id STORE_ID --name "stripe_key"
```

### Link Secret Store to Service

```bash
fastly service resource-link create \
  --service-id SERVICE_ID \
  --version 1 \
  --resource-id STORE_ID \
  --name secrets
```

## Resource Links

Resource links connect stores to services.

```bash
# List all resource links
fastly service resource-link list --service-id SERVICE_ID --version 1

# Create link
fastly service resource-link create \
  --service-id SERVICE_ID \
  --version 1 \
  --resource-id STORE_ID \
  --name my-store

# Describe link
fastly service resource-link describe --service-id SERVICE_ID --version 1 --id LINK_ID

# Update link name
fastly service resource-link update --service-id SERVICE_ID --version 1 --id LINK_ID --name new-name

# Delete link
fastly service resource-link delete --service-id SERVICE_ID --version 1 --id LINK_ID
```

## Using Stores in Compute Applications

### Rust Example

```rust
use fastly::kv_store::KVStore;
use fastly::config_store::ConfigStore;
use fastly::secret_store::SecretStore;

// KV Store
let store = KVStore::open("my-cache")?.unwrap();
let value = store.lookup("key")?;
store.insert("key", "value")?;

// Config Store
let config = ConfigStore::open("settings");
let flag = config.get("feature_flag")?;

// Secret Store
let secrets = SecretStore::open("api-keys");
let api_key = secrets.get("stripe_key")?.plaintext();
```

### JavaScript Example

```javascript
import { KVStore } from "fastly:kv-store";
import { ConfigStore } from "fastly:config-store";
import { SecretStore } from "fastly:secret-store";

// KV Store
const kv = new KVStore("my-cache");
const entry = await kv.get("key");
await kv.put("key", "value");

// Config Store
const config = new ConfigStore("settings");
const flag = config.get("feature_flag");

// Secret Store
const secrets = new SecretStore("api-keys");
const apiKey = await secrets.get("stripe_key");
```

## Common Workflows

### Setup Feature Flags

```bash
# Create config store
fastly config-store create --name feature-flags

# Add flags
fastly config-store-entry create --store-id STORE_ID --key "new_ui" --value "false"
fastly config-store-entry create --store-id STORE_ID --key "beta_features" --value "true"

# Link to service
fastly service resource-link create --service-id SERVICE_ID --version 1 --resource-id STORE_ID --name flags

# Update flag (no redeploy needed)
fastly config-store-entry update --store-id STORE_ID --key "new_ui" --value "true"
```

### Setup API Key Storage

```bash
# Create secret store
fastly secret-store create --name external-apis

# Add secrets (value read from file or STDIN)
fastly secret-store-entry create --store-id STORE_ID --name "stripe_key" --file=./stripe.key
fastly secret-store-entry create --store-id STORE_ID --name "openai_key" --file=./openai.key

# Link to service
fastly service resource-link create --service-id SERVICE_ID --version 1 --resource-id STORE_ID --name apis
```

### Setup Edge Cache

```bash
# Create KV store
fastly kv-store create --name edge-cache

# Prepopulate data
fastly kv-store-entry create --store-id STORE_ID --key "product:1" --value '{"name":"Widget","price":9.99}'

# Link to service
fastly service resource-link create --service-id SERVICE_ID --version 1 --resource-id STORE_ID --name cache
```

## Propagation Delays

Store updates have varying propagation times:
- **KV Store**: Real-time to near real-time propagation
- **Config Store**: Near real-time (typically under 30 seconds)
- **Secret Store**: Near real-time (typically under 30 seconds)

When automating store operations, allow time for changes to propagate before reading updated values from edge applications. Resource link changes require version activation and follow standard service propagation times (5-30 seconds).

## Dangerous Operations

Ask the user for explicit confirmation before running these commands:

- `fastly kv-store delete` - Permanently deletes a KV store and all its entries
- `fastly kv-store delete --all` - Permanently deletes all entries in a KV store
- `fastly kv-store-entry delete --all` - Permanently deletes all entries in a KV store
- `fastly config-store delete` - Permanently deletes a config store
- `fastly config-store-entry delete --all` - Permanently deletes all entries in a config store
- `fastly secret-store delete` - Permanently deletes a secret store and its secrets

These operations are irreversible. Linked services will lose access to the deleted store.

## fastly.toml Setup Configuration

Define stores in your manifest for automatic creation during deploy:

```toml
[setup.config_stores]
  [setup.config_stores.settings]
  description = "Application configuration"

[setup.kv_stores]
  [setup.kv_stores.cache]
  description = "Edge cache storage"

[setup.secret_stores]
  [setup.secret_stores.secrets]
  description = "API keys and credentials"
```

## KV Store Troubleshooting

### Read-After-Write Consistency

KV stores have eventual consistency. After a `PUT`, the value may not be immediately available via `GET`. When testing locally or in evals, add a short delay or retry logic for read-after-write scenarios. Don't assume a key is readable the instant you write it.

### Store Linking

KV stores must be linked to a service before the Compute app can access them. The correct sequence is:

```bash
# 1. Create the store (note the store ID in the output)
fastly kv-store create --name NAME

# 2. Link the store to your service
fastly service resource-link create --service-id SERVICE_ID --version VERSION --resource-id STORE_ID --autoclone

# 3. Deploy the app
fastly compute deploy
```

A common error is getting "store not found" at runtime. This almost always means the store was not linked to the service. Double-check with `fastly service resource-link list` that the store appears as a linked resource.

### Redirect Pattern

When building URL shorteners or similar apps that look up a URL in a KV store and redirect the user, the response MUST use a `302` status with a `Location` header:

```javascript
return new Response(null, { status: 302, headers: { "Location": url } });
```

Do NOT return a `200` with the URL in the body. Browsers will not follow the redirect without the `Location` header and a `3xx` status code.

### KV Store Key Listing

The `kv-store-entry list` command paginates results. Use `--json` and check for a `cursor` field in the output to retrieve subsequent pages:

```bash
# First page
fastly kv-store-entry list --store-id STORE_ID --json

# Next page (if cursor was returned)
fastly kv-store-entry list --store-id STORE_ID --json --cursor=CURSOR_VALUE
```

In the Compute SDK (JavaScript), use `KVStore.prototype.list()` which returns an async iterator that handles pagination automatically:

```javascript
const store = new KVStore("my-store");
for await (const entry of store.list()) {
  console.log(entry);
}
```
