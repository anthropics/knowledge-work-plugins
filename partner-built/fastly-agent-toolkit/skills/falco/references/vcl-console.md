# VCL Console with Falco

## Quick start

```bash
# Start interactive console (default: recv scope)
falco console

# Start in specific scope
falco console -s fetch
```

## Key flags

| Flag          | Description                   |
| ------------- | ----------------------------- |
| `-s, --scope` | Initial scope (default: recv) |

## Available scopes

- `recv` - Client request received
- `hash` - Hash generation
- `hit` - Cache hit
- `miss` - Cache miss
- `pass` - Pass to backend
- `fetch` - Backend response received
- `error` - Error handling
- `deliver` - Response delivery
- `log` - Logging
- `pipe` - Pipe to backend

## Console commands

| Command              | Description            |
| -------------------- | ---------------------- |
| `\s, \scope [scope]` | Change execution scope |
| `\h, \help`          | Show help              |
| `\q, \quit`          | Exit console           |

## Usage examples

**Evaluate expressions:**
```
recv> req.url
(STRING) /

recv> req.http.Host
(STRING) localhost

recv> 1 + 2
(INTEGER) 3
```

**Test string operations:**
```
recv> set req.http.Test = "hello"
recv> req.http.Test + " world"
(STRING) hello world
```

**Test conditionals:**
```
recv> if (req.url ~ "^/api") { "api" } else { "web" }
(STRING) web
```

**Change scope:**
```
recv> \s fetch
fetch> beresp.status
(INTEGER) 200
```

## Features

- Auto-completion for VCL keywords and variables
- Command history (up/down arrows)
- Colored output with type information
- Error messages with suggestions

## Common patterns

**Test regex patterns:**
```
recv> "test-string" ~ "test"
(BOOL) true

recv> "test-string" ~ "^test-"
(BOOL) true
```

**Explore available variables:**
```
recv> req.
# Tab completion shows available req.* variables
```
