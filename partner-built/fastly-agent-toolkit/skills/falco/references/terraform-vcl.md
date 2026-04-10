# Terraform VCL Integration with Falco

## Quick start

```bash
# Generate terraform plan and pipe to falco
terraform plan -out planned.out
terraform show -json planned.out | falco terraform

# Specific action (lint is default)
terraform show -json planned.out | falco terraform lint
terraform show -json planned.out | falco terraform test
terraform show -json planned.out | falco terraform stats
terraform show -json planned.out | falco terraform simulate
```

## Workflow

1. Create Terraform plan: `terraform plan -out planned.out`
2. Convert to JSON: `terraform show -json planned.out`
3. Pipe to falco: `| falco terraform [action] [flags]`

## Available actions

| Action     | Description           |
| ---------- | --------------------- |
| `lint`     | Run linting (default) |
| `test`     | Run VCL unit tests    |
| `stats`    | Get VCL statistics    |
| `simulate` | Start local simulator |

## Key flags

Same flags as individual commands:

| Flag                 | Description                   |
| -------------------- | ----------------------------- |
| `-I, --include_path` | Add include path (repeatable) |
| `-v`                 | Show warnings                 |
| `-vv`                | Show all results              |
| `-json`              | JSON output                   |

## Supported Terraform resources

Falco extracts VCL configuration from these Fastly provider resources:

- `fastly_service_vcl` - Main service configuration
- `fastly_service_v1` - Legacy service configuration
- `fastly_service_acl_entries` - ACL entries
- `fastly_service_dictionary_items` - Dictionary items

## Example Terraform configuration

```hcl
resource "fastly_service_vcl" "example" {
  name = "example-service"

  domain {
    name = "example.com"
  }

  backend {
    name    = "origin"
    address = "origin.example.com"
    port    = 443
    ssl     = true
  }

  vcl {
    name    = "main"
    content = file("vcl/main.vcl")
    main    = true
  }

  vcl {
    name    = "helpers"
    content = file("vcl/helpers.vcl")
  }
}
```

## CI/CD integration

```bash
#!/bin/bash
set -e

# Plan terraform changes
terraform plan -out planned.out

# Validate VCL before applying
terraform show -json planned.out | falco terraform -vv

# If validation passes, apply
terraform apply planned.out
```

## Common patterns

**Validate in CI pipeline:**
```bash
terraform show -json planned.out | falco terraform -json > vcl-lint.json
```

**Test VCL from Terraform:**
```bash
terraform show -json planned.out | falco terraform test -I ./tests
```

**Check multiple services:**
```bash
# Falco handles multiple fastly_service_vcl resources in one plan
terraform show -json planned.out | falco terraform -vv
```
