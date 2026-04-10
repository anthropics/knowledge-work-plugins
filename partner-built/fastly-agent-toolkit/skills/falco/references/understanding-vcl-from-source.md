# Understanding VCL by Reading Falco Source Code

Falco is a complete Go implementation of Fastly's VCL 2.x dialect. Its source code is the most detailed and precise reference for how VCL works — more complete than prose documentation because it encodes every variable, function, type rule, and scope constraint as executable code.

**Default local path**: `~/src/falco`

If not available locally, clone it:
```bash
git clone https://github.com/ysugimoto/falco.git ~/src/falco
```

## Table of Contents

- [Understanding VCL by Reading Falco Source Code](#understanding-vcl-by-reading-falco-source-code)
  - [Table of Contents](#table-of-contents)
  - [How to Use This Guide](#how-to-use-this-guide)
  - [Variables](#variables)
    - [Common lookup patterns](#common-lookup-patterns)
  - [Functions](#functions)
    - [Function registry](#function-registry)
    - [Individual function implementations](#individual-function-implementations)
    - [Common lookup patterns](#common-lookup-patterns-1)
  - [Types and Values](#types-and-values)
  - [Request Lifecycle and Scopes](#request-lifecycle-and-scopes)
  - [VCL Syntax and Parsing](#vcl-syntax-and-parsing)
    - [Keywords and operators](#keywords-and-operators)
    - [Parser](#parser)
    - [AST (Abstract Syntax Tree)](#ast-abstract-syntax-tree)
  - [Linting Rules](#linting-rules)
  - [VCL Execution Semantics](#vcl-execution-semantics)
  - [Test Examples — Real VCL Patterns](#test-examples--real-vcl-patterns)
  - [Tips for Agents](#tips-for-agents)

---

## How to Use This Guide

When you need to answer a VCL question, **read the relevant source file directly** rather than guessing. The falco source is structured so that each concern lives in a predictable location. This guide tells you exactly which file to open for each type of question.

**Important**: The source files are Go code, but the VCL knowledge they encode is straightforward to extract — variable names appear as string constants, function signatures are explicit, and scope rules are encoded as switch statements.

---

## Variables

**Location**: `interpreter/variable/`

Each VCL scope has its own file defining which variables are accessible:

| File         | Scope         | Variables accessible in this scope                       |
| ------------ | ------------- | -------------------------------------------------------- |
| `recv.go`    | `vcl_recv`    | `req.*`, `client.*`, request-phase variables             |
| `hash.go`    | `vcl_hash`    | Variables available during hash computation              |
| `hit.go`     | `vcl_hit`     | `obj.*` (cached object), `stale.*`                       |
| `miss.go`    | `vcl_miss`    | `bereq.*` (backend request being constructed)            |
| `pass.go`    | `vcl_pass`    | `bereq.*` variables for pass-through requests            |
| `fetch.go`   | `vcl_fetch`   | `beresp.*` (backend response), `bereq.*`                 |
| `deliver.go` | `vcl_deliver` | `resp.*` (response to client), `obj.*`                   |
| `error.go`   | `vcl_error`   | `obj.*` for synthetic responses                          |
| `log.go`     | `vcl_log`     | Logging-phase variables                                  |
| `all.go`     | All scopes    | Variables available everywhere (`now`, `server.*`, etc.) |

**How to read these files**: Each scope file has a `Get()` method with a switch statement listing every variable name as a string constant. The return type tells you the VCL type. For example:
- `return &value.String{...}` → STRING type
- `return &value.Integer{...}` → INTEGER type
- `return &value.IP{...}` → IP type

**Variable name constants** are defined in `predefined.go` and `constant.go` — these list every `req.http.*`, `beresp.*`, `client.*` etc. variable name.

### Common lookup patterns

**"What type is `client.geo.latitude`?"** → Read `recv.go`, find the constant, look at what value type the Get() method returns.

**"Can I set `beresp.ttl` in `vcl_recv`?"** → Check `recv.go` — if it's not in the switch statement, it's not accessible in that scope. Then check `fetch.go` where `beresp.*` variables live.

**"What variables are read-only?"** → Each scope file also has a `Set()` method. If a variable appears in `Get()` but not `Set()`, it's read-only in that scope.

---

## Functions

**Location**: `interpreter/function/`

### Function registry

The file `builtin_functions.go` is the master registry mapping function names to their implementations. Each function entry specifies:
- The function name (e.g., `"regsuball"`)
- Expected argument types
- Return type
- Which scopes can call it

### Individual function implementations

Each built-in function has its own file in `interpreter/function/builtin/`:

```
builtin/
├── regsuball.go              # regsuball(string, pattern, replacement)
├── regsub.go                 # regsub(string, pattern, replacement)
├── querystring_sort.go       # querystring.sort(url)
├── digest_hash_sha256.go     # digest.hash_sha256(string)
├── crypto_encrypt_base64.go  # crypto.encrypt_base64(...)
├── addr_is_ipv4.go           # addr.is_ipv4(ip)
├── ... (396 files total, one per function)
```

**How to read these files**: Each file contains a Go function that:
1. Validates argument types (tells you what VCL types the function accepts)
2. Implements the behavior (tells you exactly what the function does)
3. Returns a value (tells you the return type)

### Common lookup patterns

**"Does `regsuball` replace all occurrences?"** → Read `builtin/regsuball.go` — the Go implementation shows it uses `regexp.ReplaceAllString`.

**"What arguments does `digest.hash_sha256` take?"** → Read `builtin/digest_hash_sha256.go` — the argument validation at the top of the function shows expected types.

**"What string functions are available?"** → List files: `ls interpreter/function/builtin/ | grep -i string`

---

## Types and Values

**Location**: `interpreter/value/value.go`

VCL has 8 fundamental types:

| VCL Type | Go Struct       | Description             |
| -------- | --------------- | ----------------------- |
| STRING   | `value.String`  | Text values             |
| INTEGER  | `value.Integer` | 64-bit integers         |
| FLOAT    | `value.Float`   | 64-bit floating point   |
| BOOL     | `value.Boolean` | true/false              |
| TIME     | `value.Time`    | Absolute timestamps     |
| RTIME    | `value.RTime`   | Relative time durations |
| IP       | `value.IP`      | IP addresses            |
| BACKEND  | `value.Backend` | Backend references      |

**Type coercion rules** are in this file too — look for conversion methods to understand how VCL implicitly converts between types (e.g., STRING to INTEGER in comparisons).

**Director types** are defined in `interpreter/value/director.go` — random, fallback, hash, client, content hash.

---

## Request Lifecycle and Scopes

**Location**: `interpreter/context/`

- `scope.go` — Defines the 9 VCL subroutine scopes and their relationships
- `context.go` — The execution context carrying request/response state between scopes
- `option.go` — Configuration options for the interpreter

The VCL request lifecycle flows through these scopes:

```
Client Request
    → vcl_recv
        → vcl_hash
            → [cache lookup]
                → vcl_hit (cache hit)
                → vcl_miss (cache miss) → vcl_fetch (got backend response)
                → vcl_pass (uncacheable) → vcl_fetch
        → vcl_error (synthetic response)
    → vcl_deliver (send response to client)
    → vcl_log (after response sent)
```

Each scope determines which variables you can read/write and which `return()` actions are valid (e.g., `return(pass)` is valid in `vcl_recv` but not in `vcl_deliver`).

---

## VCL Syntax and Parsing

**Location**: `token/token.go`, `lexer/`, `parser/`, `ast/`

### Keywords and operators
`token/token.go` defines every VCL keyword, operator, and literal type. This is authoritative for "is X a reserved word in VCL?"

### Parser
The `parser/` directory contains the recursive descent parser:
- `declaration_parser.go` — How `backend`, `acl`, `table`, `director`, `sub` declarations are parsed
- `expression_parser.go` — How VCL expressions (comparisons, string concatenation, etc.) are parsed
- `statement_parser.go` — How `set`, `unset`, `return`, `if/else`, `call`, etc. are parsed

### AST (Abstract Syntax Tree)
The `ast/` directory defines the node types for every VCL construct. Reading these helps understand VCL's grammar — what can appear where.

---

## Linting Rules

**Location**: `linter/`, `docs/rules.md`

The linter encodes 50+ rules for common VCL mistakes:

- `linter/rules.go` — The rule definitions with severity levels
- `docs/rules.md` — Human-readable descriptions of every rule
- `linter/declaration_linter.go` — Rules for backend, ACL, director, table declarations
- `linter/expression_linter.go` — Rules for type mismatches, invalid operators
- `linter/statement_linter.go` — Rules for set/unset/return statements

These rules represent real-world VCL mistakes that Fastly users commonly make — reading them is a fast way to learn VCL best practices.

---

## VCL Execution Semantics

**Location**: `interpreter/`

The interpreter directory shows how VCL actually executes:

| File             | What it shows                                               |
| ---------------- | ----------------------------------------------------------- |
| `interpreter.go` | Main execution loop — how VCL programs run                  |
| `statement.go`   | How each statement type executes (set, unset, if, return)   |
| `expression.go`  | How expressions are evaluated (operators, comparisons)      |
| `director.go`    | How director selection works (random, fallback, hash, etc.) |
| `assign/`        | How variable assignment works per scope                     |
| `coverage.go`    | Code coverage tracking for tests                            |

---

## Test Examples — Real VCL Patterns

**Location**: `examples/testing/`

These are complete working VCL test examples showing real-world patterns:

| Directory             | Pattern demonstrated                                  |
| --------------------- | ----------------------------------------------------- |
| `assertion/`          | All assertion types available in VCL tests            |
| `backend_failover/`   | Testing backend health checks and failover            |
| `base64/`             | Base64 encoding/decoding in VCL                       |
| `default_values/`     | Default variable values and behavior                  |
| `group/`              | Test grouping with describe blocks                    |
| `inject_dictionary/`  | Mocking edge dictionaries in tests                    |
| `inject_variables/`   | Injecting test values for geo, device detection, etc. |
| `mock_subroutine/`    | Mocking subroutines for isolated testing              |
| `override_variables/` | Overriding request/response variables in tests        |
| `rate_limiting/`      | Testing rate limiting and penaltybox logic            |
| `regex/`              | Regular expression patterns in VCL                    |
| `synthetic_response/` | Creating synthetic/error responses                    |
| `table_manipulation/` | Working with VCL tables (edge dictionaries)           |

These examples are especially valuable when writing VCL tests — each directory contains both the VCL source and its corresponding test file showing the testing pattern.

---

## Tips for Agents

1. **Always check the source** before answering VCL questions about variables, functions, or scopes. The source is authoritative; your training data may be outdated.

2. **Use grep/glob on the source** to find specific things:
   ```bash
   # Find a specific variable
   grep -r "CLIENT_GEO" ~/src/falco/interpreter/variable/

   # Find a specific function
   ls ~/src/falco/interpreter/function/builtin/ | grep digest

   # Find what scopes allow a return action
   grep -r "return(pass)" ~/src/falco/interpreter/
   ```

3. **Read the test examples** in `examples/testing/` when you need to show users how to write VCL tests — they're complete, working examples.

4. **Check `docs/rules.md`** when reviewing VCL for potential issues — it lists every linting rule with explanations.

5. **The variable files are your best friend** for scope questions. Each scope file (`recv.go`, `fetch.go`, etc.) is a definitive list of what's accessible.
