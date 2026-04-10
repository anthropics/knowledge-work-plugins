---
name: configuring-sso-and-scim
description: Configures SSO authentication and SCIM 2.0 provisioning for CockroachDB across four distinct layers — Cloud Console SSO (SAML/OIDC), DB Console SSO (OIDC), SQL/Cluster SSO (JWT or LDAP/AD), and SCIM 2.0 automated provisioning. Use when enabling centralized identity management, setting up SSO for compliance, or automating user lifecycle management.
compatibility: Requires CockroachDB Cloud organization admin for Console SSO/SCIM. Requires cluster admin for DB Console and SQL SSO configuration. DB Console SSO requires Advanced or Enterprise plan (not available on Standard/Basic). LDAP/AD authentication is self-hosted only (not available on CockroachDB Cloud). SCIM 2.0 requires Enterprise plan.
metadata:
  author: cockroachdb
  version: "2.0"
---

# Configuring SSO and SCIM

Configures Single Sign-On (SSO) and SCIM 2.0 provisioning for CockroachDB across four distinct layers:

1. **Cloud Console SSO** — SAML or OIDC for the CockroachDB Cloud web console
2. **DB Console SSO** — OIDC for the DB Console web UI (Advanced/Enterprise only)
3. **SQL/Cluster SSO** — JWT-based or LDAP/AD authentication for SQL client connections
4. **SCIM 2.0** — Automated user provisioning on the Cloud Console

## When to Use This Skill

- Enabling centralized identity management via an IdP (Okta, Azure AD, Google Workspace, etc.)
- Meeting compliance requirements for SSO-only authentication
- Automating user provisioning and deprovisioning to prevent orphaned accounts
- Setting up SSO for SQL authentication to eliminate database-level passwords
- Configuring LDAP/AD authentication for self-hosted clusters in on-prem or hybrid environments
- Responding to a security audit finding about missing SSO or SCIM configuration

## Prerequisites

- **Cloud Console role:** Organization Admin (for Console SSO and SCIM)
- **SQL access:** Cluster admin role (for DB Console SSO and SQL/Cluster SSO)
- **Identity Provider (IdP):** Configured and operational — Okta, Azure AD, Google Workspace, PingOne, or other SAML/OIDC-compatible provider
- **ccloud CLI** authenticated (`ccloud auth login`) — for Cloud Console SSO/SCIM
- **DB Console SSO:** Advanced or Enterprise plan required (not available on Standard or Basic)
- **SCIM:** Enterprise plan required for SCIM 2.0
- **LDAP/AD:** Self-hosted CockroachDB cluster required (LDAP is not available on CockroachDB Cloud)

**Verify access:**
```bash
ccloud auth whoami
```

## Configuration Decisions

Before proceeding, determine which layers the user needs. Ask which of the following apply, then follow only the relevant Parts below.

**Decision 1 — Cloud Console SSO:**
- **SAML:** Best for enterprise IdPs with existing SAML infrastructure (Okta, Azure AD, PingOne)
- **OIDC:** Simpler setup, supports Google Workspace and modern IdPs natively
- **Skip:** Not needed

**Decision 2 — DB Console SSO:**
- **Enable (OIDC):** SSO for the DB Console web UI. Requires Advanced or Enterprise plan — not available on Standard or Basic
- **Skip:** Not needed or plan does not support it

**Decision 3 — SQL/Cluster SSO method:**
- **JWT-based:** Cloud-native approach using JWT tokens for SQL client connections. Works on both CockroachDB Cloud and self-hosted clusters
- **LDAP/AD:** Direct directory authentication against Active Directory or OpenLDAP. Self-hosted only (not available on CockroachDB Cloud)
- **Skip:** Not needed

**Decision 4 — SCIM 2.0 provisioning:**
- **Enable:** Automates user lifecycle (create/update/deactivate) between IdP and Cloud Console. Requires Enterprise plan
- **Skip:** Manage Cloud Console users manually

## Steps

### Step 0: Audit Current SSO Configuration

Before configuring anything, audit the current state of all four SSO layers.

#### Cloud Console SSO

Check SSO status in the Cloud Console UI: **Organization Settings > Authentication**. The `ccloud` CLI does not expose SSO configuration commands.

#### DB Console SSO (OIDC)

```sql
SHOW CLUSTER SETTING server.oidc_authentication.enabled;
SHOW CLUSTER SETTING server.oidc_authentication.provider_url;
SHOW CLUSTER SETTING server.oidc_authentication.client_id;
```

#### SQL/Cluster SSO (JWT)

```sql
SHOW CLUSTER SETTING server.jwt_authentication.enabled;
SHOW CLUSTER SETTING server.jwt_authentication.issuers.configuration;
SHOW CLUSTER SETTING server.jwt_authentication.jwks_auto_fetch.enabled;
```

#### LDAP Authentication

```sql
-- Check HBA rules for any ldap method entries
SHOW CLUSTER SETTING server.host_based_authentication.configuration;
```

Look for lines containing `ldap` in the HBA output.

#### Auto-Provisioning

```sql
SHOW CLUSTER SETTING security.provisioning.jwt.enabled;
SHOW CLUSTER SETTING security.provisioning.ldap.enabled;
```

### Part 1: Cloud Console SSO

Cloud Console SSO enables SAML or OIDC authentication for the CockroachDB Cloud web console, replacing password-based login.

#### 1.1 Check Current SSO Configuration

Check SSO status in the Cloud Console UI (Organization Settings > Authentication). The `ccloud` CLI does not currently expose SSO configuration commands.

#### 1.2a Configure SAML SSO

Follow this section if the user selected **SAML** in Decision 1.

1. Navigate to **Organization Settings > Authentication** in the Cloud Console
2. Select **SAML** as the SSO provider type
3. Configure the SAML connection:
   - Enter the IdP metadata URL or upload the metadata XML
   - Copy the CockroachDB Cloud **ACS URL** and **Entity ID** to your IdP
   - Map IdP attributes to CockroachDB Cloud user fields (email, name)
4. In your IdP, create a SAML 2.0 application:
   - Set the **Single sign-on URL** to the CockroachDB Cloud ACS URL
   - Set the **Audience URI (SP Entity ID)** to the CockroachDB Cloud Entity ID
   - Set **Name ID format** to Email Address
   - Map attributes: `email`, `firstName`, `lastName`
5. Assign users or groups to the SAML application in the IdP

See [configuration steps reference](references/configuration-steps.md) for IdP-specific SAML instructions (Okta, Azure AD).

#### 1.2b Configure OIDC SSO

Follow this section if the user selected **OIDC** in Decision 1.

1. Navigate to **Organization Settings > Authentication** in the Cloud Console
2. Select **OIDC** as the SSO provider type
3. Configure the OIDC connection:
   - Enter the OIDC discovery URL from your IdP (e.g., `https://accounts.google.com/.well-known/openid-configuration`)
   - Enter the **Client ID** and **Client Secret** from your IdP
   - Configure the redirect URI in the IdP to point to CockroachDB Cloud
4. In your IdP, create an OIDC/OAuth 2.0 application:
   - Set **Sign-in redirect URI** to the CockroachDB Cloud redirect URI
   - Grant scopes: `openid`, `profile`, `email`
5. Assign users or groups to the OIDC application in the IdP

See [configuration steps reference](references/configuration-steps.md) for IdP-specific OIDC instructions (Okta, Azure AD, Google Workspace).

#### 1.3 Test SSO Login

1. Open a new browser session (or incognito window)
2. Navigate to the CockroachDB Cloud Console login page
3. Select **Sign in with SSO**
4. Verify redirect to IdP, authenticate, and redirect back to Cloud Console

#### 1.4 Enforce SSO (Disable Password Login)

After verifying SSO works:

1. Navigate to **Organization Settings > Authentication**
2. Enable **Require SSO** to disable password-based login
3. Confirm a break-glass admin account exists (see Safety Considerations)

### Part 2: DB Console SSO (OIDC)

> **This configures SSO for the DB Console web UI only, NOT for SQL client connections.** SQL client SSO is configured separately in Part 3 (JWT) or Part 4 (LDAP/AD).

> **Prerequisite:** Advanced or Enterprise plan required. DB Console SSO is not available on Standard or Basic plans.

DB Console SSO uses OIDC to authenticate users to the CockroachDB DB Console web interface.

#### 2.1 Check Current DB Console SSO Configuration

```sql
SHOW CLUSTER SETTING server.oidc_authentication.enabled;
SHOW CLUSTER SETTING server.oidc_authentication.provider_url;
SHOW CLUSTER SETTING server.oidc_authentication.client_id;
```

#### 2.2 Configure DB Console SSO

```sql
-- Enable OIDC authentication for the DB Console
SET CLUSTER SETTING server.oidc_authentication.enabled = true;

-- Set the OIDC provider URL (your IdP's discovery endpoint)
SET CLUSTER SETTING server.oidc_authentication.provider_url = 'https://your-idp.example.com';

-- Set the client ID registered in your IdP
SET CLUSTER SETTING server.oidc_authentication.client_id = '<client-id>';

-- Set the client secret
SET CLUSTER SETTING server.oidc_authentication.client_secret = '<client-secret>';

-- Configure the claim field used for username mapping
SET CLUSTER SETTING server.oidc_authentication.claim_json_key = 'email';

-- Configure the principal regex (extract username from claim)
SET CLUSTER SETTING server.oidc_authentication.principal_regex = '^([^@]+)';
```

See [configuration steps reference](references/configuration-steps.md) for IdP-specific DB Console SSO setup (Okta, Azure AD).

#### 2.3 Test DB Console SSO

1. Open the DB Console URL in a browser
2. Click **Log in with OIDC**
3. Authenticate with your IdP
4. Verify you are logged into the DB Console

### Part 3: SQL/Cluster SSO (JWT)

SQL/Cluster SSO uses JWT tokens from an IdP to authenticate SQL client connections. This is separate from DB Console SSO (Part 2) — it authenticates `cockroach sql` and application connections, not the web UI.

#### 3.1 Check Current JWT SSO Configuration

```sql
SHOW CLUSTER SETTING server.jwt_authentication.enabled;
SHOW CLUSTER SETTING server.jwt_authentication.issuers.configuration;
SHOW CLUSTER SETTING server.jwt_authentication.jwks_auto_fetch.enabled;
```

#### 3.2 Configure JWT Authentication

```sql
-- Enable JWT authentication for SQL connections
SET CLUSTER SETTING server.jwt_authentication.enabled = true;

-- Configure the JWT issuer(s)
-- Format: JSON object with issuer URL and audience
SET CLUSTER SETTING server.jwt_authentication.issuers.configuration = '{
  "issuers": [
    {
      "issuer": "https://your-idp.example.com",
      "audience": "<client-id>"
    }
  ]
}';

-- Enable automatic JWKS fetching (recommended)
SET CLUSTER SETTING server.jwt_authentication.jwks_auto_fetch.enabled = true;

-- Configure the claim used for SQL username mapping
SET CLUSTER SETTING server.jwt_authentication.claim = 'email';
```

See [configuration steps reference](references/configuration-steps.md) for IdP-specific JWT configuration (Okta, Azure AD, Google).

#### 3.3 Configure Identity Mapping

Map IdP identities (e.g., email addresses) to SQL usernames:

```sql
-- Map user@example.com -> user (strip domain)
SET CLUSTER SETTING server.identity_map.configuration = '
crdb /^(.*)@example\.com$ \1
';
```

#### 3.4 Enable Auto User Provisioning (Optional)

Auto-provision SQL users when they first authenticate via JWT:

```sql
SET CLUSTER SETTING security.provisioning.jwt.enabled = true;
```

When enabled, a SQL user is automatically created for authenticated JWT users who do not yet have an account.

#### 3.5 Test SQL/Cluster SSO

```bash
# Obtain a JWT token from your IdP (method varies by IdP)
# Then connect using the token as the password with JWT auth enabled
cockroach sql --url "postgresql://<username>@<cluster-host>:26257/defaultdb?sslmode=verify-full&options=--crdb:jwt_auth_enabled=true" --external-io-implicit-credentials
```

The JWT token is passed as the password. The `--crdb:jwt_auth_enabled=true` connection option tells CockroachDB to treat the password as a JWT token.

```sql
-- Verify the connection
SELECT current_user();
```

### Part 4: LDAP/AD Authentication

LDAP/AD authentication validates SQL credentials directly against an LDAP directory (Active Directory or OpenLDAP). **Self-hosted only** — not available on CockroachDB Cloud.

> **WARNING — HBA first-match-wins:** HBA rules are evaluated top-to-bottom. The first matching rule is used. A rule like `host all all all ldap ...` matches ALL users from ALL addresses and will prevent password fallback for any user. **Always scope LDAP rules to specific users or roles** to avoid locking out admin accounts.

#### 4.1 Check Current HBA Configuration

```sql
SHOW CLUSTER SETTING server.host_based_authentication.configuration;
```

#### 4.2 Configure LDAP Authentication via HBA

LDAP authentication is configured through HBA (Host-Based Authentication) rules. **Always scope LDAP rules** to specific databases or users — never use `host all all all ldap`.

```sql
-- Configure HBA for LDAP authentication scoped to specific users
-- The 'root' user and other admin users keep password auth
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all root all password
host all admin_user all password
host all all all ldap "ldapserver=ldap.example.com" "ldapport=389" "ldapbasedn=dc=example,dc=com" "ldapsearchattribute=uid" "ldapsearchfilter=(objectClass=inetOrgPerson)" "ldapbinddn=cn=readonly,dc=example,dc=com" "ldapbindpasswd=<bind-password>"
host all all all password
';
```

Key LDAP HBA parameters:
- `ldapserver` — LDAP server hostname
- `ldapport` — LDAP server port (389 for LDAP, 636 for LDAPS)
- `ldapbasedn` — Base DN for user search
- `ldapsearchattribute` — Attribute matching the SQL username (e.g., `uid` for OpenLDAP, `sAMAccountName` for AD)
- `ldapsearchfilter` — **Required.** LDAP filter to narrow the user search (e.g., `(objectClass=inetOrgPerson)`)
- `ldapbinddn` — DN of the service account used for LDAP bind/search
- `ldapbindpasswd` — Password for the bind DN service account

> **Important:** Each HBA option must be quoted as `"key=value"` (the entire key=value pair in one set of quotes).

See [configuration steps reference](references/configuration-steps.md) for Active Directory, OpenLDAP, group mapping, and LDAPS examples.

#### 4.3 Use LDAPS (TLS) for Production

For production environments, always use LDAPS (LDAP over TLS on port 636) to encrypt credentials in transit. Do NOT use `ldaptls=1` — this option is not supported. Instead, use port 636 and configure the custom CA certificate:

```sql
-- Configure the LDAP CA certificate for TLS verification
SET CLUSTER SETTING server.ldap_authentication.domain.custom_ca = '-----BEGIN CERTIFICATE-----
<your-ldap-ca-certificate-pem>
-----END CERTIFICATE-----';

-- Set HBA to use LDAPS (port 636)
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all root all password
host all admin_user all password
host all all all ldap "ldapserver=ldap.example.com" "ldapport=636" "ldapbasedn=dc=example,dc=com" "ldapsearchattribute=uid" "ldapsearchfilter=(objectClass=inetOrgPerson)" "ldapbinddn=cn=readonly,dc=example,dc=com" "ldapbindpasswd=<bind-password>"
host all all all password
';
```

#### 4.4 Configure LDAP Group-to-Role Mapping

LDAP group mapping assigns CockroachDB SQL roles based on LDAP/AD group membership. Group mapping is configured via the `ldapgrouplistfilter` HBA parameter — not via cluster settings.

```sql
-- HBA with group-to-role mapping
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all root all password
host all admin_user all password
host all all all ldap "ldapserver=ad.corp.example.com" "ldapport=636" "ldapbasedn=ou=Users,dc=corp,dc=example,dc=com" "ldapsearchattribute=sAMAccountName" "ldapsearchfilter=(objectClass=user)" "ldapbinddn=cn=crdb-svc,ou=ServiceAccounts,dc=corp,dc=example,dc=com" "ldapbindpasswd=<service-account-password>" "ldapgrouplistfilter=(&(objectClass=group)(member={{.User.DN}}))"
host all all all password
';
```

The LDAP group CN is mapped directly to a SQL role name. The role must already exist in CockroachDB:

```sql
CREATE ROLE IF NOT EXISTS db_admins;
GRANT admin TO db_admins;
```

#### 4.5 Enable Auto User Provisioning (Optional)

Auto-provision SQL users when they first authenticate via LDAP:

```sql
SET CLUSTER SETTING security.provisioning.ldap.enabled = true;
```

#### 4.6 Test LDAP Authentication

```bash
# Test with an LDAP user credential
cockroach sql --url "postgresql://<ldap-username>:<ldap-password>@<cluster-host>:26257/defaultdb?sslmode=verify-full"
```

```sql
-- Verify the user connected successfully
SELECT current_user();

-- If group mapping is enabled, verify role grants
SHOW GRANTS FOR <ldap-username>;
```

### Part 5: SCIM 2.0 on Cloud Console

> **Skip this section** if the user does not need automated user provisioning or does not have an Enterprise plan.

SCIM 2.0 enables automated user provisioning and deprovisioning on the Cloud Console, syncing user lifecycle with your IdP.

#### 5.1 Check Current SCIM Configuration

Check SCIM status in the Cloud Console UI (Organization Settings > Authentication > SCIM). The `ccloud` CLI does not currently expose SCIM configuration commands.

#### 5.2 Enable SCIM Endpoint

1. Navigate to **Organization Settings > Authentication > SCIM** in the Cloud Console
2. Enable the SCIM 2.0 endpoint
3. Copy the **SCIM base URL** and **Bearer token** for IdP configuration

#### 5.3 Configure IdP for SCIM

In your IdP (Okta, Azure AD, etc.):

1. Add a new SCIM provisioning integration
2. Enter the SCIM base URL from step 5.2
3. Enter the Bearer token for authentication
4. Configure provisioning actions:
   - **Create users** — New IdP users are created in CockroachDB Cloud
   - **Update user attributes** — Name and email changes sync
   - **Deactivate users** — Removed IdP users are deactivated in CockroachDB Cloud
5. Assign users or groups to the SCIM integration

See [configuration steps reference](references/configuration-steps.md) for IdP-specific SCIM setup.

#### 5.4 Verify SCIM Provisioning

1. Create a test user in your IdP and assign them to the SCIM integration
2. Check the Cloud Console — the user should appear within a few minutes
3. Remove the test user from the IdP SCIM assignment
4. Verify the user is deactivated in the Cloud Console

## Troubleshooting

### SSO Lockout Recovery

If SSO is enforced and the IdP becomes unavailable or misconfigured:

1. **Use the break-glass account:** Log in with the pre-configured password-based admin account
2. **Disable SSO enforcement:** Navigate to Organization Settings > Authentication and disable "Require SSO"
3. **If no break-glass account exists:** Contact CockroachDB Cloud support to disable SSO enforcement for your organization

**Prevention:** Always create and test a break-glass admin account before enforcing SSO.

### JWT Authentication Errors

**"ERROR: JWT authentication: invalid token"**
- Verify the JWT issuer configuration in `server.jwt_authentication.issuers.configuration`
- Check that the JWT token has not expired
- Verify that `server.jwt_authentication.jwks_auto_fetch.enabled` is `true`
- Inspect the token contents: `echo '<token>' | cut -d. -f2 | base64 -d | jq .`
- Verify the `aud` (audience) claim in the token matches the configured audience

**"ERROR: JWT authentication: issuer not configured"**
- The issuer URL in the token does not match `server.jwt_authentication.issuers.configuration`
- Re-check the issuer URL matches exactly (trailing slashes matter)

### DB Console OIDC Errors

**"OIDC: unable to match principal"**
- The `server.oidc_authentication.principal_regex` does not match the claim value from the token
- Test the regex against the actual claim value:

```sql
SHOW CLUSTER SETTING server.oidc_authentication.principal_regex;
-- Common patterns:
-- Email -> username (strip domain): '^([^@]+)'
-- Full email as username: '^(.+)$'
```

**Complex regex not accepted:**
- CockroachDB uses Go's `regexp` syntax (no lookaheads/lookbehinds)
- Test at https://regex101.com/ with the "Golang" flavor

### LDAP Authentication Errors

**"ERROR: LDAP authentication: unable to bind"**
- Verify `ldapbinddn` and `ldapbindpasswd` are correct
- Check that the bind service account has read access to the user search base
- Test with: `ldapsearch -H ldap://ldap.example.com -D "cn=readonly,dc=example,dc=com" -W -b "dc=example,dc=com" "(uid=testuser)"`

**"ERROR: LDAP authentication: user not found"**
- Verify `ldapbasedn` includes the OU where the user resides
- Check that `ldapsearchattribute` matches the login attribute (`uid` for OpenLDAP, `sAMAccountName` for AD)
- **Check that `ldapsearchfilter` is set** — without it, LDAP user search will fail

**LDAP lockout — all users blocked**
- This happens when an overly broad HBA rule like `host all all all ldap ...` is the first rule and the LDAP server is unreachable, or the LDAP config is wrong
- **Fix:** Ensure `root` and admin users have explicit `password` rules BEFORE any `ldap` rule
- **Recovery:** Connect as `root` using client certificate auth (bypasses HBA) and fix the HBA configuration

**LDAP server unreachable**
- Verify network connectivity from CockroachDB nodes to the LDAP server
- For LDAPS, ensure the CA certificate is configured via `server.ldap_authentication.domain.custom_ca`
- Check firewall rules for port 389 (LDAP) or 636 (LDAPS)

### Azure AD / Entra ID Specific Issues

**Token audience mismatch:**
- Azure AD tokens include an `aud` claim that must match the configured audience
- For JWT SQL SSO: ensure the audience in `server.jwt_authentication.issuers.configuration` matches
- For DB Console OIDC: ensure `server.oidc_authentication.client_id` matches

**Multi-tenant vs single-tenant:**
- For single-tenant: use `https://login.microsoftonline.com/<tenant-id>/v2.0` as the issuer
- For multi-tenant: use `https://login.microsoftonline.com/common/v2.0` (requires additional validation)

### Missing ldapsearchfilter

If LDAP authentication fails with "user not found" errors but the user exists in the directory, check whether `ldapsearchfilter` is included in the HBA rule. This parameter is required and without it the LDAP search may fail silently or return no results.

## Safety Considerations

**SSO misconfiguration can lock out users.** If SSO is enforced and the IdP is down or misconfigured, no one can log in.

**Mitigation — Break-glass account:**
1. Before enforcing SSO, ensure at least one organization admin account uses password authentication
2. Document the break-glass account credentials in a secure vault (e.g., 1Password, HashiCorp Vault)
3. Test the break-glass account periodically to ensure it still works
4. For SQL SSO (JWT or LDAP), keep at least one SQL user with password authentication as a fallback

**HBA first-match-wins — lockout risk:**
HBA rules are evaluated top-to-bottom. The first matching rule wins. This means:
- `host all all all ldap ...` as the first rule will force ALL users through LDAP — including `root`
- If the LDAP server goes down, ALL authentication fails (including admin access)
- **Always place password rules for `root` and admin users BEFORE LDAP rules**

Example of a dangerous configuration:
```
# DANGEROUS — locks out root if LDAP is unavailable
host all all all ldap ...
host all all all password
```

Safe configuration:
```
# SAFE — root and admins always have password fallback
host all root all password
host all admin_user all password
host all all all ldap ...
host all all all password
```

**SCIM risks:**
- **Mass deprovisioning:** If the IdP SCIM assignment is accidentally removed, all provisioned users may be deactivated. Start with a small group before enabling for the full organization.
- **Attribute mapping errors:** Incorrect attribute mapping can create users with wrong names or emails. Test with a single user first.

**LDAP/AD risks:**
- **LDAP server unavailability blocks authentication:** If the LDAP server is down, users authenticating via LDAP cannot connect. Always keep password-based fallback HBA rules for admin users.
- **Use a restricted service account for LDAP bind:** The `ldapbinddn` account should have minimal read-only permissions. Never use a domain admin account.
- **Credential exposure without LDAPS:** LDAP without TLS transmits passwords in cleartext. Always use LDAPS (port 636) with `server.ldap_authentication.domain.custom_ca` in production.

## Rollback

### Disable Cloud Console SSO Enforcement

1. Log in with the break-glass admin account
2. Navigate to **Organization Settings > Authentication**
3. Disable **Require SSO** to re-enable password login

### Disable DB Console SSO (OIDC)

```sql
SET CLUSTER SETTING server.oidc_authentication.enabled = false;
```

### Disable SQL/Cluster SSO (JWT)

```sql
SET CLUSTER SETTING server.jwt_authentication.enabled = false;
```

### Disable LDAP/AD Authentication

```sql
-- Revert HBA to password-only authentication
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all all all password
';
```

### Disable Auto User Provisioning

```sql
-- Disable JWT auto-provisioning
SET CLUSTER SETTING security.provisioning.jwt.enabled = false;

-- Disable LDAP auto-provisioning
SET CLUSTER SETTING security.provisioning.ldap.enabled = false;
```

### Disable SCIM

1. Navigate to **Organization Settings > Authentication > SCIM**
2. Disable the SCIM endpoint
3. Remove the SCIM integration from your IdP

### Remove Identity Mapping

```sql
SET CLUSTER SETTING server.identity_map.configuration = '';
```

## References

**Skill references:**
- [IdP configuration steps](references/configuration-steps.md)

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit
- [enforcing-password-policies](../enforcing-password-policies/SKILL.md) — Strengthen password policies as an alternative to SSO
- [managing-tls-certificates](../managing-tls-certificates/SKILL.md) — Certificate-based authentication as an alternative to SSO

**Official CockroachDB Documentation:**
- [Cloud Console SSO](https://www.cockroachlabs.com/docs/cockroachcloud/cloud-org-sso.html)
- [DB Console SSO](https://www.cockroachlabs.com/docs/stable/sso-db-console.html)
- [Cluster SSO (JWT)](https://www.cockroachlabs.com/docs/stable/sso-sql.html)
- [SCIM Provisioning](https://www.cockroachlabs.com/docs/cockroachcloud/configure-scim-provisioning)
- [Cluster Settings](https://www.cockroachlabs.com/docs/stable/cluster-settings.html)
- [HBA Configuration](https://www.cockroachlabs.com/docs/stable/security-reference/authentication.html)
- [JWT Authentication](https://www.cockroachlabs.com/docs/stable/sso-sql.html)
- [LDAP Authentication](https://www.cockroachlabs.com/docs/stable/ldap-authentication)
- [Authentication Reference](https://www.cockroachlabs.com/docs/stable/security-reference/authentication)
