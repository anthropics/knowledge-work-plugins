# Daloopa Plugin for Claude Code & Claude Cowork

A plugin for Claude Code and Claude Cowork that adds 19 financial analysis skills powered by [Daloopa's](https://daloopa.com) institutional-grade financial data. Works in any project — no Python dependencies or infrastructure needed.

## Prerequisites

- **Claude Code or Claude Cowork** — Install Claude Code with `npm install -g @anthropic-ai/claude-code`, or use [Claude Cowork](https://claude.ai/cowork) directly in the browser
- **Daloopa account** — Sign up at [daloopa.com](https://daloopa.com) (free tier available)

## Installation

```bash
# 1. Add the marketplace
claude plugin marketplace add daloopa/plugin

# 2. Install the plugin
claude plugin install daloopa
```

## Getting Started

```bash
# 1. Verify the connection
/daloopa:setup

# 2. Run your first analysis
/daloopa:tearsheet AAPL
```

On first use, OAuth will open a browser window for Daloopa login. No API keys needed.

## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/daloopa:setup` | Verify MCP connection, show available skills | `/daloopa:setup` |
| `/daloopa:tearsheet` | Quick one-page company overview | `/daloopa:tearsheet MSFT` |
| `/daloopa:earnings` | Full earnings analysis with guidance tracking | `/daloopa:earnings AAPL` |
| `/daloopa:earnings-prep` | Pre-earnings preparation report for the night before | `/daloopa:earnings-prep AAPL` |
| `/daloopa:earnings-flash` | Rapid first-read earnings flash | `/daloopa:earnings-flash AAPL` |
| `/daloopa:guidance-tracker` | Track management guidance accuracy | `/daloopa:guidance-tracker NVDA` |
| `/daloopa:bull-bear` | Bull/bear/base scenario framework | `/daloopa:bull-bear TSLA` |
| `/daloopa:industry` | Cross-company industry comparison | `/daloopa:industry AAPL MSFT GOOG` |
| `/daloopa:inflection` | Auto-detect metric accelerations/decelerations | `/daloopa:inflection AAPL` |
| `/daloopa:capital-allocation` | Buybacks, dividends, shareholder yield | `/daloopa:capital-allocation MSFT` |
| `/daloopa:dcf` | DCF valuation with sensitivity analysis | `/daloopa:dcf AAPL` |
| `/daloopa:comps` | Trading comparables with peer multiples | `/daloopa:comps AAPL` |
| `/daloopa:precedent-transactions` | Precedent M&A transactions with deal multiples | `/daloopa:precedent-transactions AAPL` |
| `/daloopa:supply-chain` | Interactive supply chain dashboard with suppliers and customers | `/daloopa:supply-chain AAPL` |
| `/daloopa:research-note` | Generate a professional Word document research note | `/daloopa:research-note AAPL` |
| `/daloopa:build-model` | Build a multi-tab Excel financial model | `/daloopa:build-model AAPL` |
| `/daloopa:comp-sheet` | Industry comp sheet Excel model with deep operational KPIs | `/daloopa:comp-sheet AAPL` |
| `/daloopa:ib-deck` | Investment banking pitch deck (HTML → PDF) | `/daloopa:ib-deck AAPL` |
| `/daloopa:initiate` | Initiate coverage — research note + Excel model | `/daloopa:initiate AAPL` |

All output is displayed directly in the conversation. You can also just ask Claude anything about a company — the commands are shortcuts for common analysis workflows.

## Data Sources

- **Daloopa MCP** — Institutional-grade financial data from SEC filings (income statements, balance sheets, cash flow, KPIs, guidance, segment breakdowns)
- **Market data** — The plugin uses generic language for market data (price, multiples, peers). Claude will use whatever tools are available in your environment.
- **Consensus estimates** — When available, adds beat/miss and forward valuation context.

Every Daloopa-sourced financial figure includes a citation link back to the original filing.

## Full Project Repo

For enhanced features including:
- Word document research notes (.docx)
- Multi-tab Excel financial models (.xlsx)
- PDF rendering with professional styling
- Investment banking pitch decks (HTML → PDF)
- Chart generation (6 professional chart types)
- Forward financial projections engine

See the full project repo: [github.com/daloopa/investing](https://github.com/daloopa/investing)
