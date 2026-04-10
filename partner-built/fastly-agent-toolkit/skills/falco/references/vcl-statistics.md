# VCL Statistics with Falco

## Quick start

```bash
# Get statistics for VCL project
falco stats /path/to/main.vcl

# With include paths
falco stats -I ./vcl /path/to/main.vcl

# JSON output
falco stats -json /path/to/main.vcl
```

## Key flags

| Flag                 | Description                   |
| -------------------- | ----------------------------- |
| `-I, --include_path` | Add include path (repeatable) |
| `-json`              | Output results as JSON        |
| `-r, --remote`       | Include remote snippets       |

## Output

**Plain text output:**
```
================================================================================
| Main VCL File                                              ./vcl/main.vcl   |
================================================================================
| Included Module Files                                                    12 |
| Total VCL Lines                                                        2847 |
| Subroutines                                                              34 |
| Backends                                                                  5 |
| Tables                                                                    8 |
| Access Control Lists                                                      3 |
| Directors                                                                 2 |
================================================================================
```

**JSON output:**
```json
{
  "main": "./vcl/main.vcl",
  "subroutines": 34,
  "tables": 8,
  "backends": 5,
  "acls": 3,
  "directors": 2,
  "files": 13,
  "lines": 2847
}
```

## Statistics collected

| Metric                | Description                          |
| --------------------- | ------------------------------------ |
| Main VCL File         | Entry point VCL file                 |
| Included Module Files | Number of included VCL files         |
| Total VCL Lines       | Total lines of code across all files |
| Subroutines           | Number of `sub` declarations         |
| Backends              | Number of `backend` declarations     |
| Tables                | Number of `table` declarations       |
| Access Control Lists  | Number of `acl` declarations         |
| Directors             | Number of `director` declarations    |

## Common patterns

**Track codebase growth:**
```bash
falco stats -json -I ./vcl ./vcl/main.vcl >> stats-history.jsonl
```

**Compare branches:**
```bash
git checkout main && falco stats -json main.vcl > main-stats.json
git checkout feature && falco stats -json main.vcl > feature-stats.json
diff main-stats.json feature-stats.json
```
