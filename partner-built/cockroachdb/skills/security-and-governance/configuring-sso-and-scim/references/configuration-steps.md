# IdP Configuration Steps for SSO and SCIM

This reference provides IdP-specific configuration steps for setting up SSO and SCIM with CockroachDB.

## Cloud Console SSO — IdP Configuration

### Okta (SAML)

1. In Okta Admin, go to **Applications > Create App Integration**
2. Select **SAML 2.0**
3. Configure:
   - **Single sign-on URL:** `<CockroachDB Cloud ACS URL>` (from Cloud Console SSO settings)
   - **Audience URI (SP Entity ID):** `<CockroachDB Cloud Entity ID>` (from Cloud Console SSO settings)
   - **Name ID format:** Email Address
   - **Application username:** Okta username (email)
4. Map attributes:
   - `email` -> `user.email`
   - `firstName` -> `user.firstName`
   - `lastName` -> `user.lastName`
5. Assign users/groups to the application

### Okta (OIDC)

1. In Okta Admin, go to **Applications > Create App Integration**
2. Select **OIDC - OpenID Connect** and **Web Application**
3. Configure:
   - **Sign-in redirect URIs:** `<CockroachDB Cloud redirect URI>` (from Cloud Console SSO settings)
   - **Sign-out redirect URIs:** `<CockroachDB Cloud logout URI>`
4. Copy the **Client ID** and **Client Secret** to Cloud Console SSO settings
5. Set the discovery URL: `https://<your-okta-domain>/.well-known/openid-configuration`
6. Assign users/groups to the application

### Azure AD (OIDC)

1. In Azure Portal, go to **Azure Active Directory > App registrations > New registration**
2. Configure:
   - **Name:** CockroachDB Cloud SSO
   - **Redirect URI:** `<CockroachDB Cloud redirect URI>` (Web platform)
3. Under **Certificates & secrets**, create a new client secret
4. Copy **Application (client) ID** and **Client secret** to Cloud Console SSO settings
5. Set the discovery URL: `https://login.microsoftonline.com/<tenant-id>/v2.0/.well-known/openid-configuration`
6. Under **API permissions**, grant `openid`, `profile`, `email`

### Google Workspace (OIDC)

1. In Google Cloud Console, go to **APIs & Services > Credentials**
2. Create an **OAuth 2.0 Client ID** (Web application)
3. Configure:
   - **Authorized redirect URIs:** `<CockroachDB Cloud redirect URI>`
4. Copy **Client ID** and **Client Secret** to Cloud Console SSO settings
5. Set the discovery URL: `https://accounts.google.com/.well-known/openid-configuration`

## DB Console SSO (OIDC) — IdP Configuration

These settings configure SSO for the CockroachDB DB Console web UI only. They use the `server.oidc_authentication.*` cluster settings.

### Okta

1. In Okta Admin, create a new **Web** application for DB Console SSO
2. Configure:
   - **Grant type:** Authorization Code
   - **Sign-in redirect URI:** `https://<db-console-host>:<port>/oidc/v1/callback`
3. Under **Security > API > Authorization Servers**, note the issuer URL
4. Configure CockroachDB cluster settings:

```sql
SET CLUSTER SETTING server.oidc_authentication.provider_url = 'https://<your-okta-domain>/oauth2/default';
SET CLUSTER SETTING server.oidc_authentication.client_id = '<client-id>';
SET CLUSTER SETTING server.oidc_authentication.client_secret = '<client-secret>';
SET CLUSTER SETTING server.oidc_authentication.redirect_url = 'https://<db-console-host>:<port>/oidc/v1/callback';
```

### Azure AD

1. In Azure Portal, create a new App registration for DB Console SSO
2. Configure:
   - **Redirect URI:** `https://<db-console-host>:<port>/oidc/v1/callback` (Web platform)
3. Grant API permissions: `openid`, `profile`, `email`
4. Configure CockroachDB cluster settings:

```sql
SET CLUSTER SETTING server.oidc_authentication.provider_url = 'https://login.microsoftonline.com/<tenant-id>/v2.0';
SET CLUSTER SETTING server.oidc_authentication.client_id = '<client-id>';
SET CLUSTER SETTING server.oidc_authentication.client_secret = '<client-secret>';
SET CLUSTER SETTING server.oidc_authentication.redirect_url = 'https://<db-console-host>:<port>/oidc/v1/callback';
```

## SQL/Cluster SSO (JWT) — IdP Configuration

These settings configure JWT-based authentication for SQL client connections. They use the `server.jwt_authentication.*` cluster settings — separate from DB Console OIDC settings.

### Okta

1. In Okta Admin, go to **Security > API > Authorization Servers**
2. Select your authorization server (or create a new one)
3. Note the **Issuer URI** (e.g., `https://<your-okta-domain>/oauth2/default`)
4. Create a custom scope or use default scopes
5. Under the authorization server's **Access Policies**, ensure a policy/rule allows token issuance
6. Configure CockroachDB cluster settings:

```sql
SET CLUSTER SETTING server.jwt_authentication.enabled = true;
SET CLUSTER SETTING server.jwt_authentication.issuers.configuration = '{
  "issuers": [
    {
      "issuer": "https://<your-okta-domain>/oauth2/default",
      "audience": "<client-id>"
    }
  ]
}';
SET CLUSTER SETTING server.jwt_authentication.jwks_auto_fetch.enabled = true;
SET CLUSTER SETTING server.jwt_authentication.claim = 'sub';
```

To obtain a token for testing:
```bash
# Using Okta's token endpoint
curl -X POST "https://<your-okta-domain>/oauth2/default/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=<client-id>&client_secret=<client-secret>&scope=openid"
```

### Azure AD

1. In Azure Portal, go to **App registrations** and create or select an app
2. Under **Expose an API**, set the Application ID URI
3. Under **API permissions**, grant required scopes
4. Note the **Directory (tenant) ID** for the issuer URL
5. Configure CockroachDB cluster settings:

```sql
SET CLUSTER SETTING server.jwt_authentication.enabled = true;
SET CLUSTER SETTING server.jwt_authentication.issuers.configuration = '{
  "issuers": [
    {
      "issuer": "https://login.microsoftonline.com/<tenant-id>/v2.0",
      "audience": "<application-id>"
    }
  ]
}';
SET CLUSTER SETTING server.jwt_authentication.jwks_auto_fetch.enabled = true;
SET CLUSTER SETTING server.jwt_authentication.claim = 'preferred_username';
```

### Google Workspace

1. In Google Cloud Console, go to **APIs & Services > Credentials**
2. Create an **OAuth 2.0 Client ID** or use a service account
3. Configure CockroachDB cluster settings:

```sql
SET CLUSTER SETTING server.jwt_authentication.enabled = true;
SET CLUSTER SETTING server.jwt_authentication.issuers.configuration = '{
  "issuers": [
    {
      "issuer": "https://accounts.google.com",
      "audience": "<client-id>.apps.googleusercontent.com"
    }
  ]
}';
SET CLUSTER SETTING server.jwt_authentication.jwks_auto_fetch.enabled = true;
SET CLUSTER SETTING server.jwt_authentication.claim = 'email';
```

## SCIM 2.0 — IdP Configuration

### Okta

1. In Okta Admin, go to the CockroachDB Cloud application
2. Navigate to **Provisioning > Configure API Integration**
3. Enable API integration
4. Enter:
   - **SCIM connector base URL:** `<SCIM base URL from Cloud Console>`
   - **Unique identifier field:** `email`
   - **Authentication mode:** HTTP Header
   - **Authorization:** Bearer `<SCIM token from Cloud Console>`
5. Under **Provisioning > To App**, enable:
   - Create Users
   - Update User Attributes
   - Deactivate Users
6. Under **Assignments**, assign users/groups

### Azure AD

1. In Azure Portal, go to the CockroachDB Cloud Enterprise Application
2. Navigate to **Provisioning > Get started**
3. Set **Provisioning Mode** to **Automatic**
4. Under **Admin Credentials**, enter:
   - **Tenant URL:** `<SCIM base URL from Cloud Console>`
   - **Secret Token:** `<SCIM token from Cloud Console>`
5. Click **Test Connection** to verify
6. Under **Mappings**, configure attribute mappings:
   - `userPrincipalName` -> `userName`
   - `mail` -> `emails[type eq "work"].value`
   - `displayName` -> `displayName`
7. Start provisioning

### Google Workspace

Google Workspace does not natively support SCIM for third-party apps. Options:
- Use a SCIM bridge (e.g., BetterCloud, Sailpoint)
- Use Google Cloud Identity with an OIDC/SCIM adapter
- Manage users manually or via API automation

## LDAP/AD Authentication — HBA Configuration

> **Important syntax notes:**
> - Each LDAP option in HBA must be quoted as `"key=value"` (entire key=value pair in one set of quotes)
> - Always include `ldapsearchfilter` — it is required for user search to work correctly
> - Do NOT use `ldaptls=1` — this option is not supported. Use port 636 for LDAPS and configure the CA via `server.ldap_authentication.domain.custom_ca`
> - Always scope LDAP rules to specific users to prevent lockout. Place `password` rules for `root` and admin users BEFORE any `ldap` rule.

### Active Directory Example

Active Directory uses `sAMAccountName` as the login attribute and organizes users in OUs.

```sql
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all root all password
host all dba_user all password
host all all all ldap "ldapserver=ad.corp.example.com" "ldapport=636" "ldapbasedn=ou=Users,dc=corp,dc=example,dc=com" "ldapsearchattribute=sAMAccountName" "ldapsearchfilter=(objectClass=user)" "ldapbinddn=cn=crdb-svc,ou=ServiceAccounts,dc=corp,dc=example,dc=com" "ldapbindpasswd=<service-account-password>"
host all all all password
';
```

Notes:
- `sAMAccountName` maps the Windows login name (e.g., `jsmith`) to the SQL username
- The `ldapbinddn` service account needs only **Read** permissions on the user OU
- `ldapsearchfilter=(objectClass=user)` ensures only AD user objects are matched
- Port 636 enables LDAPS — configure the AD CA via `server.ldap_authentication.domain.custom_ca`

### OpenLDAP Example

OpenLDAP typically uses `uid` as the login attribute.

```sql
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all root all password
host all dba_user all password
host all all all ldap "ldapserver=ldap.example.com" "ldapport=636" "ldapbasedn=ou=People,dc=example,dc=com" "ldapsearchattribute=uid" "ldapsearchfilter=(objectClass=inetOrgPerson)" "ldapbinddn=cn=readonly,dc=example,dc=com" "ldapbindpasswd=<bind-password>"
host all all all password
';
```

### LDAP Group-to-Role Mapping

LDAP group-to-role mapping assigns CockroachDB SQL roles based on LDAP/AD group membership. The LDAP group name (CN) is mapped directly to a SQL role name — the role must already exist in CockroachDB.

Group mapping is configured via the `ldapgrouplistfilter` HBA parameter — **not** via cluster settings.

#### Active Directory Group Mapping

```sql
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all root all password
host all dba_user all password
host all all all ldap "ldapserver=ad.corp.example.com" "ldapport=636" "ldapbasedn=ou=Users,dc=corp,dc=example,dc=com" "ldapsearchattribute=sAMAccountName" "ldapsearchfilter=(objectClass=user)" "ldapbinddn=cn=crdb-svc,ou=ServiceAccounts,dc=corp,dc=example,dc=com" "ldapbindpasswd=<service-account-password>" "ldapgrouplistfilter=(&(objectClass=group)(member={{.User.DN}}))"
host all all all password
';
```

Example: If AD user `jsmith` is a member of the `db_admins` group, they receive the `db_admins` SQL role. Create the role first:

```sql
CREATE ROLE IF NOT EXISTS db_admins;
GRANT admin TO db_admins;
```

#### OpenLDAP Group Mapping

```sql
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all root all password
host all dba_user all password
host all all all ldap "ldapserver=ldap.example.com" "ldapport=636" "ldapbasedn=ou=People,dc=example,dc=com" "ldapsearchattribute=uid" "ldapsearchfilter=(objectClass=inetOrgPerson)" "ldapbinddn=cn=readonly,dc=example,dc=com" "ldapbindpasswd=<bind-password>" "ldapgrouplistfilter=(&(objectClass=posixGroup)(memberUid={{.User.Username}}))"
host all all all password
';
```

### LDAPS (TLS) Configuration

LDAPS encrypts all traffic between CockroachDB and the LDAP server. This is required for production environments to prevent credential exposure.

Configure the LDAP server's CA certificate:

```sql
-- Set the custom CA for LDAP TLS verification
SET CLUSTER SETTING server.ldap_authentication.domain.custom_ca = '-----BEGIN CERTIFICATE-----
<your-ldap-ca-certificate-pem>
-----END CERTIFICATE-----';
```

Then use port 636 in the HBA rule (see AD and OpenLDAP examples above).

**Verifying LDAPS connectivity** (run from a CockroachDB node):

```bash
# Test LDAPS connection and check certificate
openssl s_client -connect ldap.example.com:636 -showcerts </dev/null

# Test LDAP search over TLS
ldapsearch -H ldaps://ldap.example.com:636 -D "cn=readonly,dc=example,dc=com" -W -b "dc=example,dc=com" "(uid=testuser)"
```

## Identity Mapping Examples

Identity mapping is used with JWT-based SQL SSO (Part 3) to map IdP identities to SQL usernames.

### Map Email to SQL Username

```sql
-- Map user@example.com -> user (strip domain)
SET CLUSTER SETTING server.identity_map.configuration = '
crdb /^(.*)@example\.com$ \1
';
```

### Map with Domain Prefix

```sql
-- Map user@example.com -> example_user (prefix with domain)
SET CLUSTER SETTING server.identity_map.configuration = '
crdb /^(.*)@(.*)\.com$ \2_\1
';
```

### Multiple Domain Mapping

```sql
-- Map users from multiple domains
SET CLUSTER SETTING server.identity_map.configuration = '
crdb /^(.*)@engineering\.example\.com$ \1
crdb /^(.*)@ops\.example\.com$ ops_\1
';
```

## Notes

- All IdP URLs and credentials should be stored securely
- Test SSO and SCIM with a small group before rolling out organization-wide
- Keep documentation of IdP configuration for disaster recovery
- IdP-specific UI and steps may change — refer to your IdP's official documentation for the most current instructions
- CockroachDB Cloud SSO settings are available in the Cloud Console under Organization Settings > Authentication
- DB Console SSO (`server.oidc_authentication.*`) and SQL/Cluster SSO (`server.jwt_authentication.*`) are independent — configure them separately
