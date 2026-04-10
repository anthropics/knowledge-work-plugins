# Testing VCL with Falco

## Quick start

```bash
# Run all tests (finds *.test.vcl files)
falco test /path/to/main.vcl

# With include paths
falco test -I ./vcl -I ./tests /path/to/main.vcl

# Watch mode (re-run on file changes)
falco test -w /path/to/main.vcl

# Run specific test files
falco test -f "auth/*.test.vcl" /path/to/main.vcl

# With coverage
falco test --coverage /path/to/main.vcl
```

## Key flags

| Flag                 | Description                                         |
| -------------------- | --------------------------------------------------- |
| `-I, --include_path` | Add include path (repeatable)                       |
| `-f, --filter`       | Glob pattern for test files (default: `*.test.vcl`) |
| `-w, --watch`        | Watch mode - re-run on changes                      |
| `-t, --tag`          | Filter tests by tag (repeatable)                    |
| `--coverage`         | Enable code coverage reporting                      |
| `--timeout`          | Test timeout in minutes (default: 10)               |
| `-request`           | Override request config                             |
| `--max_backends`     | Override max backends limitation                    |
| `--max_acls`         | Override max ACLs limitation                        |
| `-json`              | Output results as JSON                              |

## Writing test files

Test files use `.test.vcl` extension with special syntax:

```vcl
// @scope: recv
// @suite: Authentication tests

sub test_auth_header_present {
    set req.http.Authorization = "Bearer token123";

    testing.call_subroutine("vcl_recv");

    assert.equal(req.http.X-Auth-Status, "valid");
}

sub test_auth_header_missing {
    unset req.http.Authorization;

    testing.call_subroutine("vcl_recv");

    assert.equal(req.http.X-Auth-Status, "missing");
}
```

## Test assertions

```vcl
// Equality
assert.equal(actual, expected);
assert.not_equal(actual, expected);
assert.strict_equal(actual, expected);
assert.not_strict_equal(actual, expected);
assert.equal_fold(actual, expected);  // case-insensitive

// Boolean
assert.true(condition);
assert.false(condition);

// String matching
assert.match(string, regex);
assert.not_match(string, regex);
assert.contains(haystack, needle);
assert.not_contains(haystack, needle);
assert.starts_with(string, prefix);
assert.ends_with(string, suffix);

// State and errors
assert.state(lookup);
assert.not_state(error);
assert.error(404);
assert.error(404, "Not Found");
assert.not_error();

// Subroutine tracking
assert.subroutine_called("my_helper");
assert.not_subroutine_called("unused");

// Other
assert.restart();
assert.not_restart();
assert.is_notset(req.http.X-Missing);
assert.is_json(resp.body);
```

## Testing helpers

```vcl
// Call a subroutine under test
testing.call_subroutine("vcl_recv");

// Set up request state
testing.override_host("example.com");
testing.fixed_time("2024-01-15 12:00:00");
testing.inject_variable("client.geo.country_code", "US");

// Table manipulation
testing.table_set(redirects, "/old", "/new");
testing.table_merge(config, "feature_flag", "enabled");

// Mock subroutines
testing.mock("check_auth", "mock_auth");
testing.restore_mock("check_auth");
testing.restore_all_mocks();

// Backend health
testing.set_backend_health(primary_backend, false);

// Environment and rate
testing.get_env("MY_VAR");
testing.fixed_access_rate(0.5);
```

## Testing variables

```vcl
// Read-only variables available in tests
testing.state                // Return state from return statement
testing.synthetic_body       // Body from synthetic calls
testing.return_value         // Return value from functional subroutines
testing.origin_host_header   // Host header sent to backend
```

## Grouped tests (describe blocks)

```vcl
describe authentication_tests {
  before_recv {
    set req.http.Host = "api.example.com";
  }

  after_recv {
    testing.restore_all_mocks();
  }

  // @scope: recv
  sub test_valid_token {
    set req.http.Authorization = "Bearer valid_token";
    testing.call_subroutine("vcl_recv");
    assert.not_error();
  }

  // @scope: recv
  sub test_missing_token {
    testing.call_subroutine("vcl_recv");
    assert.error(401);
  }
}
```

`before_[scope]` runs before each test in that scope, `after_[scope]` runs after.

## Configuration file

In `.falco.yaml`:

```yaml
testing:
  timeout: 10  # minutes (default: 10)
  filter: "*.test.vcl"
  tags:
    - unit
  overrides:
    client.geo.country_code: "US"
    server.datacenter: "TEST"
  edge_dictionary:
    config_dict:
      feature_flag: "enabled"
```

## Common patterns

**Run tests with specific tag:**
```bash
falco test -t integration /path/to/main.vcl
```

**Development workflow with watch:**
```bash
falco test -w -I ./vcl ./vcl/main.vcl
```

**CI with coverage:**
```bash
falco test --coverage -json main.vcl
```
