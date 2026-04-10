---
name: enabling-cmek-encryption
description: Enables Customer-Managed Encryption Keys (CMEK) on CockroachDB Cloud clusters with the Advanced plan and Advanced Security Add-on to give organizations control over data-at-rest encryption keys via their cloud provider's KMS. Use when enabling CMEK for compliance, rotating encryption keys, or verifying CMEK configuration.
compatibility: Requires CockroachDB Cloud Advanced plan with Advanced Security Add-on and cloud provider KMS (AWS KMS, GCP Cloud KMS, or Azure Key Vault).
metadata:
  author: cockroachdb
  version: "1.0"
---

# Enabling CMEK Encryption

Enables Customer-Managed Encryption Keys (CMEK) on CockroachDB Cloud clusters so that data-at-rest encryption is controlled by keys in the organization's own cloud provider KMS (AWS KMS, GCP Cloud KMS, or Azure Key Vault). CMEK gives organizations full control over key lifecycle, rotation, and revocation.

## When to Use This Skill

- Enabling CMEK for regulatory or compliance requirements (SOC 2, HIPAA, PCI DSS)
- Verifying CMEK is properly configured after initial setup
- Rotating CMEK keys per organization key rotation policy
- Responding to a security audit finding about encryption at rest
- Understanding CMEK requirements and plan prerequisites

## Prerequisites

- **CockroachDB Cloud Advanced plan** — CMEK is not available on Basic or Standard plans
- **Advanced Security Add-on** — Must be enabled on the Advanced plan cluster
- **Cloud provider KMS:**
  - **AWS:** KMS key in the same region as the cluster, with appropriate IAM policy
  - **GCP:** Cloud KMS key ring and key in the same region, with appropriate IAM bindings
  - **Azure:** Key Vault with key in the same region, with appropriate access policies
- **ccloud CLI** authenticated with Cluster Admin role
- **Cross-account access:** The CockroachDB Cloud service account must have permission to use the KMS key

**Check plan eligibility:**
```bash
# Verify cluster plan type
ccloud cluster info <cluster-name> -o json
# Look for "plan": "ADVANCED" and Advanced Security Add-on status
```

## Configuration Decisions

Before proceeding, determine which cloud provider KMS the user will use. Ask which option applies to their environment, then follow only the corresponding subsection in Step 2.

**Decision 1 — Cloud provider KMS:**
- **AWS KMS:** Use when the CockroachDB Cloud cluster runs on AWS. Requires a symmetric encryption key in the same region as the cluster.
- **GCP Cloud KMS:** Use when the cluster runs on GCP. Requires a key ring and key in the same region.
- **Azure Key Vault:** Use when the cluster runs on Azure. Requires a Key Vault with a key in the same region.

## Steps

### 1. Verify Plan and Add-on Eligibility

```bash
ccloud cluster info <cluster-name> -o json
```

**If Standard plan:** CMEK is not available. The upgrade path is:
1. Upgrade to Advanced plan (contact CockroachDB sales or upgrade in Cloud Console)
2. Enable the Advanced Security Add-on

**If Advanced plan without Advanced Security Add-on:** Enable the add-on in the Cloud Console before proceeding.

### 2. Create a KMS Key in Your Cloud Provider

Follow only the subsection for the user's cloud provider (selected in Configuration Decisions above).

#### AWS KMS

```bash
# Create a symmetric encryption key in the same region as the cluster
aws kms create-key \
  --description "CockroachDB CMEK - <cluster-name>" \
  --key-usage ENCRYPT_DECRYPT \
  --origin AWS_KMS \
  --region <aws-region>
```

Grant the CockroachDB Cloud service account access to the key:
```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "<cockroachdb-cloud-service-account-arn>"
  },
  "Action": [
    "kms:Encrypt",
    "kms:Decrypt",
    "kms:GenerateDataKey",
    "kms:DescribeKey"
  ],
  "Resource": "*"
}
```

#### GCP Cloud KMS

```bash
# Create a key ring
gcloud kms keyrings create cockroachdb-cmek \
  --location <gcp-region>

# Create a symmetric encryption key
gcloud kms keys create cmek-key \
  --keyring cockroachdb-cmek \
  --location <gcp-region> \
  --purpose encryption
```

Grant the CockroachDB Cloud service account access:
```bash
gcloud kms keys add-iam-policy-binding cmek-key \
  --keyring cockroachdb-cmek \
  --location <gcp-region> \
  --member "serviceAccount:<cockroachdb-cloud-service-account>" \
  --role "roles/cloudkms.cryptoKeyEncrypterDecrypter"
```

#### Azure Key Vault

```bash
# Create a key in the existing Key Vault
az keyvault key create \
  --vault-name <vault-name> \
  --name cockroachdb-cmek \
  --kty RSA \
  --size 2048
```

Grant the CockroachDB Cloud managed identity access via Key Vault access policies.

### 3. Configure CMEK on the Cluster

```bash
# Enable CMEK with the KMS key URI
ccloud cluster update <cluster-id> \
  --cmek-key-spec '<key-spec-json>'
```

The key spec format varies by cloud provider. Refer to the CockroachDB Cloud documentation for the exact JSON structure for your provider.

See [ccloud commands reference](references/ccloud-commands.md) for detailed command syntax.

### 4. Verify CMEK Configuration

```bash
# Check CMEK status
ccloud cluster info <cluster-name> -o json
# Verify cmek_config shows enabled status and correct key URI
```

```sql
-- Verify encryption via SQL
SHOW CLUSTER SETTING enterprise.encryption.type;
```

### 5. Test Key Accessibility

After enabling CMEK, verify the cluster is operating normally:

```sql
-- Create and query a test table to verify read/write works
CREATE TABLE cmek_test (id INT PRIMARY KEY, data STRING);
INSERT INTO cmek_test VALUES (1, 'encryption test');
SELECT * FROM cmek_test;
DROP TABLE cmek_test;
```

## Safety Considerations

**CMEK misconfiguration can make data inaccessible.** If the KMS key is deleted, disabled, or access is revoked, the cluster will not be able to read or write data.

**Before enabling CMEK:**
- Ensure the KMS key has appropriate deletion protection enabled
- Verify the IAM/access policy grants are correct
- Confirm the KMS key region matches the cluster region
- Document the key URI and access policies

**Key management risks:**
- **Key deletion:** Deleting the KMS key makes all cluster data permanently inaccessible
- **Access revocation:** Revoking CockroachDB's access to the key will cause the cluster to stop serving reads and writes
- **Key rotation:** Plan key rotation per your organization's policy; CockroachDB supports automatic re-encryption with rotated keys

## Rollback

CMEK cannot be disabled once enabled on a cluster. However:

1. **Key rotation:** You can rotate to a new key at any time
2. **Access restoration:** If access was accidentally revoked, restore the IAM/access policy to resume operations
3. **New cluster:** If CMEK configuration is fundamentally wrong, create a new cluster and migrate data

**Emergency — Key access lost:**
1. Restore KMS key access immediately (IAM policy, key re-enable)
2. The cluster will resume operations once key access is restored
3. If the key was permanently deleted, data recovery is not possible

## References

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit

**Official CockroachDB Documentation:**
- [CMEK Overview](https://www.cockroachlabs.com/docs/cockroachcloud/cmek.html)
- [Managing CMEK for Dedicated Clusters](https://www.cockroachlabs.com/docs/cockroachcloud/managing-cmek.html)
- [CockroachDB Cloud Security Overview](https://www.cockroachlabs.com/docs/cockroachcloud/security-overview.html)

**Cloud Provider KMS Documentation:**
- [AWS KMS](https://docs.aws.amazon.com/kms/)
- [GCP Cloud KMS](https://cloud.google.com/kms/docs)
- [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/)
