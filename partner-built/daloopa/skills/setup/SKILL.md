---
name: setup
description: Verify Daloopa MCP connection and show available skills
---

Walk the user through verifying their Daloopa plugin setup. Be conversational and helpful.

## Step 1: Verify Claude Code
Confirm Claude Code is running (if the user is seeing this, it is — tell them they're good).

## Step 2: Verify MCP Connection
This plugin connects to two Daloopa MCP servers:
- **daloopa** (`mcp.daloopa.com/server/mcp`) — Financial data (fundamentals, KPIs, SEC filings)
- **daloopa-docs** (`docs.daloopa.com/mcp`) — Daloopa knowledgebase (API docs, how-tos, usage help)

Run a quick test by calling `discover_companies` with a well-known ticker like "AAPL" to confirm the data MCP server is connected and responding. Show the user the result.

If this fails:
- Check that the `.mcp.json` file is properly configured
- The user may need to restart Claude Code after plugin installation
- On first use, OAuth will open a browser window for Daloopa login

## Step 3: Quick Tour
Tell the user about the available slash commands:

**Analysis Skills** (all prefixed with `/daloopa:`):
- `/daloopa:earnings TICKER` — Full earnings analysis with guidance tracking
- `/daloopa:tearsheet TICKER` — Quick one-page company overview
- `/daloopa:industry TICKER1 TICKER2 ...` — Cross-company comparison
- `/daloopa:bull-bear TICKER` — Bull/bear/base scenario framework
- `/daloopa:guidance-tracker TICKER` — Track management guidance accuracy
- `/daloopa:inflection TICKER` — Auto-detect metric accelerations/decelerations
- `/daloopa:capital-allocation TICKER` — Buybacks, dividends, shareholder yield
- `/daloopa:dcf TICKER` — DCF valuation with sensitivity analysis
- `/daloopa:comps TICKER` — Trading comparables with peer multiples

Each skill generates a styled HTML report saved to the `reports/` directory.

Suggest they try `/daloopa:tearsheet AAPL` as a quick first test.

## Step 4: Note on Enhanced Features
Skills generate HTML reports to the `reports/` directory. For additional output formats (Word documents, Excel models, PDF reports, pitch decks), chart generation, and projection engines, see the full project repo at [github.com/daloopa/investing](https://github.com/daloopa/investing).
