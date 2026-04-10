# Fastly ACLs

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/security/acl

## Key Concepts

**VCL ACLs are versioned, but their entries are not.** Creating or deleting the ACL container itself requires a draft version that must be activated. However, adding, removing, or modifying individual IP entries within an existing ACL takes effect immediately without a new version. This is by design -- changes take effect immediately without a new version.

**Compute ACLs are a separate system.** They live under `/resources/acls` (not `/service/{id}/version/{v}/acl`), are not tied to service versions, and use a different data model with explicit ALLOW/BLOCK actions per entry.

**ACL entries support IP addresses and CIDR ranges.** For VCL, set `ip` and `subnet` (e.g., `ip: "10.0.0.0"`, `subnet: 8` for a /8). For Compute, use `prefix` in CIDR notation (e.g., `"10.0.0.0/8"`).

**Negation (VCL only).** Set `negated: 1` on a VCL ACL entry to exclude an IP or range from matching. Useful for creating individual exceptions to larger subnets.

**VCL usage.** Reference an ACL by name in VCL with the `~` match operator:

```vcl
# Preserve the real client IP on the first visit (prevents spoofing via X-Forwarded-For)
if (fastly.ff.visits_this_service == 0 && req.restarts == 0) {
  set req.http.Fastly-Client-IP = client.ip;
}

if (client.ip ~ my_blocklist) {
  error 403 "Forbidden";
}
```

## VCL ACLs (Versioned)

ACL containers are versioned resources -- creating or deleting an ACL requires a draft service version that must be activated.

| Action     | Method   | Endpoint                                                    |
| ---------- | -------- | ----------------------------------------------------------- |
| List ACLs  | `GET`    | `/service/{service_id}/version/{version_id}/acl`            |
| Create ACL | `POST`   | `/service/{service_id}/version/{version_id}/acl`            |
| Get ACL    | `GET`    | `/service/{service_id}/version/{version_id}/acl/{acl_name}` |
| Update ACL | `PUT`    | `/service/{service_id}/version/{version_id}/acl/{acl_name}` |
| Delete ACL | `DELETE` | `/service/{service_id}/version/{version_id}/acl/{acl_name}` |

```bash
# Create an ACL on a draft version
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=my_blocklist" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/acl"
```

## VCL ACL Entries (Not Versioned)

ACL entries are **not versioned** -- add, remove, or update IP entries without creating or activating a new service version. Entries reference the ACL by its `acl_id`, not its name.

| Action       | Method   | Endpoint                                                  |
| ------------ | -------- | --------------------------------------------------------- |
| List entries | `GET`    | `/service/{service_id}/acl/{acl_id}/entries`              |
| Create entry | `POST`   | `/service/{service_id}/acl/{acl_id}/entry`                |
| Get entry    | `GET`    | `/service/{service_id}/acl/{acl_id}/entry/{acl_entry_id}` |
| Update entry | `PATCH`  | `/service/{service_id}/acl/{acl_id}/entry/{acl_entry_id}` |
| Delete entry | `DELETE` | `/service/{service_id}/acl/{acl_id}/entry/{acl_entry_id}` |
| Batch update | `PATCH`  | `/service/{service_id}/acl/{acl_id}/entries`              |

```bash
# Add an entry to an ACL
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ip":"192.168.0.1","subnet":16}' \
  "https://api.fastly.com/service/{service_id}/acl/{acl_id}/entry"

# Batch update: create, update, and delete entries in one call
curl -X PATCH -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entries":[
    {"op":"create","ip":"10.0.0.0","subnet":8},
    {"op":"update","id":"{entry_id}","ip":"192.168.1.0","subnet":24},
    {"op":"delete","id":"{entry_id}"}
  ]}' \
  "https://api.fastly.com/service/{service_id}/acl/{acl_id}/entries"
```

List entries supports pagination via `page`, `per_page`, `sort`, and `direction` query parameters.

## Compute ACLs (Separate API)

Compute ACLs are a **completely separate system** from VCL ACLs -- different API paths, different data model, not versioned. Entries use CIDR prefix notation and have an explicit `action` (ALLOW or BLOCK) rather than the negation model of VCL ACLs.

| Action         | Method   | Endpoint                                  |
| -------------- | -------- | ----------------------------------------- |
| List ACLs      | `GET`    | `/resources/acls`                         |
| Create ACL     | `POST`   | `/resources/acls`                         |
| Get ACL        | `GET`    | `/resources/acls/{acl_id}`                |
| Delete ACL     | `DELETE` | `/resources/acls/{acl_id}`                |
| List entries   | `GET`    | `/resources/acls/{acl_id}/entries`        |
| Lookup IP      | `GET`    | `/resources/acls/{acl_id}/entry/{acl_ip}` |
| Update entries | `PATCH`  | `/resources/acls/{acl_id}/entries`        |

```bash
# Look up whether an IP matches a Compute ACL
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/resources/acls/{acl_id}/entry/192.0.2.1"
# Returns: {"prefix":"192.0.2.0/24","action":"block"} or 204 if no match
```

Compute ACL entry updates use the same create/update/delete `op` pattern but entries are identified by `prefix` (CIDR) rather than entry ID, and each entry has an `action` of `ALLOW` or `BLOCK`.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                     | URL                                                                           |
| -------------------------- | ----------------------------------------------------------------------------- |
| ACL API reference          | `https://www.fastly.com/documentation/reference/api/security/acl`             |
| ACL entries API reference  | `https://www.fastly.com/documentation/reference/api/security/acl-entry`       |
| Compute ACLs API reference | `https://www.fastly.com/documentation/reference/api/security/acls-in-compute` |
| ACL guide                  | `https://www.fastly.com/documentation/guides/security/access-control-lists`   |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.
