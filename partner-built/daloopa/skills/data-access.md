# Data Access Reference

All skills that need financial data should follow this reference. Read `design-system.md` (co-located with this file) for formatting, analytical density, and styling conventions.

---

## Section 1: Daloopa MCP Tools

Check your available tools. If you see Daloopa MCP tools (`discover_companies`, `discover_company_series`, `get_company_fundamentals`, `search_documents`), MCP is available.

| Operation | MCP Tool |
|---|---|
| Find company by ticker/name | `discover_companies(keywords=["TICKER"])` → returns `company_id`, `latest_calendar_quarter`, `latest_fiscal_quarter` |
| Find available series/metrics | `discover_company_series(company_id, keywords, periods)` |
| Pull financial data | `get_company_fundamentals(company_id, periods, series_ids)` |
| Search SEC filings | `search_documents(keywords, company_ids, periods)` |

Results come back as structured data you can use directly.

If MCP is not available, tell the user to verify their Daloopa MCP connection by running `/daloopa:setup`.

## Section 1.5: Period Determination

After `discover_companies`, capture `latest_calendar_quarter` and `latest_fiscal_quarter`. Use `latest_calendar_quarter` to calculate all period arrays:

| Skill Need | Calculation |
|---|---|
| Last 4 quarters | Work backward 4Q from `latest_calendar_quarter` |
| Last 8 quarters | Work backward 8Q from `latest_calendar_quarter` |
| Last 10 quarters | Work backward 10Q from `latest_calendar_quarter` |
| Last 4Q + YoY | 8 quarters: latest 4 + same 4 one year prior |
| Document search (recent) | Latest 2 quarters from `latest_calendar_quarter` |

Example: if `latest_calendar_quarter` = "2025Q4", last 8Q = ["2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4"]

**NEVER assume the current calendar date determines the latest available quarter — always use the field returned by `discover_companies`.**

### Fiscal Year Context

Note that `get_company_fundamentals` returns both `calendar_period` and `fiscal_period` for each data point.

- **Single-company analysis** (tearsheet, earnings, guidance-tracker, bull-bear, etc.): Note the company's fiscal year end and use `fiscal_period` labels when presenting data (e.g., "FQ1'26" for Apple's Oct-Dec quarter).
- **Multi-company comparison** (industry, comps): Use `calendar_period` labels to normalize across different fiscal year ends.
- **API input is always calendar quarters** — never pass `latest_fiscal_quarter` values to the API. Fiscal notation (e.g., "FQ2'25") will be misinterpreted. Always calculate period arrays from `latest_calendar_quarter`.

## Section 2: External Market Data

Skills that need market-side data should gather the following:

| Data Need | What to Get |
|---|---|
| **Stock quote** | Current price, market cap, shares outstanding, beta |
| **Trading multiples** | Trailing P/E, Forward P/E, EV/EBITDA, P/S, P/B, dividend yield |
| **Historical prices** | OHLCV data for trend analysis (1-5 years) |
| **Peer multiples** | Side-by-side trading multiples for 5-10 comparable companies |
| **Risk-free rate** | 10Y Treasury yield (for WACC/DCF calculations) |

**Resolution order — use the first available source:**

1. **MCP tools** — Check your available tools for any MCP server that provides market data (stock quotes, multiples, historical prices). Use whatever the user has configured. This is the preferred path because it requires no local dependencies.
2. **Web search** — If no market data MCP is available, use web search to look up current stock price and key multiples.
3. **Defaults** — If no market data source is available at all, use reasonable defaults (beta=1.0, risk-free rate=4.5%) and note the limitation. Proceed with Daloopa fundamentals only.

## Section 3: Consensus Estimates (Optional)

When available, consensus analyst estimates add valuable context. Look for:

| Data Need | Use Case |
|---|---|
| **Consensus revenue / EPS** | Beat/miss analysis vs. Street expectations |
| **Forward estimates (NTM)** | Forward P/E, forward EV/EBITDA for comps |
| **Estimate revisions** | Trend in analyst expectations (up/down/stable) |
| **Price targets** | Consensus target and range for context |

If consensus data is not available, skip these sections and note "consensus data not available" rather than guessing.

## Section 4: Citation Requirements (MANDATORY)

**Every financial figure sourced from Daloopa MUST include a citation link.** This is non-negotiable.

Format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

The `fundamental_id` (or `id`) is returned in every `get_company_fundamentals` response. You must:

1. **Capture the `fundamental_id` at data-pull time** — when you call `get_company_fundamentals`, record the `id` for every value
2. **Carry the ID through to output** — when building tables, prose, or context JSON, attach the citation link to every Daloopa-sourced number
3. **Never drop citation IDs** — if a value came from Daloopa, it gets a link. No exceptions. Computed values (e.g., margins, growth rates) derived from Daloopa figures should cite the underlying inputs
4. **Document citations** — when quoting SEC filings from `search_documents`, link to: `[Document Name](https://marketplace.daloopa.com/document/{document_id})`

If you output a financial figure without a citation, it cannot be verified. Uncitable numbers are useless to an analyst.

## Section 4.5: Firm Attribution

Every output (HTML report) must display "Prepared by {FIRM_NAME}":

- **Default**: "Daloopa"
- **User override**: If the user specifies a firm name in their prompt (e.g., "use firm name Acme Capital"), use that instead
- **NEVER hallucinate a firm name** (Goldman Sachs, Morgan Stanley, JPMorgan, etc.). If no firm name is provided, use "Daloopa". Period.

The HTML report footer template in `design-system.md` includes the `{FIRM_NAME}` placeholder. Replace it with the resolved firm name when generating output.
