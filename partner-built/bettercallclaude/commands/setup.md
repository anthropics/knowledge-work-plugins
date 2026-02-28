---
description: "Check MCP server status and auto-install servers to Claude Desktop if needed"
---

# BetterCallClaude MCP Server Setup

When this command is invoked, perform the following diagnostic and configuration workflow.

## Step 1: Probe MCP Servers

Attempt to call a tool from each of the 5 MCP servers to determine connectivity. For each server, try listing its available tools or calling a no-op endpoint:

| Server | Test Method |
|--------|-------------|
| bettercallclaude-entscheidsuche | Try calling any `search_decisions` or listing tools |
| bettercallclaude-bge-search | Try calling any `search_bge` or listing tools |
| bettercallclaude-legal-citations | Try calling any `validate_citation` or listing tools |
| bettercallclaude-fedlex-sparql | Try calling any `search_legislation` or listing tools |
| bettercallclaude-onlinekommentar | Try calling any `search_commentary` or listing tools |

## Step 2: Display Status Table

Output the following formatted status report, replacing status indicators based on Step 1 results:

```
==============================================
  BetterCallClaude MCP Server Status
==============================================

  Server                    Status
  ------                    ------
  entscheidsuche            [x] Connected / [ ] Not configured
  bge-search                [x] Connected / [ ] Not configured
  legal-citations           [x] Connected / [ ] Not configured
  fedlex-sparql             [x] Connected / [ ] Not configured
  onlinekommentar           [x] Connected / [ ] Not configured

  Connected: X/5 servers
==============================================
```

## Step 3: Provide Guidance Based on Results

### If all 5 servers are connected:

```
All MCP servers are operational. No setup needed.
BetterCallClaude is running at full capability.
```

Skip to Step 5 (Requirements Check).

### If any servers are missing:

**YOU MUST EXECUTE the steps below in order. Start with Step 3a to detect the environment, then follow the appropriate path. DO NOT skip ahead to the fallback section. DO NOT just show the user text instructions. You must RUN the commands yourself.**

Background: MCP servers in Cowork Desktop run in a sandboxed VM without network access. The setup detects the environment and uses the best available method to install servers into Claude Desktop's host config file.

#### Step 3a: Detect environment (EXECUTE NOW)

Check whether the `mcp__Control_your_Mac__osascript` tool is available in your current tool list. This tool is only present in Cowork Desktop sessions where the "Control your Mac" MCP server is enabled.

- **If `mcp__Control_your_Mac__osascript` IS available**: You are in Cowork Desktop with host Mac access. Proceed to **Step 3b** (osascript install).
- **If `mcp__Control_your_Mac__osascript` is NOT available**: You are in Claude Code CLI or a Cowork session without host access. Skip to **Step 3c** (direct install fallback).

#### Step 3b: Install via osascript — Cowork Desktop (EXECUTE NOW)

This method uses the `mcp__Control_your_Mac__osascript` tool to run shell commands on the HOST Mac, bypassing the Cowork VM sandbox. Execute each sub-step in order. If any sub-step fails, skip to Step 3c.

**Step 3b-i: Get the host $HOME path**

Call the osascript tool with:
```applescript
do shell script "echo $HOME"
```

Store the result as `HOST_HOME` (e.g., `/Users/username`). You will need this for constructing absolute paths.

**Step 3b-ii: Find the plugin's MCP servers on the host**

Call the osascript tool with:
```applescript
do shell script "find ~/.claude -path '*/bettercallclaude*/mcp-servers/entscheidsuche/dist/index.js' 2>/dev/null | sort -V | tail -1"
```

This searches the host's `~/.claude/` directory (which includes the plugin cache) for the entscheidsuche server binary. The result is the full path to one server's `index.js`.

If the result is empty, the plugin cache may not exist on the host yet. Skip to Step 3c.

Extract the base `mcp-servers` directory from the result by removing the `/entscheidsuche/dist/index.js` suffix. Store this as `FOUND_SERVERS_DIR`.

**Step 3b-iii: Copy servers to a stable host location**

The plugin cache path may change between Cowork sessions. Copy servers to a stable location that persists across sessions.

Call the osascript tool with (replace `<FOUND_SERVERS_DIR>` with the actual path from Step 3b-ii):
```applescript
do shell script "mkdir -p ~/.claude/bettercallclaude-servers && cp -R <FOUND_SERVERS_DIR>/* ~/.claude/bettercallclaude-servers/"
```

The stable server path is now: `<HOST_HOME>/.claude/bettercallclaude-servers`

Verify the copy succeeded by calling the osascript tool with:
```applescript
do shell script "ls ~/.claude/bettercallclaude-servers/entscheidsuche/dist/index.js ~/.claude/bettercallclaude-servers/bge-search/dist/index.js ~/.claude/bettercallclaude-servers/legal-citations/dist/index.js ~/.claude/bettercallclaude-servers/fedlex-sparql/dist/index.js ~/.claude/bettercallclaude-servers/onlinekommentar/dist/index.js 2>&1"
```

If any files are missing, skip to Step 3c.

**Step 3b-iv: Read the existing Claude Desktop config**

Call the osascript tool with:
```applescript
do shell script "cat ~/Library/Application\\ Support/Claude/claude_desktop_config.json 2>/dev/null || echo '{}'"
```

Parse the returned JSON string in your context. This is the existing Claude Desktop configuration. **You MUST preserve all existing entries** — only add or update the 5 BetterCallClaude server entries.

**Step 3b-v: Merge the server entries**

In your context, parse the existing config JSON and merge in the 5 server entries. Each entry uses the absolute path with the `HOST_HOME` value from Step 3b-i:

```json
{
  "mcpServers": {
    "...existing entries preserved...",
    "bettercallclaude-entscheidsuche": {
      "command": "node",
      "args": ["<HOST_HOME>/.claude/bettercallclaude-servers/entscheidsuche/dist/index.js"]
    },
    "bettercallclaude-bge-search": {
      "command": "node",
      "args": ["<HOST_HOME>/.claude/bettercallclaude-servers/bge-search/dist/index.js"]
    },
    "bettercallclaude-legal-citations": {
      "command": "node",
      "args": ["<HOST_HOME>/.claude/bettercallclaude-servers/legal-citations/dist/index.js"]
    },
    "bettercallclaude-fedlex-sparql": {
      "command": "node",
      "args": ["<HOST_HOME>/.claude/bettercallclaude-servers/fedlex-sparql/dist/index.js"]
    },
    "bettercallclaude-onlinekommentar": {
      "command": "node",
      "args": ["<HOST_HOME>/.claude/bettercallclaude-servers/onlinekommentar/dist/index.js"]
    }
  }
}
```

Replace `<HOST_HOME>` with the actual value from Step 3b-i (e.g., `/Users/username`). Ensure the merged JSON is valid.

**Step 3b-vi: Write the merged config back**

First, create a backup of the existing config. Call the osascript tool with:
```applescript
do shell script "cp ~/Library/Application\\ Support/Claude/claude_desktop_config.json ~/Library/Application\\ Support/Claude/claude_desktop_config.json.bak.$(date +%Y%m%d-%H%M%S) 2>/dev/null; echo 'backup done'"
```

Then write the merged config. Call the osascript tool with (replace `<MERGED_JSON>` with the actual formatted JSON from Step 3b-v):
```applescript
do shell script "cat > ~/Library/Application\\ Support/Claude/claude_desktop_config.json << 'BCCEOF'\n<MERGED_JSON>\nBCCEOF"
```

**IMPORTANT**: The JSON must be properly formatted with newlines. Use the heredoc syntax exactly as shown. Do not use `echo` or single-line writes for multi-line JSON.

Verify the write succeeded by calling the osascript tool with:
```applescript
do shell script "cat ~/Library/Application\\ Support/Claude/claude_desktop_config.json | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len([k for k in d.get(\"mcpServers\",{}) if k.startswith(\"bettercallclaude\")]))'"
```

The result should be `5`. If it is not, something went wrong — skip to Step 3c.

**Step 3b-vii: Tell the user**

If all sub-steps succeeded, tell the user:

```
MCP servers installed successfully via host Mac access.

5 BetterCallClaude servers have been added to Claude Desktop's config file.
A backup of your previous config was created.

Please restart Claude Desktop, then re-run /bettercallclaude:setup to verify all 5 servers are connected.
```

**STOP HERE** — do not proceed to any further installation steps.

#### Step 3c: Direct install fallback (CLI or no osascript — EXECUTE NOW)

This fallback is used when:
- Running in Claude Code CLI (not Cowork Desktop)
- Running in Cowork but `mcp__Control_your_Mac__osascript` is not available
- Step 3b failed at any sub-step

**Step 3c-i: Locate the MCP server directory**

Run these Bash commands NOW to find the `mcp-servers` directory:

```bash
# Try plugin cache first, then current dir, then common locations
SERVER_DIR=""
for candidate in \
  "${CLAUDE_PLUGIN_ROOT:-}/mcp-servers" \
  "$(find ~/.claude/plugins -type d -name 'mcp-servers' 2>/dev/null | head -1)" \
  "./mcp-servers" \
  "$HOME/Dev/BetterCallClaude_Marketplace/mcp-servers"; do
  if [ -n "$candidate" ] && [ -f "$candidate/entscheidsuche/dist/index.js" ]; then
    SERVER_DIR="$candidate"
    break
  fi
done
echo "SERVER_DIR=$SERVER_DIR"
```

If `SERVER_DIR` is empty, tell the user the plugin may not be fully installed and skip to Step 3d (fallback). Otherwise, verify all 5 servers exist:

```bash
for s in entscheidsuche bge-search legal-citations fedlex-sparql onlinekommentar; do
  [ -f "$SERVER_DIR/$s/dist/index.js" ] && echo "OK: $s" || echo "MISSING: $s"
done
```

If any are missing, skip to Step 3d.

**Step 3c-ii: Try direct config modification**

```bash
# Determine config path
if [ "$(uname)" = "Darwin" ]; then
  CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
else
  CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
fi

# Try direct config modification via Node.js
node -e "
const fs = require('fs');
const path = require('path');
const configPath = process.argv[1];
const serverDir = process.argv[2];
try {
  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  let config = {};
  try { config = JSON.parse(fs.readFileSync(configPath, 'utf8')); } catch(e) {}
  // Backup existing config
  if (Object.keys(config).length > 0) {
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    fs.writeFileSync(configPath + '.bak.' + ts, JSON.stringify(config, null, 2));
    console.log('BACKUP: ' + configPath + '.bak.' + ts);
  }
  // Merge servers
  if (!config.mcpServers) config.mcpServers = {};
  ['entscheidsuche','bge-search','legal-citations','fedlex-sparql','onlinekommentar'].forEach(s => {
    config.mcpServers['bettercallclaude-' + s] = {
      command: 'node',
      args: [path.join(serverDir, s, 'dist', 'index.js')]
    };
  });
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
  const count = Object.keys(config.mcpServers).filter(k => k.startsWith('bettercallclaude')).length;
  console.log('DIRECT_INSTALL_OK: ' + count + ' servers installed');
} catch(e) {
  console.log('DIRECT_INSTALL_FAIL: ' + e.message);
}
" "$CONFIG_PATH" "$SERVER_DIR"
```

**If the output contains `DIRECT_INSTALL_OK`**: Tell the user:

```
MCP servers have been installed directly into Claude Desktop's config file.

Please restart Claude Desktop, then re-run /bettercallclaude:setup to verify all 5 servers are connected.
```

**STOP HERE** — do not proceed to any further installation steps.

**If the output contains `DIRECT_INSTALL_FAIL`**: The config file is not accessible from this environment. Proceed to Step 3d.

#### Step 3d: Fallback (ONLY if Steps 3b and 3c failed)

Only show these alternatives if both Step 3b (osascript) and Step 3c (direct install) failed, or if the user explicitly reports that the automated install did not work:

**Option A — MCPB bundles**: Download and double-click `.mcpb` files from the latest release:

```
  https://github.com/fedec65/BetterCallClaude_Marketplace/releases/latest

Download all 5 .mcpb files and double-click each one:
  - bettercallclaude-entscheidsuche.mcpb
  - bettercallclaude-bge-search.mcpb
  - bettercallclaude-legal-citations.mcpb
  - bettercallclaude-fedlex-sparql.mcpb
  - bettercallclaude-onlinekommentar.mcpb
```

**Option B — Install script**: Run from a Mac Terminal (outside Cowork):

```
git clone https://github.com/fedec65/BetterCallClaude_Marketplace.git
cd BetterCallClaude_Marketplace
bash scripts/install-claude-desktop.sh
```

**Option C — Manual config**: Edit Claude Desktop's config file directly:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

See the CONNECTORS.md file in the plugin for the full JSON configuration.

## Step 4: CLI-Specific Guidance

If the environment appears to be Claude Code CLI (not Cowork Desktop), provide this additional guidance:

```
MCP servers should auto-register from the plugin's .mcp.json file.

Try these steps:
1. Restart Claude Code (quit and reopen)
2. Run /mcp to check registered servers
3. If servers don't appear, run: claude mcp list
4. Re-run /bettercallclaude:setup to verify
```

**How to detect CLI vs Cowork**: If the Bash tool can access the host filesystem (e.g., `ls ~/Library/Application\ Support/Claude/` succeeds on macOS), the user is likely in Cowork Desktop or has Desktop access. If not, they are in CLI-only mode.

## Step 5: Requirements Check

Also verify:
- **Node.js**: Run `node --version` via Bash. Require >= 18.0.0. If not found or too old, warn the user.

## Step 6: Interpret Backend Errors

If a server connects but returns errors during use, consult this diagnostic guide:

| Error Pattern | Likely Cause | Resolution |
|---------------|-------------|------------|
| "table cache_entries does not exist" or similar missing table errors | Database initialization failed — TypeORM `synchronize` was disabled | Update to plugin version 1.3.1+ which fixes this. Re-register the server and restart. |
| SPARQL endpoint timeout or HTTP 5xx from fedlex-sparql | Fedlex service (`fedlex.data.admin.ch`) is temporarily unavailable | Retry later. The server has built-in retry logic (3 attempts, 2s delay). This is an external service issue, not a plugin bug. |
| "ECONNREFUSED" or "ENOTFOUND" from onlinekommentar | `onlinekommentar.ch` API is unreachable — likely blocked by Cowork Desktop's network sandbox | Install at the Desktop level (see Step 3 above). Desktop-level MCP servers run on the host OS and bypass the sandbox. |
| Connection works but no search results | Server is healthy but the query returned no matches | Try broader search terms or different parameters. |

## Notes

- MCP servers are required for live database access (court decisions, legislation, citation verification)
- Without MCP servers, BetterCallClaude operates in **reduced mode** using built-in Swiss law knowledge
- Reduced mode cannot search live databases, verify citation existence, or access current legislation
- All 5 servers are self-contained and require no API keys or external accounts
- The auto-install preserves any existing MCP server configuration in Claude Desktop
- For manual installation, see `scripts/install-claude-desktop.sh` or the CONNECTORS.md documentation

## User Query

$ARGUMENTS
