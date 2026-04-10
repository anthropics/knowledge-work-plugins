# ccloud Commands for CMEK Management

This reference provides `ccloud` CLI commands for managing Customer-Managed Encryption Keys (CMEK) on CockroachDB Cloud clusters.

## Checking CMEK Status

```bash
# Check current CMEK configuration
ccloud cluster info <cluster-name> -o json
# Look for cmek_config section in the output
```

**Key fields to inspect:**
- `cmek_config.status` — Whether CMEK is enabled
- `cmek_config.key_spec` — KMS key details (provider, key URI, region)

## Enabling CMEK

```bash
# Enable CMEK with a KMS key specification
ccloud cluster update <cluster-id> \
  --cmek-key-spec '<key-spec-json>'
```

### Key Spec Examples

**AWS KMS:**
```json
{
  "type": "AWS_KMS",
  "uri": "arn:aws:kms:<region>:<account-id>:key/<key-id>",
  "auth_principal": "<cockroachdb-cloud-iam-role-arn>"
}
```

**GCP Cloud KMS:**
```json
{
  "type": "GCP_CLOUD_KMS",
  "uri": "projects/<project>/locations/<region>/keyRings/<keyring>/cryptoKeys/<key>",
  "auth_principal": "<cockroachdb-cloud-service-account>"
}
```

**Azure Key Vault:**
```json
{
  "type": "AZURE_KEY_VAULT",
  "uri": "https://<vault-name>.vault.azure.net/keys/<key-name>/<key-version>",
  "auth_principal": "<cockroachdb-cloud-managed-identity>"
}
```

## Verifying Plan Eligibility

```bash
# Check if cluster is on Advanced plan
ccloud cluster info <cluster-name> -o json | grep -i plan
```

CMEK requires:
1. Advanced plan (not Basic or Standard)
2. Advanced Security Add-on enabled

## Notes

- CMEK cannot be disabled once enabled on a cluster
- The KMS key must be in the same region as the cluster
- CockroachDB Cloud needs explicit permission to use the KMS key
- Key rotation is supported — update the key spec with a new key version
- Replace `<cluster-id>` with the actual cluster UUID from `ccloud cluster list`
- Refer to official CockroachDB docs for the most current key spec format
