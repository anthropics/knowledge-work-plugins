# Fastly Account Management

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/account

## Key Concepts

**Token types: personal vs automation.** Personal tokens (created via `POST /tokens`) are tied to the user who creates them and inherit that user's permissions. If the user is deleted or locked, their tokens stop working. Automation tokens (created via `POST /automation-tokens`) are not tied to a user lifecycle -- they survive user account changes and are designed for CI/CD and machine-to-machine use. Automation tokens require a superuser in sudo mode to create.

**IAM model: user groups + service groups + roles.** Access control is built on three primitives. A *user group* contains users (and pending invitations). A *service group* contains services. A *role* defines a set of permissions. You grant access by associating a user group with one or more roles and one or more service groups. Members of the user group then receive the role's permissions on the services in those service groups.

**Superuser vs non-superuser.** Superusers can manage IAM resources, create automation tokens, delete other users, and invite with any role. Non-superusers cannot manage IAM resources, create automation tokens, or delete other users.

**Token scopes are a ceiling, not a floor.** A token's scope limits what it can do, but it can never exceed the permissions of the user (personal tokens) or role (automation tokens) it belongs to.

## Customer / Account

| Action                  | Method   | Endpoint                        |
| ----------------------- | -------- | ------------------------------- |
| Get current customer    | `GET`    | `/current_customer`             |
| Get a customer          | `GET`    | `/customer/{customer_id}`       |
| Update a customer       | `PUT`    | `/customer/{customer_id}`       |
| Delete a customer       | `DELETE` | `/customer/{customer_id}`       |
| List users for customer | `GET`    | `/customer/{customer_id}/users` |

Update request body is form-encoded. Writable fields include `name`, `billing_contact_id`, `billing_network_type` (`public` or `private`), `billing_ref`, `force_2fa`, `force_sso`, `has_account_panel`, `has_improved_events`, `has_openstack_logging`, `has_pci`, `ip_whitelist`, `owner_id`, `phone_number`, `postal_address`, and contact IDs (`legal_contact_id`, `security_contact_id`, `technical_contact_id`). Read-only response fields: `can_upload_vcl`, `can_reset_passwords`, `can_configure_wordpress`, `has_improved_ssl_config`, `has_pci_passwords`.

## Users & Invitations

### Users

| Action                     | Method   | Endpoint                                    |
| -------------------------- | -------- | ------------------------------------------- |
| Get current user           | `GET`    | `/current_user`                             |
| Get a user                 | `GET`    | `/user/{user_id}`                           |
| Create a user (deprecated) | `POST`   | `/user`                                     |
| Update a user              | `PUT`    | `/user/{user_id}`                           |
| Delete a user              | `DELETE` | `/user/{user_id}`                           |
| Update password            | `POST`   | `/current_user/password`                    |
| Request password reset     | `POST`   | `/user/{user_login}/password/request_reset` |

User roles: `user`, `billing`, `engineer`, `tls_viewer`, `tls_admin`, `superuser`. Only superusers can modify other users. Non-superusers can only edit their own account. Two-factor attributes (`two_factor_auth_enabled`, `two_factor_setup_required`) are not editable via this endpoint. The `roles` field accepts an array of role IDs for IAM-based role assignment. Deleting a user requires revoking their API tokens first.

### Invitations

Uses JSON:API format (`application/vnd.api+json`).

| Action            | Method   | Endpoint                       |
| ----------------- | -------- | ------------------------------ |
| List invitations  | `GET`    | `/invitations`                 |
| Create invitation | `POST`   | `/invitations`                 |
| Delete invitation | `DELETE` | `/invitations/{invitation_id}` |

Create payload structure: `data.type` = `"invitation"`, `data.attributes.email`, `data.attributes.roles` (array of role IDs), `data.attributes.limit_services` (boolean), `data.relationships.customer.data` (customer ID/type), and `data.relationships.service_invitations.data` (array of service invitation objects with `permission` and service relationship). Per-service permissions: `full`, `read_only`, `purge_select`, `purge_all`. Superusers can invite with any role. Engineers without per-service limitations can invite new users with the `engineer` or `user` role but cannot modify permissions.

List supports JSON:API pagination: `page[number]`, `page[size]`.

```bash
# Get the current account info
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/current_customer"

# List all users on the account
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/customer/$CUSTOMER_ID/users"
```

## API Tokens (Personal)

Personal tokens are tied to the user who creates them and inherit that user's permission level. Created with username/password authentication (not token auth). Supports 2FA via `Fastly-OTP` header.

| Action               | Method   | Endpoint                         |
| -------------------- | -------- | -------------------------------- |
| List my tokens       | `GET`    | `/tokens`                        |
| List customer tokens | `GET`    | `/customer/{customer_id}/tokens` |
| Create token         | `POST`   | `/tokens`                        |
| Get current token    | `GET`    | `/tokens/self`                   |
| Get token by ID      | `GET`    | `/tokens/{token_id}`             |
| Revoke current token | `DELETE` | `/tokens/self`                   |
| Revoke token by ID   | `DELETE` | `/tokens/{token_id}`             |
| Bulk revoke tokens   | `DELETE` | `/tokens`                        |

Scopes: `global` (default, full access), `purge_select` (purge by URL/surrogate key only), `purge_all` (purge entire service), `global:read` (read-only). Multiple scopes can be combined (space-delimited).

Tokens can be restricted to specific services via `services[]` parameter. Service-limited tokens with `global` or `global:read` scopes can still access non-service endpoints. Limit of 100 active tokens per user (deleted/expired tokens do not count). Optional `expires_at` in ISO 8601 format.

Bulk revoke uses content type `application/vnd.api+json; ext=bulk` with a `data` array of `{id, type: "token"}` objects. Users may only revoke their own tokens; superusers may revoke tokens of others.

Create error codes: `invalid_grant` (bad credentials), `invalid_request` (missing credentials), `invalid_scope` (bad scope), `account_locked`, `2fa.verify` (missing/expired OTP). Format error on `expires_at` returns 422.

```bash
# Get info about the token being used for this request
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/tokens/self"
```

Token creation (`POST /tokens`) returns the `access_token` in the response body. Confirm with the user before executing token-creation commands — the response will contain a credential visible in the LLM conversation context.

## Automation Tokens

Automation tokens are not tied to a specific user account. They are designed for CI/CD pipelines and automated systems. Only superusers can create them (must be in sudo mode). Cannot be created if the account has force SSO or force MFA enabled.

| Action                  | Method   | Endpoint                           |
| ----------------------- | -------- | ---------------------------------- |
| List automation tokens  | `GET`    | `/automation-tokens`               |
| Create automation token | `POST`   | `/automation-tokens`               |
| Get automation token    | `GET`    | `/automation-tokens/{id}`          |
| Revoke automation token | `DELETE` | `/automation-tokens/{id}`          |
| List token services     | `GET`    | `/automation-tokens/{id}/services` |

Create request body (JSON): `name` (required), `role` (required -- `billing`, `engineer`, or `user`), `expires_at` (required, null for no expiry), `scope` (default `global`; also `global:read`, `purge_all`, `purge_select`), `services` (optional array of service IDs, empty for all), `tls_access` (boolean). The `access_token` is only returned in the create response -- store it immediately.

Automation tokens do not trigger or apply to Next-Gen WAF features and scopes. All personal token limitations also apply to automation tokens.

Automation token creation (`POST /automation-tokens`) returns the `access_token` only once in the response body. Confirm with the user before executing — the response will contain a credential visible in the LLM conversation context.

## IAM (Identity & Access Management)

IAM uses a three-part model: **user groups** contain users, **service groups** contain services, and **roles** define permissions. Assign roles and service groups to user groups to grant scoped access. Most IAM management endpoints require superuser tokens. Service groups and user groups use `page`/`per_page` pagination.

### Roles

| Action         | Method | Endpoint                  |
| -------------- | ------ | ------------------------- |
| List roles     | `GET`  | `/iam/v1/roles`           |
| Get role by ID | `GET`  | `/iam/v1/roles/{role_id}` |

Built-in roles: `superuser`, `engineer`, `billing`, `user`, `tls_admin`, `tls_viewer`. Get role supports `?include=permissions` to return the full permission set. List uses cursor-based pagination (`limit`, `cursor`).

### Permissions

| Action           | Method | Endpoint       |
| ---------------- | ------ | -------------- |
| List permissions | `GET`  | `/permissions` |

Each permission has a `scope` (`service` or `account`), a `resource_name` (e.g., TLS), `resource_description`, and a `name`.

### Service Groups

| Action                     | Method   | Endpoint                                      |
| -------------------------- | -------- | --------------------------------------------- |
| List service groups        | `GET`    | `/service-groups`                             |
| Create service group       | `POST`   | `/service-groups`                             |
| Get service group          | `GET`    | `/service-groups/{service_group_id}`          |
| Update service group       | `PATCH`  | `/service-groups/{service_group_id}`          |
| Delete service group       | `DELETE` | `/service-groups/{service_group_id}`          |
| List services in group     | `GET`    | `/service-groups/{service_group_id}/services` |
| Add services to group      | `POST`   | `/service-groups/{service_group_id}/services` |
| Remove services from group | `DELETE` | `/service-groups/{service_group_id}/services` |

Add/remove services body: `{"services": [{"id": "..."},{"id": "..."}]}`.

### User Groups

| Action                            | Method   | Endpoint                                      |
| --------------------------------- | -------- | --------------------------------------------- |
| List user groups                  | `GET`    | `/user-groups`                                |
| Create user group                 | `POST`   | `/user-groups`                                |
| Get user group                    | `GET`    | `/user-groups/{user_group_id}`                |
| Update user group                 | `PATCH`  | `/user-groups/{user_group_id}`                |
| Delete user group                 | `DELETE` | `/user-groups/{user_group_id}`                |
| List members                      | `GET`    | `/user-groups/{user_group_id}/members`        |
| Add members                       | `POST`   | `/user-groups/{user_group_id}/members`        |
| Remove members                    | `DELETE` | `/user-groups/{user_group_id}/members`        |
| List roles in group               | `GET`    | `/user-groups/{user_group_id}/roles`          |
| Add roles to group                | `POST`   | `/user-groups/{user_group_id}/roles`          |
| Remove roles from group           | `DELETE` | `/user-groups/{user_group_id}/roles`          |
| List service groups in user group | `GET`    | `/user-groups/{user_group_id}/service-groups` |
| Add service groups                | `POST`   | `/user-groups/{user_group_id}/service-groups` |
| Remove service groups             | `DELETE` | `/user-groups/{user_group_id}/service-groups` |

Members can be users or invitations. When adding, specify `object: "user"` or `object: "invitation"` in each member entry: `{"members": [{"id": "...", "object": "user"}]}`.

```bash
# List available IAM roles
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/iam/v1/roles"
```

## Billing

### Billing Address

Uses JSON:API format (`application/vnd.api+json`).

| Action                 | Method   | Endpoint                                  |
| ---------------------- | -------- | ----------------------------------------- |
| Get billing address    | `GET`    | `/customer/{customer_id}/billing_address` |
| Add billing address    | `POST`   | `/customer/{customer_id}/billing_address` |
| Update billing address | `PATCH`  | `/customer/{customer_id}/billing_address` |
| Delete billing address | `DELETE` | `/customer/{customer_id}/billing_address` |

Address attributes: `address_1`, `address_2`, `city`, `state`, `country` (ISO 3166-1 two-letter code), `postal_code`, `locality`. Set `skip_verification: true` to bypass address verification. A 400 response with `candidates` means multiple matching addresses were found and one must be selected.

### Invoices

| Action                    | Method | Endpoint                             |
| ------------------------- | ------ | ------------------------------------ |
| List invoices             | `GET`  | `/billing/v3/invoices`               |
| Get invoice by ID         | `GET`  | `/billing/v3/invoices/{invoice_id}`  |
| Get month-to-date invoice | `GET`  | `/billing/v3/invoices/month-to-date` |

List supports `billing_start_date`, `billing_end_date` query params (format `YYYY-MM-DD`). Paginated with `limit` (default 100, max 200) and `cursor`. Sorted by billing start date, newest to oldest. Each invoice includes `transaction_line_items` with `product_name`, `product_group`, `product_line`, `region`, `usage_type`, `rate`, and `units`. Month-to-date may return 202 Accepted.

### Usage Metrics

| Action                          | Method | Endpoint                            |
| ------------------------------- | ------ | ----------------------------------- |
| Get monthly usage metrics       | `GET`  | `/billing/v3/usage-metrics`         |
| Get service-level usage metrics | `GET`  | `/billing/v3/service-usage-metrics` |

Monthly usage requires `start_month` and `end_month` params (format `YYYY-MM`). Maximum period of three months per request. Service-level usage supports optional filters: `product_id` (e.g., `cdn_usage`), `usage_type_name` (e.g., `North America Requests`), `service` (service ID). Paginated with `limit` (default 1000, max 10000) and `cursor`. Only use this API if you do not receive invoices; invoiced customers should use the Invoices API.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                            | URL                                                                                                     |
| --------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Account API reference             | `https://www.fastly.com/documentation/reference/api/account`                                            |
| Tokens API reference              | `https://www.fastly.com/documentation/reference/api/account/tokens`                                     |
| Automation tokens reference       | `https://www.fastly.com/documentation/reference/api/auth-tokens/automation`                             |
| IAM guide                         | `https://www.fastly.com/documentation/guides/account/iam`                                               |
| User management guide             | `https://www.fastly.com/documentation/guides/account/user-access-and-control`                           |
| Invoices API reference            | `https://www.fastly.com/documentation/reference/api/account/invoices`                                   |
| Billing, plans, invoices guide    | `https://www.fastly.com/documentation/guides/account-info/billing`                                      |
| API token creation and management | `https://www.fastly.com/documentation/guides/account-info/user-and-account-management/using-api-tokens` |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.
