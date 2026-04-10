# Testing VCL with Falco

Falco is a VCL development tool that provides linting, simulation, and unit testing.

**Falco documentation**: https://github.com/ysugimoto/falco

## Quick Start

```bash
# Lint VCL
falco lint main.vcl

# Run unit tests
falco test main.vcl

# Start local simulator
falco simulate main.vcl

# Format VCL
falco fmt main.vcl
```

## Linting

```bash
# Basic lint
falco lint main.vcl

# With include paths
falco lint -I . -I ./includes main.vcl

# Verbose output (show warnings)
falco lint -v main.vcl

# JSON output
falco lint -json main.vcl
```

## Local Simulator

```bash
# Start HTTP server on localhost:3124
falco simulate main.vcl

# With debugging TUI
falco simulate -debug main.vcl

# Actual proxy behavior (forwards to origin)
falco simulate --proxy main.vcl

# HTTPS with certificates
falco simulate main.vcl --key key.pem --cert cert.pem
```

## Unit Testing

### Test File Structure

Test files must match `*.test.vcl` pattern. Place test files alongside VCL files:
- `main.vcl` - Main VCL file
- `main.test.vcl` - Test file for main.vcl

### Basic Test

```vcl
// main.test.vcl

// @scope: recv
// @suite: Should set backend
sub test_recv_backend {
  testing.call_subroutine("vcl_recv");
  assert.equal(req.backend, my_origin);
}

// @scope: deliver
// @suite: Should add cache header
sub test_deliver_cache_header {
  testing.call_subroutine("vcl_deliver");
  assert.equal(resp.http.X-Cache, "HIT");
}
```

### Running Tests

```bash
# Run all tests
falco test main.vcl

# With include paths
falco test -I . main.vcl

# Watch mode (rerun on changes)
falco test main.vcl --watch

# With coverage report
falco test main.vcl --coverage

# JSON output
falco test main.vcl -json
```

## Test Annotations

### Scope

Specify which VCL scope the test runs in:

```vcl
// @scope: recv
sub test_recv { }

// @scope: fetch
sub test_fetch { }

// @scope: deliver
sub test_deliver { }

// Multiple scopes
// @scope: recv,pass,miss
sub test_multi { }
```

### Suite Name

```vcl
// @suite: Backend should be selected based on path
sub test_backend_selection { }
```

### Skip Test

```vcl
// @skip
sub test_not_ready { }
```

### Tags

```vcl
// @tag: prod
sub test_prod_only { }

// @tag: !prod
sub test_not_in_prod { }
```

Run with tags:
```bash
falco test main.vcl -t prod
```

## Assertions

### Equality

```vcl
// Strict equal
assert.equal(req.http.Host, "example.com");
assert.not_equal(resp.status, 500);

// Case-insensitive
assert.equal_fold(req.method, "GET");
```

### Boolean

```vcl
assert.true(req.is_ssl);
assert.false(beresp.cacheable);
```

### String Matching

```vcl
// Contains
assert.contains(req.url, "/api/");
assert.not_contains(req.url, "admin");

// Regex match
assert.match(req.url.path, "^/api/v[0-9]+/");
assert.not_match(req.url, "password");

// Starts/ends with
assert.starts_with(req.url.path, "/api/");
assert.ends_with(req.url.path, ".json");
```

### State

```vcl
// Check return state
assert.state(lookup);
assert.not_state(error);

// Check if error was called
assert.error(404);
assert.error(404, "Not Found");
assert.not_error();
```

### Subroutine Calls

```vcl
// Check if subroutine was called
assert.subroutine_called("my_helper");
assert.subroutine_called("my_helper", 2);  // called twice
assert.not_subroutine_called("unused_helper");
```

### Restart

```vcl
assert.restart();
assert.not_restart();
```

### NotSet

```vcl
assert.is_notset(req.http.X-Missing);
```

### JSON Validation

```vcl
assert.is_json(resp.body);
```

## Testing Helpers

### Call Subroutine

```vcl
// @scope: recv
sub test_recv {
  testing.call_subroutine("vcl_recv");
  // assertions...
}
```

### Set Up Request

```vcl
// @scope: recv
sub test_with_setup {
  // Set up request before calling
  set req.http.Host = "api.example.com";
  set req.url = "/api/users?page=1";
  set req.method = "GET";

  testing.call_subroutine("vcl_recv");
  assert.equal(req.backend, api_backend);
}
```

### Override Host

```vcl
// @scope: recv
sub test_with_host {
  testing.override_host("example.com");
  testing.call_subroutine("vcl_recv");
}
```

### Fixed Time

```vcl
// @scope: recv
sub test_time_sensitive {
  testing.fixed_time("2024-01-15 12:00:00");
  testing.call_subroutine("vcl_recv");
  // now returns fixed time
}
```

### Inject Variables

```vcl
// @scope: recv
sub test_with_geo {
  testing.inject_variable("client.geo.country_code", "US");
  testing.call_subroutine("vcl_recv");
  assert.equal(req.http.X-Country, "US");
}
```

### Inject Table Values

```vcl
// @scope: recv
sub test_with_table {
  testing.table_set(redirects, "/old", "/new");
  testing.call_subroutine("vcl_recv");
  assert.error(301);
}
```

### Mock Subroutines

```vcl
sub mock_auth {
  set req.http.X-Authenticated = "true";
}

// @scope: recv
sub test_with_mock {
  testing.mock("check_auth", "mock_auth");
  testing.call_subroutine("vcl_recv");
  assert.equal(req.http.X-Authenticated, "true");
  testing.restore_mock("check_auth");
}
```

### Inspect Variables

```vcl
// @scope: recv
sub test_inspect {
  testing.call_subroutine("vcl_recv");
  // Access variables from any scope
  assert.equal(testing.inspect("obj.status"), 404);
}
```

### Synthetic Body

```vcl
// @scope: error
sub test_synthetic {
  set obj.status = 503;
  testing.call_subroutine("vcl_error");
  assert.contains(testing.synthetic_body, "Service Unavailable");
}
```

### Backend Health

```vcl
// @scope: recv
sub test_failover {
  testing.set_backend_health(primary_backend, false);
  testing.call_subroutine("vcl_recv");
  assert.equal(req.backend, secondary_backend);
}
```

## Grouped Tests

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
  sub test_invalid_token {
    set req.http.Authorization = "Bearer invalid";
    testing.call_subroutine("vcl_recv");
    assert.error(401);
  }

  // @scope: recv
  sub test_missing_token {
    testing.call_subroutine("vcl_recv");
    assert.error(401);
  }
}
```

## Example Test Suite

```vcl
// main.test.vcl

// @scope: recv
// @suite: Should route API requests to API backend
sub test_api_routing {
  set req.url = "/api/v1/users";
  testing.call_subroutine("vcl_recv");
  assert.equal(req.backend, api_backend);
}

// @scope: recv
// @suite: Should route static assets to static backend
sub test_static_routing {
  set req.url = "/static/style.css";
  testing.call_subroutine("vcl_recv");
  assert.equal(req.backend, static_backend);
}

// @scope: recv
// @suite: Should bypass cache for authenticated requests
sub test_auth_bypass {
  set req.http.Authorization = "Bearer token";
  testing.call_subroutine("vcl_recv");
  assert.state(pass);
}

// @scope: fetch
// @suite: Should set TTL for successful responses
sub test_ttl_200 {
  set beresp.status = 200;
  testing.call_subroutine("vcl_fetch");
  assert.equal(beresp.ttl, 3600s);
}

// @scope: fetch
// @suite: Should not cache errors
sub test_no_cache_errors {
  set beresp.status = 500;
  testing.call_subroutine("vcl_fetch");
  assert.equal(beresp.ttl, 0s);
}

// @scope: deliver
// @suite: Should add security headers
sub test_security_headers {
  testing.call_subroutine("vcl_deliver");
  assert.equal(resp.http.X-Content-Type-Options, "nosniff");
  assert.equal(resp.http.X-Frame-Options, "DENY");
}

// @scope: error
// @suite: Should handle 404 errors
sub test_404_error {
  set obj.status = 404;
  testing.call_subroutine("vcl_error");
  assert.contains(testing.synthetic_body, "Not Found");
}
```

## Configuration File

Create `.falco.yml`:

```yaml
include_paths:
  - "."
  - "./includes"

testing:
  timeout: 10  # minutes (default: 10)

  # Override tentative variables
  overrides:
    client.geo.country_code: "US"
    server.datacenter: "TEST"

  # Inject edge dictionary values
  edge_dictionary:
    config:
      feature_flag: "enabled"
```

## Simulator Limitations

Note: The simulator has limitations:
- Backend requests are simulated (no actual network calls)
- Geographic data returns dummy values
- Rate limiting functions return false/0
- Cache is in-memory only, not persistent
- WAF and ESI don't work

See [Falco simulator documentation](https://github.com/ysugimoto/falco/blob/develop/docs/simulator.md) for full details.

## Workflow

```bash
# 1. Write XVCL
vim main.xvcl

# 2. Compile to VCL
uvx xvcl main.xvcl -o main.vcl

# 3. Lint
falco lint -I . main.vcl

# 4. Write tests
vim main.test.vcl

# 5. Run tests
falco test -I . main.vcl

# 6. Run with coverage
falco test -I . main.vcl --coverage

# 7. Debug interactively
falco simulate -debug main.vcl
```
