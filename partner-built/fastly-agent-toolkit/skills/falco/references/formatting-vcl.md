# Formatting VCL with Falco

## Quick start

```bash
# Format and print to stdout
falco fmt /path/to/file.vcl

# Format and overwrite file
falco fmt -w /path/to/file.vcl

# Format multiple files
falco fmt -w ./vcl/*.vcl

# Format with glob pattern
falco fmt -w ./vcl/**/*.vcl
```

## Key flags

| Flag          | Description                                 |
| ------------- | ------------------------------------------- |
| `-w, --write` | Overwrite input files with formatted output |

Without `-w`, formatted output is printed to stdout.

## Configuration file

Configure formatting style in `.falco.yaml`:

```yaml
format:
  indent_width: 2              # Spaces per indent (default: 2)
  indent_style: "space"        # "space" or "tab"
  line_width: 120              # Max line width (default: 120)
  trailing_comment_width: 1    # Space before trailing comments

  # Statement formatting
  return_statement_parenthesis: true   # return(pass) vs return pass
  else_if: false                       # Use "else if" vs "elsif"
  always_next_line_else_if: false      # Force else-if on new line
  break_compound_conditions: false     # Break compound conditions across lines

  # Declaration formatting
  sort_declaration: false              # Sort declarations alphabetically
  sort_declaration_property: false     # Sort properties in declarations
  align_declaration_property: false    # Align property values

  # Comment formatting
  align_trailing_comment: false        # Align trailing comments
  comment_style: "none"                # "none", "slash", or "sharp"

  # Other
  explicit_string_concat: true         # Use explicit + for string concat (default: true)
  should_use_unset: false              # Use unset vs remove
  indent_case_labels: false            # Indent case labels
```

## Formatting examples

**Before:**
```vcl
sub vcl_recv{
if(req.url~"^/api"){set req.http.X-API="true";
return(pass);}
}
```

**After (default settings):**
```vcl
sub vcl_recv {
  if (req.url ~ "^/api") {
    set req.http.X-API = "true";
    return(pass);
  }
}
```

## Common patterns

**Format all VCL files in project:**
```bash
falco fmt -w ./vcl/**/*.vcl
```

**Check formatting (CI):**
```bash
# Format to temp and compare
falco fmt main.vcl > /tmp/formatted.vcl
diff main.vcl /tmp/formatted.vcl
```

**Format single file to stdout for review:**
```bash
falco fmt main.vcl | less
```
