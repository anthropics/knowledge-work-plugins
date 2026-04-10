# Linting VCL with Falco

## Quick start

```bash
# Lint a VCL file (default command)
falco /path/to/main.vcl

# With include paths
falco -I ./vcl -I ./includes /path/to/main.vcl

# Verbose output (show warnings)
falco -v /path/to/main.vcl

# Very verbose (show all including info/recommendations)
falco -vv /path/to/main.vcl

# JSON output
falco -json /path/to/main.vcl
```

## Key flags

| Flag                 | Description                                     |
| -------------------- | ----------------------------------------------- |
| `-I, --include_path` | Add include path for VCL imports (repeatable)   |
| `-v`                 | Show warnings in addition to errors             |
| `-vv`                | Show all results including info/recommendations |
| `-json`              | Output results as JSON                          |
| `-r, --remote`       | Fetch snippets from Fastly API                  |
| `--generated`        | Lint Fastly-generated VCL (different rule set)  |
| `--refresh`          | Refresh remote snippet cache                    |

## Exit codes

- `0`: No errors found
- `1`: Errors found or parse failure

## Configuration file

Create `.falco.yaml` in project root:

```yaml
include_paths:
  - ./vcl
  - ./includes

linter:
  verbose: "warning"  # or "info" for all messages
  rules:
    # Override rule severities: ERROR, WARNING, INFO, IGNORE
    acl/syntax: ERROR
    backend/notfound: WARNING
  ignore_subroutines:
    - vcl_pipe  # Skip linting these subroutines
```

## Common patterns

**Lint all VCL in a directory:**
```bash
falco -I ./vcl ./vcl/main.vcl
```

**Check before deployment:**
```bash
falco -vv -I . main.vcl && echo "VCL is valid"
```

**CI integration:**
```bash
falco -json -I . main.vcl > lint-results.json
```
