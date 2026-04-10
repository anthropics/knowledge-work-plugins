# CMEK (Customer-Managed Encryption Keys) Procedures

## Prerequisites

- **CockroachDB Advanced** tier (Cloud) with advanced security features enabled.
- CMEK must be configured **at cluster creation time**. It cannot be enabled on an existing cluster.
- The encryption key must exist before cluster creation.
- CockroachDB Cloud service account must have the appropriate IAM permissions to use the key.

---

## AWS KMS

### Key Rotation

AWS KMS supports automatic annual key rotation. When enabled, AWS creates new key material annually but retains all previous key material, so existing encrypted data can still be decrypted without re-encryption.

#### Enable Automatic Key Rotation

```bash
aws kms enable-key-rotation \
  --key-id arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012
```

#### Check Rotation Status

```bash
aws kms get-key-rotation-status \
  --key-id arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012
```

Expected output:

```json
{
    "KeyRotationEnabled": true
}
```

#### Manual Key Rotation (Create New Key Version)

If you need to rotate immediately rather than waiting for automatic rotation, you can create a new key alias pointing to a new key. However, this requires re-configuration on the CockroachDB side and is not a standard procedure. Contact Cockroach Labs support before performing manual KMS key rotation.

#### IAM Policy Verification

Verify that the CockroachDB Cloud service account retains the required permissions after any IAM changes:

```bash
# Check the key policy
aws kms get-key-policy \
  --key-id arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012 \
  --policy-name default \
  --output text
```

Required permissions for the CockroachDB service role:

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::123456789012:role/CockroachCloudCMEKRole"
  },
  "Action": [
    "kms:Encrypt",
    "kms:Decrypt",
    "kms:GenerateDataKey",
    "kms:GenerateDataKeyWithoutPlaintext",
    "kms:ReEncryptFrom",
    "kms:ReEncryptTo",
    "kms:DescribeKey"
  ],
  "Resource": "*"
}
```

#### CloudTrail Audit

Verify key usage via CloudTrail to confirm CockroachDB is actively using the key:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceType,AttributeValue=AWS::KMS::Key \
  --start-time "2026-02-01T00:00:00Z" \
  --end-time "2026-02-23T23:59:59Z" \
  --query 'Events[?contains(Resources[].ResourceName, `12345678-1234-1234-1234-123456789012`)].[EventName, EventTime, Username]' \
  --output table
```

---

## GCP Cloud KMS

### Key Rotation

GCP Cloud KMS supports both automatic and manual key rotation. When a key is rotated, a new primary key version is created. Previous versions remain available for decryption.

#### Automatic Key Rotation

Configure automatic rotation with a rotation period:

```bash
gcloud kms keys update my-cmek-key \
  --keyring=my-keyring \
  --location=us-east1 \
  --rotation-period=90d \
  --next-rotation-time="2026-05-23T00:00:00Z"
```

#### Manual Key Rotation (Create New Version)

```bash
gcloud kms keys versions create \
  --key=my-cmek-key \
  --keyring=my-keyring \
  --location=us-east1
```

#### Check Key Status

```bash
# List all key versions
gcloud kms keys versions list \
  --key=my-cmek-key \
  --keyring=my-keyring \
  --location=us-east1

# Check key rotation schedule
gcloud kms keys describe my-cmek-key \
  --keyring=my-keyring \
  --location=us-east1 \
  --format="yaml(rotationPeriod, nextRotationTime)"
```

#### IAM Verification

Verify the CockroachDB service account has the correct role:

```bash
gcloud kms keys get-iam-policy my-cmek-key \
  --keyring=my-keyring \
  --location=us-east1
```

Required role: `roles/cloudkms.cryptoKeyEncrypterDecrypter`

```bash
# Grant if missing
gcloud kms keys add-iam-policy-binding my-cmek-key \
  --keyring=my-keyring \
  --location=us-east1 \
  --member="serviceAccount:cockroach-cloud-sa@my-project.iam.gserviceaccount.com" \
  --role="roles/cloudkms.cryptoKeyEncrypterDecrypter"
```

#### Audit Log Check

Verify key usage via GCP Audit Logs:

```bash
gcloud logging read \
  'resource.type="cloudkms_cryptokey" AND
   resource.labels.key_ring_id="my-keyring" AND
   resource.labels.crypto_key_id="my-cmek-key" AND
   timestamp>="2026-02-01T00:00:00Z"' \
  --project=my-project \
  --limit=20 \
  --format="table(timestamp, protoPayload.methodName, protoPayload.authenticationInfo.principalEmail)"
```

---

## Azure Key Vault

### Key Rotation

Azure Key Vault supports automatic key rotation via rotation policies and manual rotation.

#### Automatic Key Rotation

Configure a rotation policy:

```bash
az keyvault key rotation-policy update \
  --vault-name my-keyvault \
  --name my-cmek-key \
  --value '{
    "lifetimeActions": [
      {
        "trigger": {
          "timeBeforeExpiry": "P30D"
        },
        "action": {
          "type": "Rotate"
        }
      },
      {
        "trigger": {
          "timeBeforeExpiry": "P15D"
        },
        "action": {
          "type": "Notify"
        }
      }
    ],
    "attributes": {
      "expiryTime": "P90D"
    }
  }'
```

#### Manual Key Rotation

```bash
az keyvault key rotate \
  --vault-name my-keyvault \
  --name my-cmek-key
```

#### Check Key Status

```bash
# List key versions
az keyvault key list-versions \
  --vault-name my-keyvault \
  --name my-cmek-key \
  --output table

# Check current key details
az keyvault key show \
  --vault-name my-keyvault \
  --name my-cmek-key \
  --output yaml

# Check rotation policy
az keyvault key rotation-policy show \
  --vault-name my-keyvault \
  --name my-cmek-key
```

#### Access Policy Verification

Verify the CockroachDB service principal has the required permissions:

```bash
# Check access policies
az keyvault show \
  --name my-keyvault \
  --query "properties.accessPolicies[?objectId=='<cockroach-service-principal-id>']" \
  --output yaml
```

Required key permissions: `get`, `wrapKey`, `unwrapKey`

```bash
# Set access policy if needed
az keyvault set-policy \
  --name my-keyvault \
  --object-id <cockroach-service-principal-id> \
  --key-permissions get wrapKey unwrapKey
```

If using Azure RBAC instead of access policies:

```bash
# Check role assignments
az role assignment list \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/my-keyvault" \
  --assignee <cockroach-service-principal-id> \
  --output table
```

Required role: `Key Vault Crypto Service Encryption User`

#### Azure Monitor Audit Check

Verify key usage via Azure Monitor diagnostic logs:

```bash
az monitor diagnostic-settings list \
  --resource "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/my-keyvault" \
  --output table

# Query key usage logs (requires Log Analytics workspace)
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "AzureDiagnostics | where ResourceProvider == 'MICROSOFT.KEYVAULT' and Resource == 'MY-KEYVAULT' and OperationName in ('KeyGet', 'Encrypt', 'Decrypt', 'WrapKey', 'UnwrapKey') | project TimeGenerated, OperationName, CallerIPAddress, identity_claim_appid_s | order by TimeGenerated desc | take 20" \
  --output table
```

---

## CMEK Operational Notes

### Key Revocation Warning

**Revoking CockroachDB's access to the CMEK key will make the cluster inaccessible.** Data encrypted with the key cannot be read without key access. This is by design -- it provides a "kill switch" for data sovereignty compliance -- but it must be understood as an irreversible action unless access is restored.

### Key Deletion Warning

**Deleting a CMEK key permanently destroys access to all data encrypted with that key.** All cloud providers have key deletion safeguards (scheduled deletion periods), but once a key is permanently deleted, the encrypted data is unrecoverable.

- AWS: Minimum 7-day waiting period before deletion.
- GCP: Key versions can be destroyed (24-hour delay) but key material is not recoverable after.
- Azure: Soft delete and purge protection can provide recovery windows.

### Cross-Region Considerations

If your CockroachDB cluster spans multiple regions, ensure the CMEK key is accessible from all regions. Options:

- **AWS**: Use a multi-region KMS key.
- **GCP**: Cloud KMS keys are regional. Create keys in each region or use global keys.
- **Azure**: Key Vault is regional. Use Key Vault replication or separate keys per region.

### Monitoring Key Health

Set up alerts for:

1. **Key access failures**: Monitor CockroachDB logs for encryption/decryption errors.
2. **Key approaching expiry**: Alert before rotation policy triggers.
3. **IAM permission changes**: Alert on changes to the key's IAM policy or access policies.
4. **Key disabled/scheduled for deletion**: Alert immediately on any key state changes.
