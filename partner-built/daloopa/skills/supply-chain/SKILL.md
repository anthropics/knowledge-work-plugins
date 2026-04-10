---
name: supply-chain
description: Interactive supply chain dashboard mapping suppliers, customers, and financial interdependencies
argument-hint: TICKER
---

Generate an interactive supply chain dashboard for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

This skill maps the upstream (supplier) and downstream (customer) relationships for a target company, quantifying financial interdependencies in both directions. The output enables an analyst to understand: Who are the critical suppliers and customers? Where is concentration risk on both sides? Which suppliers depend heavily on this company for revenue? Which customers depend on this company's products as critical inputs? How does a shock propagate both upstream (demand shock to suppliers) and downstream (supply disruption to customers)?

## Output Format

The final deliverable is a **single self-contained HTML file** with:
- Embedded CSS and JavaScript (no external dependencies)
- **Tier-grouped Canvas network visualization** — columns: Tier 3 → Tier 2 → Tier 1 → Target → Customers, with connection lines. Clickable nodes open detail overlays.
- **Inventory Health Overview table** — for all suppliers: RM%, WIP%, FG% of total inventory shown as stacked colored bars, plus latest total inventory value
- **Supplier cards grouped by tier** — Tier 1 (Critical/Sole-source), Tier 2 (Major Component), Tier 3 (Specialty) with click-to-expand detail overlays
- **Detail overlays** for each supplier containing:
  - 10-quarter financial table (Revenue, Gross Profit, Net Income, Gross Margin %)
  - 10-quarter inventory breakdown table (Raw Materials, WIP, Finished Goods, Total, RM%, WIP%, FG%)
  - Canvas chart: stacked bar chart of inventory composition with Gross Margin % line overlay
  - Business description and relationship to target company
- **Customer cards grouped by category** — Channel Partners, Enterprise/B2B, End-Market Exposure — with click-to-expand detail overlays matching supplier depth
- **Detail overlays** for each customer containing:
  - 10-quarter financial table (Revenue, Gross Profit, Net Income, Gross Margin %)
  - 10-quarter inventory breakdown table (Raw Materials, WIP, Finished Goods, Total, RM%, WIP%, FG%)
  - Canvas chart: stacked bar chart of inventory composition with Gross Margin % line overlay
  - Business description and relationship to target company
- **Upstream Shock Analysis** section — narrative analysis of how a demand/supply shock to the target company ripples upstream through the supplier chain, with an impact matrix table (Revenue Impact, Margin Impact, Overall Risk per supplier)
- **Downstream Shock Analysis** section — narrative analysis of how a supply disruption at the target company ripples downstream through the customer chain, with an impact matrix table (Input Criticality, Switching Cost, Revenue at Risk, Overall Disruption Risk per customer)
- All financial figures hyperlinked to Daloopa source citations
- A "Download as PDF" button (uses `window.print()`)

**DOM Safety**: All JavaScript MUST use `createElement()` + `textContent` + `appendChild()` for DOM construction. NEVER use `innerHTML`, `outerHTML`, or any HTML-string injection methods. Use helper functions like `ce(tag)`, `ca(el, attrs)`, `cA(parent, children)` to keep code compact.

Save to `reports/{TICKER}_supply-chain.html` and open it with `open`.

---

## RESEARCH WORKFLOW

This is a multi-phase research process. Each phase builds on the previous one. Maximize parallelism across independent API calls.

### Phase 1: Target Company Identification

1. Use `discover_companies` with the ticker symbol to get the `company_id`, `latest_calendar_quarter`, and `latest_fiscal_quarter`. Note the firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5.
2. Pull key financials for the target company:
   - Use `discover_company_series` with keywords: ["revenue", "cost of goods", "gross profit", "operating income", "net income", "total cost"]
   - Calculate 4 quarters backward from `latest_calendar_quarter`. Use `get_company_fundamentals` for those periods to get TTM figures.
3. Note the target company's total COGS / cost of revenue (TTM) — this is the denominator for supplier % calculations.

### Phase 2: Supplier Identification

Run these concurrently to build a comprehensive supplier list:

**2a. Daloopa Document Search:**
- Search keywords: ["supplier", "vendor", "purchase", "procurement"] across last 2-4 quarters
- Search keywords: ["supply agreement", "supply chain", "manufacturing"] across last 2-4 quarters
- Search keywords: ["sole source", "single source", "key supplier"] across last 2-4 quarters
- Search keywords: ["concentration", "significant supplier"] across last 2-4 quarters
- Search the company's 10-K specifically for supplier disclosures

**2b. Web Research:**
- `"[TICKER] [company name] key suppliers list 2025 2026"` — supplier identification
- `"[TICKER] supply chain analysis suppliers"` — analyst/industry reports
- `"[TICKER] 10-K supplier disclosure"` — SEC filing analysis
- `"[company name] supply chain map"` — industry supply chain maps
- `"[company name] supplier concentration risk"` — risk analysis
- `"[company name] who manufactures for [company]"` — manufacturing partners
- `"[company name] component suppliers"` — component-level supply chain

**2c. Industry-Specific Supplier Research:**
For each industry, search for the known critical supply chain relationships:
- **Tech/Hardware**: semiconductor foundries (TSMC, Samsung), display (Samsung, LG, BOE), memory (Samsung, SK Hynix, Micron), sensors/cameras (Sony), glass (Corning), connectors (Amphenol), batteries (CATL, LG Energy), PCB/assembly (Foxconn/Hon Hai, Pegatron, Luxshare)
- **Automotive**: battery (CATL, Panasonic, LG Energy), semiconductors (Infineon, NXP, ON Semi, TI), steel (Nippon, POSCO), tires (Michelin, Bridgestone), glass (AGC, Saint-Gobain)
- **Pharma**: CDMOs (Lonza, Samsung Biologics, Catalent), API suppliers, packaging, distribution
- **Retail**: brand suppliers, logistics (FedEx, UPS), packaging
- **Energy**: equipment (Baker Hughes, Schlumberger), pipe (Tenaris), chemicals

### Phase 3: Supplier Financial Analysis

For each identified supplier (aim for 8-15 key suppliers):

1. **Discover the supplier** using `discover_companies` with their ticker
2. **Pull key financials** from Daloopa:
   - `discover_company_series` with keywords: ["revenue", "net income", "gross margin", "operating margin"]
   - `get_company_fundamentals` for the same 4 calendar quarters as the target company
3. **Determine revenue concentration**:
   - Search Daloopa documents for the supplier: keywords ["[target company name]", "customer", "concentration"]
   - Web search: `"[supplier name] [target company] revenue percentage customer"`
   - Web search: `"[supplier name] 10-K customer concentration"`
   - Many suppliers disclose their top customers in 10-K filings — look for "customers that accounted for 10% or more of revenue"
4. **Determine COGS attribution** (what % of target's costs is this supplier):
   - This is often estimated. Use logic like:
     - If Apple's COGS is ~$200B TTM and TSMC's revenue from Apple is ~$70B, then TSMC = ~35% of COGS
     - Cite the source of each estimate (analyst report, 10-K disclosure, industry research)
   - Flag when this is an estimate vs. a disclosed figure
5. **Business & product description**: What does this supplier provide? Be specific (e.g., "5nm/3nm chip fabrication for A-series and M-series SoCs" not just "semiconductors")

### Phase 3b: Inventory & 10-Quarter Financial Data

For the target company AND each identified supplier (8-15 companies), pull **10 quarters** of data:

1. **Discover inventory series** using `discover_company_series` with keywords: ["raw material", "work in process", "finished good", "inventory", "inventories"]
   - Look for separate RM, WIP, FG series, plus a total inventory series
   - Some companies report "carrying amount" breakdowns — use those for RM/WIP/FG splits
2. **Discover financial series** using `discover_company_series` with keywords: ["revenue", "gross profit", "net income", "gross margin"]
3. **Pull 10 quarters** using `get_company_fundamentals`. Calculate 10 quarters backward from `latest_calendar_quarter`.
   - Example: if latest is Q4'25, pull ["2023Q3", "2023Q4", "2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4"]
4. **Compute inventory composition**: For each quarter, calculate RM%, WIP%, FG% of total inventory
   - High WIP% can signal production bottlenecks
   - Rising FG% can signal demand weakness
   - Rising RM% can signal supply hoarding or procurement buildup
5. **Handle missing data gracefully**: Some suppliers may not report full inventory breakdowns — show what's available and note gaps
6. **Multi-currency handling**: Note the reporting currency for each company (USD, NTD, KRW, EUR, etc.) and display with appropriate units (e.g., "NTD B" for TSMC, "KRW T" for Samsung)

Run inventory and financial series pulls in parallel across all companies.

### Phase 4: Customer / Downstream Identification

The downstream side requires the same research rigor as the upstream side. Run these concurrently to build a comprehensive customer list:

**4a. Daloopa Document Search (target company filings):**
- Search keywords: ["customer", "contract", "agreement", "channel"] across last 2-4 quarters
- Search keywords: ["customer concentration", "significant customer", "major customer"] across last 2-4 quarters — many companies disclose customers >10% of revenue
- Search keywords: ["distribution", "retail partner", "reseller", "licensee"] across last 2-4 quarters
- Search keywords: ["accounts receivable", "contract asset", "deferred revenue"] — concentration in A/R often reveals customer dependency even when not explicitly named
- Search the company's 10-K specifically for customer disclosures and segment end-market breakdowns

**4b. Web Research:**
- `"[TICKER] [company name] major customers list"` — direct customer identification
- `"[TICKER] customer concentration revenue breakdown"` — analyst/industry reports
- `"[TICKER] 10-K customer disclosure"` — SEC filing analysis
- `"[company name] who buys from [company name]"` — downstream identification
- `"[company name] channel partners distributors"` — channel analysis
- `"[company name] end market exposure"` — end-market breakdown

**4c. Industry-Specific Customer Research:**
For each industry, search for the known critical downstream relationships:
- **Semiconductors**: Which OEMs depend on these chips? (e.g., NVDA → hyperscalers MSFT/AMZN/GOOG, QCOM → smartphone OEMs AAPL/Samsung, AVGO → networking OEMs Cisco/Arista)
- **Components/Materials**: Which assemblers or product companies use these inputs? (e.g., Corning → AAPL/Samsung for glass, TSMC → fabless semis NVDA/AMD/AAPL)
- **Software/Platform**: Who builds on this platform? (e.g., MSFT Azure → ISVs, AAPL App Store → developers, Salesforce → SI partners)
- **Consumer products**: Channel partners (carriers, retailers, e-commerce) and enterprise customers
- **Industrial/B2B**: End-market verticals (auto, aerospace, medical, telecom)
- **Pharma/Biotech**: Distributors (McKesson, AmerisourceBergen), PBMs, hospital systems

**4d. Customer Financial Analysis:**

For each identified customer (aim for 6-10 key customers):

1. **Discover the customer** using `discover_companies` with their ticker
2. **Pull key financials** from Daloopa:
   - `discover_company_series` with keywords: ["revenue", "net income", "gross margin", "cost of goods", "operating income"]
   - `get_company_fundamentals` for the same 4 calendar quarters as the target company
3. **Determine revenue attribution** (what % of target's revenue comes from this customer):
   - Search Daloopa documents for the target company: keywords ["[customer name]", "customer", "concentration", "accounts receivable"]
   - Web search: `"[target company] [customer name] revenue percentage"`
   - Web search: `"[target company] 10-K customer concentration"`
   - Many companies disclose customers that account for >10% of revenue in their 10-K
4. **Determine input criticality** (what % of customer's COGS comes from target):
   - This is the inverse of the supplier analysis: if the target sells $X to a customer with $Y in COGS, then input share = X/Y
   - Search for: `"[customer name] [target company] supplier dependence"` or `"[customer name] key inputs components"`
   - Flag whether the target's product is a critical, hard-to-substitute input vs. a commodity with alternatives
5. **Assess switching costs**: Can the customer easily replace the target company's product?
   - **High switching cost**: Custom/proprietary integration, long qualification cycles, regulatory requirements (e.g., TSMC's process node — customers can't easily switch foundries mid-design)
   - **Medium switching cost**: Some integration required but alternatives exist with 6-12 month transition
   - **Low switching cost**: Commodity input, multiple qualified alternatives, short switching timeline
6. **Business & product description**: What does the target supply to this customer? Be specific (e.g., "A17 Pro and M4 SoCs fabricated on TSMC's 3nm process" not just "chips")

### Phase 4e: Customer Inventory & 10-Quarter Financial Data

Mirror Phase 3b for the customer side. For each identified customer (6-10 companies), pull **10 quarters** of data:

1. **Discover inventory series** using `discover_company_series` with keywords: ["raw material", "work in process", "finished good", "inventory", "inventories"]
   - Look for separate RM, WIP, FG series, plus a total inventory series
2. **Discover financial series** using `discover_company_series` with keywords: ["revenue", "gross profit", "net income", "gross margin"]
3. **Pull 10 quarters** using `get_company_fundamentals` with the same 10 calendar quarters as the target company and suppliers (calculated from `latest_calendar_quarter`)
4. **Compute inventory composition**: RM%, WIP%, FG% of total inventory
   - For customers, inventory signals have different meaning:
   - Rising RM% at a customer → they're stocking up on target company's inputs (bullish for target's near-term revenue, but may mean future destocking)
   - Falling RM% → customer is drawing down inventory, may signal reduced orders ahead
   - Rising FG% at a customer → demand for the customer's end product is softening, which will flow back upstream to the target
5. **Handle missing data gracefully**: Some customers may not report inventory breakdowns — show what's available
6. **Multi-currency handling**: Same as suppliers — note reporting currency

Run customer inventory and financial series pulls in parallel, and in parallel with supplier pulls where possible.

### Phase 5: Tier 2 Supplier Research

For the top 3-5 most important Tier 1 suppliers, repeat a lighter version of Phase 2-3:

1. Identify their key suppliers (Tier 2 to the original target)
2. Pull basic financials
3. Determine what they supply and rough revenue/cost relationships
4. This enables the "drill deeper" functionality in the dashboard

### Phase 6: Data Assembly & Synthesis

Before writing HTML, organize all data into this structure:

```
TARGET COMPANY:
  - Name, ticker, description
  - TTM Revenue, COGS, Gross Profit, Net Income, Gross Margin, Op Margin
  - Market cap, stock price (from web)

TIER 1 SUPPLIERS (sorted by estimated % of target COGS, descending):
  For each:
  - Name, ticker, description
  - What they supply (specific products/components)
  - Estimated % of target company COGS (with source/logic)
  - % of supplier revenue from target company (with source)
  - TTM Revenue, Net Income, Gross Margin
  - Market cap
  - Relationship summary (sole source? multi-source? critical?)
  - Their key suppliers (Tier 2) if researched
  - 10-quarter financials: Revenue, Gross Profit, Net Income, GM% (with Daloopa citation IDs)
  - 10-quarter inventory: RM, WIP, FG, Total, RM%, WIP%, FG% (with Daloopa citation IDs)
  - Reporting currency and unit (e.g., USD $M, NTD B, KRW T)

TIER 1 CUSTOMERS (sorted by estimated % of target revenue, descending):
  For each:
  - Name, ticker, description
  - What target company supplies to them (specific products/services)
  - Estimated % of target revenue from this customer (with source/logic)
  - Estimated % of customer COGS from target (input criticality, with source)
  - Switching cost assessment (High/Medium/Low with reasoning)
  - TTM Revenue, COGS, Net Income, Gross Margin
  - Market cap
  - Relationship summary (exclusive? multi-source? long-term contract? spot?)
  - 10-quarter financials: Revenue, Gross Profit, Net Income, GM% (with Daloopa citation IDs)
  - 10-quarter inventory: RM, WIP, FG, Total, RM%, WIP%, FG% (with Daloopa citation IDs)
  - Reporting currency and unit (e.g., USD $M, EUR M, JPY B)

TIER 2 CUSTOMERS (for top 3-5 Tier 1 customers — who do THEY sell to?):
  For each Tier 1 customer, their key customers with basic data
  This traces the value chain forward: Target → Customer → End Market

TIER 2 SUPPLIERS (for top 3-5 Tier 1 suppliers):
  For each Tier 1 supplier, their key suppliers with basic data
```

### Phase 6b: Upstream Shock Analysis (Demand Shock → Suppliers)

Prepare a narrative analysis of how a demand shock at the target company would ripple upstream through the supplier chain:

1. **Classify each supplier by dependency level**:
   - **High dependency**: Target company is >20% of supplier's revenue → severe impact from demand shock
   - **Moderate dependency**: Target is 10-20% of revenue → meaningful but manageable impact
   - **Low dependency**: Target is <10% of revenue → diversified, minimal direct impact

2. **Assess shock propagation for each supplier**:
   - **Revenue Impact** (High/Medium/Low): Based on % of revenue from target
   - **Margin Impact** (High/Medium/Low): Based on operating leverage, fixed costs, ability to find replacement demand
   - **Inventory Risk**: Suppliers with high FG% are more exposed to demand shocks; those with high RM% face supply-side risk
   - **Substitutability**: Can the target switch to alternatives? Can the supplier find other customers?

3. **Build an impact matrix table** with columns: Supplier, Tier, Revenue Dependency, Revenue Impact, Margin Impact, Overall Risk

4. **Write narrative sections**:
   - "Most Exposed Suppliers" — 2-3 paragraphs on suppliers facing highest risk
   - "Resilient Suppliers" — suppliers with diversified revenue bases
   - "Second-Order Effects" — how Tier 2 suppliers would be indirectly affected
   - "Key Monitoring Metrics" — what an analyst should watch (inventory days, order backlog, etc.)

### Phase 6c: Downstream Shock Analysis (Supply Disruption → Customers)

Prepare a narrative analysis of how a supply disruption at the target company (production halt, quality issue, capacity constraint, export ban) would ripple downstream through the customer chain:

1. **Classify each customer by input criticality**:
   - **Critical input**: Target's product is a key component with no drop-in replacement; disruption halts customer production (e.g., TSMC to Apple — no alternative foundry for A-series chips)
   - **Important input**: Target is a significant but not sole supplier; customer can partially substitute with 3-6 month lead time
   - **Supplementary input**: Target provides a non-critical input; customer has multiple qualified alternatives

2. **Assess downstream disruption for each customer**:
   - **Input Criticality** (High/Medium/Low): How essential is the target's product to the customer's operations?
   - **Switching Cost** (High/Medium/Low): How long and expensive to qualify an alternative? Are there contractual lock-ins?
   - **Revenue at Risk**: What portion of the customer's revenue depends on products that use the target's inputs?
   - **Inventory Buffer**: Does the customer hold significant RM inventory of the target's product? How many weeks/months of supply?
   - **Alternative Sources**: Who else could supply this? What's the capacity gap?

3. **Build a downstream impact matrix table** with columns: Customer, Category, Input Criticality, Switching Cost, Revenue at Risk, Inventory Buffer, Overall Disruption Risk

4. **Write narrative sections**:
   - "Most Vulnerable Customers" — customers who would face production disruption or revenue loss
   - "Customers with Alternatives" — those who can substitute away from the target
   - "Pricing Power Implications" — if the target faces a supply constraint, which customers have the leverage to secure allocation vs. which get cut first?
   - "Channel Inventory Signals" — what customer inventory levels (especially RM%) tell you about near-term order patterns for the target company
   - "Second-Order Downstream Effects" — how end consumers or Tier 2 customers would be affected

---

## HTML TEMPLATE & DESIGN SYSTEM

Start from the HTML Report Template in `../design-system.md` (copy the full `<style>` block). Then add the following **additional CSS** for interactive dashboard components. Use the design system's color palette throughout.

### Design Principles
- Follow `../design-system.md` for color palette, typography, and table conventions
- **Information density**: Show data compactly but with clear hierarchy
- **Interactive but not flashy**: Smooth transitions, click-to-expand, no animations for animation's sake

### Core CSS

Start with the full CSS from `../design-system.md`, then append these dashboard-specific styles:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[TICKER] Supply Chain Dashboard</title>
<style>
  /* === PASTE FULL CSS FROM design-system.md HTML Report Template HERE === */

  /* === DASHBOARD-SPECIFIC EXTENSIONS BELOW === */

  @media print {
    .no-print { display: none !important; }
    .interactive { pointer-events: none; }
    @page { margin: 0.5in; size: landscape; }
  }

  :root {
    /* Extended palette for dashboard components — supplements design-system.md vars */
    --bg: var(--light-gray);
    --surface: #ffffff;
    --border: var(--mid-gray);
    --border-light: var(--light-gray);
    --text-primary: var(--near-black);
    --text-secondary: var(--dark-gray);
    --text-tertiary: #8a8a85;
    --accent: var(--steel-blue);
    --green-bg: #f0f9f2;
    --red-bg: #fef2f2;
    --amber: #92600a;
    --amber-bg: #fefce8;
    --blue-bg: #eff6ff;
    --node-supplier: var(--mid-gray);
    --node-customer: #dde8f0;
    --node-target: var(--navy);
    --sans: "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    --mono: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
  }

  /* Layout */
  .page-header {
    background: var(--surface);
    border-bottom: 3px solid var(--navy);
    padding: 24px 40px 16px;
  }
  .page-header h1 {
    font-size: 28px;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: -0.5px;
    line-height: 1.2;
  }
  .page-header .subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin-top: 4px;
  }
  .page-header .dateline {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 8px;
    font-family: var(--mono);
  }

  .container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 24px 40px;
  }

  /* Section Headers */
  h2 {
    font-family: var(--sans);
    font-size: 20px;
    font-weight: 700;
    margin: 32px 0 16px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--mid-gray);
    letter-spacing: -0.3px;
    color: var(--navy);
  }
  h3 {
    font-family: var(--sans);
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--steel-blue);
    margin: 20px 0 10px;
  }

  /* KPI Bar */
  .kpi-bar {
    display: flex;
    gap: 0;
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    background: var(--surface);
    margin: 16px 0;
  }
  .kpi-item {
    flex: 1;
    padding: 12px 16px;
    border-right: 1px solid var(--border-light);
    text-align: center;
  }
  .kpi-item:last-child { border-right: none; }
  .kpi-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-tertiary);
    font-weight: 600;
  }
  .kpi-value {
    font-size: 18px;
    font-weight: 700;
    margin-top: 2px;
    font-variant-numeric: tabular-nums;
  }
  .kpi-sub {
    font-size: 11px;
    color: var(--text-tertiary);
    margin-top: 1px;
  }

  /* Supply Chain Visualization */
  .chain-view {
    display: flex;
    gap: 24px;
    align-items: flex-start;
    margin: 20px 0;
    overflow-x: auto;
    padding-bottom: 16px;
  }
  .chain-column {
    min-width: 280px;
    flex-shrink: 0;
  }
  .chain-column-header {
    font-family: var(--sans);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-tertiary);
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
    text-align: center;
  }
  .chain-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-tertiary);
    font-size: 24px;
    min-width: 40px;
    padding-top: 40px;
    flex-shrink: 0;
  }

  /* Company Cards */
  .company-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px 16px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .company-card:hover {
    border-color: var(--text-secondary);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .company-card.target-card {
    background: var(--navy);
    color: white;
    border-color: var(--navy);
  }
  .company-card.target-card .card-ticker { color: rgba(255,255,255,0.7); }
  .company-card.target-card .card-metric-label { color: rgba(255,255,255,0.5); }
  .company-card.target-card .card-metric-value { color: white; }
  .company-card.target-card .card-desc { color: rgba(255,255,255,0.7); }
  .company-card.expanded { border-color: var(--steel-blue); box-shadow: 0 2px 12px rgba(74,111,165,0.15); }
  .company-card.supplier-card { border-left: 3px solid var(--node-supplier); }
  .company-card.customer-card { border-left: 3px solid var(--node-customer); }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  .card-name {
    font-family: var(--sans);
    font-size: 16px;
    font-weight: 700;
    line-height: 1.2;
  }
  .card-ticker {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-tertiary);
    margin-top: 2px;
  }
  .card-badge {
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 3px;
    white-space: nowrap;
  }
  .badge-pct-high { background: var(--red-bg); color: var(--red); }
  .badge-pct-med { background: var(--amber-bg); color: var(--amber); }
  .badge-pct-low { background: var(--green-bg); color: var(--green); }

  .card-supplies {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 6px;
    line-height: 1.4;
  }

  .card-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--border-light);
  }
  .card-metric-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    color: var(--text-tertiary);
  }
  .card-metric-value {
    font-size: 13px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }

  .card-desc {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 8px;
    line-height: 1.45;
  }

  /* Expanded Detail Panel */
  .detail-panel {
    display: none;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border-light);
  }
  .company-card.expanded .detail-panel { display: block; }

  .detail-section {
    margin-bottom: 14px;
  }
  .detail-section h4 {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-tertiary);
    margin-bottom: 6px;
  }

  .relationship-bar {
    height: 8px;
    background: var(--border-light);
    border-radius: 4px;
    overflow: hidden;
    margin: 4px 0;
  }
  .relationship-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s;
  }
  .fill-red { background: var(--red); }
  .fill-amber { background: var(--amber); }
  .fill-green { background: var(--green); }
  .fill-blue { background: var(--accent); }

  /* Drill-down button */
  .drill-btn {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    color: var(--accent);
    cursor: pointer;
    padding: 4px 0;
    border: none;
    background: none;
    font-family: var(--sans);
  }
  .drill-btn:hover { text-decoration: underline; }

  /* Concentration Table */
  .conc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin: 12px 0;
  }
  .conc-table th {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-tertiary);
    font-weight: 600;
    text-align: left;
    padding: 6px 10px;
    border-bottom: 2px solid var(--border);
    background: var(--bg);
  }
  .conc-table th:not(:first-child) { text-align: right; }
  .conc-table td {
    padding: 8px 10px;
    border-bottom: 1px solid var(--border-light);
    font-variant-numeric: tabular-nums;
  }
  .conc-table td:not(:first-child) { text-align: right; }
  .conc-table tr:hover { background: var(--blue-bg); }
  .conc-table .row-total {
    font-weight: 700;
    border-top: 2px solid var(--border);
    background: var(--bg);
  }

  /* Risk indicator */
  .risk-tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 3px;
  }
  .risk-high { background: var(--red-bg); color: var(--red); }
  .risk-med { background: var(--amber-bg); color: var(--amber); }
  .risk-low { background: var(--green-bg); color: var(--green); }

  /* Tabs for switching views */
  .tab-bar {
    display: flex;
    gap: 0;
    border-bottom: 2px solid var(--border);
    margin-bottom: 20px;
  }
  .tab {
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-tertiary);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: color 0.15s, border-color 0.15s;
    font-family: var(--sans);
    background: none;
    border-top: none;
    border-left: none;
    border-right: none;
  }
  .tab:hover { color: var(--text-primary); }
  .tab.active {
    color: var(--text-primary);
    border-bottom-color: var(--text-primary);
  }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* Methodology / Source Notes */
  .methodology-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.5;
  }
  .methodology-box h4 {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-tertiary);
    margin-bottom: 8px;
  }

  /* Links & References */
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  .source-tag {
    font-size: 9px;
    color: var(--text-tertiary);
    font-style: italic;
  }

  /* Footer */
  .page-footer {
    margin-top: 40px;
    padding: 16px 0;
    border-top: 3px solid var(--navy);
    font-size: 11px;
    color: var(--text-tertiary);
    text-align: center;
  }

  /* Print button */
  .dl-btn {
    display: inline-block;
    padding: 10px 24px;
    background: var(--navy);
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    font-family: var(--sans);
  }
  .dl-btn:hover { background: var(--steel-blue); }

  /* Two-column layout */
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  @media (max-width: 800px) {
    .two-col { grid-template-columns: 1fr; }
    .chain-view { flex-direction: column; }
    .chain-arrow { transform: rotate(90deg); padding-top: 0; }
  }
</style>
</head>
```

### Core JavaScript Pattern

The dashboard uses vanilla JavaScript for interactivity. Include these functions in a `<script>` tag at the end of the body:

```javascript
<script>
// Tab switching
function switchTab(tabId) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
  document.getElementById(tabId).classList.add('active');
}

// Card expand/collapse
function toggleCard(cardId) {
  const card = document.getElementById(cardId);
  card.classList.toggle('expanded');
}

// Navigate to tier 2 view for a specific supplier
function drillDown(companyTicker) {
  // Switch to the tier-2 tab and scroll to the relevant section
  switchTab('tier2');
  const section = document.getElementById('tier2-' + companyTicker);
  if (section) {
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    section.style.outline = '2px solid var(--accent)';
    setTimeout(() => { section.style.outline = 'none'; }, 2000);
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Set first tab active
  const firstTab = document.querySelector('.tab');
  if (firstTab) firstTab.click();
});
</script>
```

---

## DOCUMENT STRUCTURE

The HTML document has these sections. Every section is mandatory.

### Section 1: Print Button Bar
```html
<div class="no-print" style="text-align:center; padding:16px; background:var(--surface); border-bottom:1px solid var(--border);">
  <button class="dl-btn" onclick="window.print()">Download as PDF</button>
  <span style="font-size:12px; color:var(--text-tertiary); margin-left:12px;">or Cmd+P &rarr; Save as PDF</span>
</div>
```

### Section 2: Page Header
```html
<div class="page-header">
  <h1>[TICKER] &mdash; Supply Chain Map</h1>
  <div class="subtitle">[Full Company Name] &middot; Interactive Supply Chain Analysis</div>
  <div class="dateline">Prepared [Date] &middot; Data sourced from <a href="https://daloopa.com">Daloopa</a> &middot; TTM through [Latest Quarter]</div>
</div>
```

### Section 3: Target Company KPI Bar
Show 6 KPIs for the target company:
```html
<div class="container">
  <div class="kpi-bar">
    <div class="kpi-item"><div class="kpi-label">TTM Revenue</div><div class="kpi-value">$XXB</div></div>
    <div class="kpi-item"><div class="kpi-label">TTM COGS</div><div class="kpi-value">$XXB</div></div>
    <div class="kpi-item"><div class="kpi-label">Gross Margin</div><div class="kpi-value">XX.X%</div></div>
    <div class="kpi-item"><div class="kpi-label">Suppliers Mapped</div><div class="kpi-value">XX</div></div>
    <div class="kpi-item"><div class="kpi-label">Top 5 = % of COGS</div><div class="kpi-value">~XX%</div></div>
    <div class="kpi-item"><div class="kpi-label">Key Customers</div><div class="kpi-value">XX</div></div>
  </div>
```

### Section 4: Page Layout

The dashboard uses a **single scrollable page** (no tabs) with the following vertical order:
1. KPI bar (target company overview)
2. Canvas network visualization (full chain: Tier 3 → Tier 2 → Tier 1 → Target → Customers → Tier 2 Customers)
3. Inventory Health Overview table (suppliers AND customers)
4. Supplier cards grouped by tier
5. Customer cards grouped by category
6. Upstream Shock Analysis (demand shock → suppliers, narrative + impact matrix)
7. Downstream Shock Analysis (supply disruption → customers, narrative + impact matrix)
8. Concentration Analysis summary (both upstream and downstream)
9. Footer

Each supplier and customer card is clickable — opening a **full-screen detail overlay** with 10-quarter financials, inventory tables, and Canvas charts. The overlay is dismissed with × or backdrop click.

### Section 5: Canvas Network Visualization

Replace the HTML card-based chain view with a **Canvas-based tier-grouped network**:

- Use a `<canvas>` element spanning the full container width, ~420px height
- **Column layout**: Tier 3 (left) → Tier 2 → Tier 1 → Target (center) → Customers (right)
- Draw each company as a rounded rectangle node with ticker label
- Draw connection lines (bezier curves or straight lines) between related nodes
- Color-code by tier: Target = navy (#1B2A4A), Tier 1 = steel blue (#4A6FA5), Tier 2 = gold (#C5A55A), Tier 3 = dark gray (#6C757D), Customers = mid gray (#E9ECEF)
- **Clickable nodes**: Track click coordinates with a `click` event listener on the canvas, determine which node was clicked via hit-testing, then open the detail overlay for that company
- Column headers ("TIER 1", "TIER 2", "TARGET", etc.) drawn as text above each column
- Responsive: redraw on `window.resize`

```javascript
// Example network drawing function pattern:
function drawNetwork() {
  const cv = document.getElementById('networkCanvas');
  const ctx = cv.getContext('2d');
  cv.width = cv.parentElement.clientWidth;
  cv.height = 420;
  ctx.clearRect(0, 0, cv.width, cv.height);

  // Define columns: x positions for each tier
  const cols = {
    tier3: cv.width * 0.08,
    tier2: cv.width * 0.28,
    tier1: cv.width * 0.48,
    target: cv.width * 0.68,
    customers: cv.width * 0.88
  };

  // Draw column headers, nodes, and connection lines
  // Store node positions for hit-testing on click
}
```

### Section 5b: Inventory Health Overview

Below the network, add an **Inventory Health Overview** table showing all suppliers AND customers:

```
| Company | Ticker | Role | Total Inventory | RM% | WIP% | FG% | Composition Bar |
```

- The "Role" column shows "Supplier T1", "Supplier T2", "Customer", or "Target"
- The "Composition Bar" column renders a stacked horizontal bar (RM = blue, WIP = amber, FG = green) using inline CSS `background: linear-gradient(...)`
- Sort by total inventory descending or by FG% descending (highest FG% = most demand-shock exposure)
- Include the target company at the top of the table, then suppliers, then customers
- Each inventory value must link to its Daloopa citation
- **Analytical note**: For suppliers, rising FG% signals demand weakness from the target. For customers, rising RM% signals stockpiling of the target's inputs (bullish near-term, potential destocking risk later). Falling RM% at customers signals reduced orders ahead.

### Section 5c: Supplier Cards by Tier

Below the inventory overview, render supplier cards grouped under tier headings:

```
── TIER 1 · Critical / Sole-Source ──────
[Card: TSMC]  [Card: Samsung]  [Card: Broadcom]  ...

── TIER 2 · Major Component ─────────────
[Card: Qualcomm]  [Card: Skyworks]  [Card: TXN]  ...

── TIER 3 · Specialty ───────────────────
[Card: Corning]  [Card: Cirrus Logic]  ...
```

Each card shows: Company name, ticker, what they supply, TTM revenue, gross margin, estimated % of target COGS, a colored dot for tier. Clicking a card opens the detail overlay.

### Section 5d: Customer Cards by Category

Below the supplier cards, render customer cards grouped under category headings:

```
── CHANNEL PARTNERS · Distribution & Retail ──────
[Card: Best Buy]  [Card: AT&T]  [Card: Verizon]  ...

── ENTERPRISE / B2B · Direct Customers ───────────
[Card: Enterprise customer 1]  [Card: Enterprise customer 2]  ...

── END-MARKET EXPOSURE · Indirect Demand ─────────
[Card: End-market exposure 1]  ...
```

Categories should be adapted to the target company's business model:
- **B2B/Components companies**: Group by end-market vertical (Auto, Aerospace, Consumer Electronics, Data Center, etc.)
- **Consumer products**: Group by channel (Direct, Retail Partners, Carriers, Enterprise)
- **Software/Platform**: Group by customer type (Enterprise, SMB, Consumer, Government)
- **Industrials**: Group by end-market (Energy, Infrastructure, Transportation, Defense)

Each card shows: Company name, ticker, what the target supplies to them, TTM revenue, gross margin, estimated % of target revenue from this customer, input criticality badge (HIGH/MED/LOW), switching cost indicator. Clicking a card opens the detail overlay.

Customer cards use the `.customer-card` CSS class (border-left color = `--node-customer`).

### Section 6: Detail Overlay

When a user clicks a supplier card, customer card, or network node, show a **full-screen overlay** with comprehensive detail. The overlay structure is the same for both suppliers and customers.

**Structure:**
- Fixed overlay div covering the viewport with semi-transparent backdrop
- Close button (×) in top-right corner
- Content area with four sub-sections:

**6a. Financial History Table (10 Quarters)**
```
| Metric        | Q3'23 | Q4'23 | Q1'24 | ... | Q4'25 |
|---------------|-------|-------|-------|-----|-------|
| Revenue       | $XXB  | $XXB  | ...   |     |       |
| Gross Profit  | $XXB  | $XXB  | ...   |     |       |
| Net Income    | $XXB  | $XXB  | ...   |     |       |
| Gross Margin  | XX.X% | XX.X% | ...   |     |       |
```
- Every value must be a Daloopa citation link: `<a href="https://daloopa.com/src/{id}">$value</a>`
- Display currency unit in header (e.g., "USD $M", "NTD B", "KRW T")

**6b. Inventory Breakdown Table (10 Quarters)**
```
| Metric           | Q3'23 | Q4'23 | ... |
|------------------|-------|-------|-----|
| Raw Materials    | $XXM  | $XXM  | ... |
| Work in Process  | $XXM  | $XXM  | ... |
| Finished Goods   | $XXM  | $XXM  | ... |
| Total Inventory  | $XXM  | $XXM  | ... |
| RM%              | XX%   | XX%   | ... |
| WIP%             | XX%   | XX%   | ... |
| FG%              | XX%   | XX%   | ... |
```
- Absolute values are Daloopa citation links; percentages are computed (no link needed)

**6c. Canvas Chart — Inventory Composition vs. Gross Margin**
- **Stacked bar chart**: Each bar represents a quarter. Segments = RM (blue), WIP (amber), FG (green), stacked to total inventory value
- **Line overlay**: Gross Margin % plotted as a line with dots on the right Y-axis (0-100%)
- **Left Y-axis**: Inventory value in reporting currency
- **X-axis**: Quarter labels (Q3'23, Q4'24, etc.)
- Draw using Canvas 2D API with `createElement('canvas')`, NOT any charting library
- Include a legend below the chart

**6d. Relationship Context Panel**
- For **suppliers**: Show "% of target COGS" bar, "% of supplier revenue from target" bar, switching cost assessment, sole-source flag, geographic risk
- For **customers**: Show "% of target revenue from customer" bar, "% of customer COGS from target" (input criticality) bar, switching cost assessment, contract type (long-term/spot), alternative sources available
- Both: Business description, specific products/services in the relationship, and source attribution for all estimates

### Section 7: Upstream Shock Analysis

A dedicated section (below the customer cards) analyzing how a demand shock at the target company would propagate upstream:

**7a. Narrative Analysis** — 3-4 paragraphs covering:
- "Most Exposed Suppliers" — those with highest revenue dependency on target
- "Resilient Suppliers" — diversified revenue, low target concentration
- "Second-Order Effects" — how Tier 2/3 suppliers are indirectly affected
- "Key Monitoring Metrics" — inventory days, order backlogs, WIP trends to watch

**7b. Upstream Impact Matrix Table**
```
| Supplier | Tier | Rev. from Target | Revenue Impact | Margin Impact | Inventory Risk | Overall |
|----------|------|------------------|---------------|---------------|----------------|---------|
| TSMC     | 1    | ~25%             | HIGH          | MEDIUM        | LOW            | HIGH    |
| ...      |      |                  |               |               |                |         |
```
- Color-code risk cells: HIGH = red background, MEDIUM = amber, LOW = green
- Sort by Overall Risk descending

### Section 7c: Downstream Shock Analysis

A dedicated section analyzing how a supply disruption at the target company would propagate downstream. This is the mirror of Section 7 — instead of "what happens to suppliers if target demand drops," this asks "what happens to customers if the target can't deliver."

**7c-i. Narrative Analysis** — 3-4 paragraphs covering:
- "Most Vulnerable Customers" — customers with highest input criticality and switching costs; a target disruption would directly impair their revenue
- "Customers with Alternatives" — those who can substitute within a reasonable timeframe; quantify how long and at what cost
- "Pricing Power Dynamics" — if the target faces constrained supply, who gets allocation priority? Large customers with long-term contracts typically get served first; smaller or spot customers get cut. This reveals the target's pricing power and customer hierarchy.
- "Channel Inventory as Leading Indicator" — what customer RM% trends tell you about the target's forward order book. If customers are building inventory, the target's next 1-2 quarters look strong but risk destocking later. If customers are drawing down, near-term orders may disappoint.

**7c-ii. Downstream Impact Matrix Table**
```
| Customer | Category | Input Criticality | Switching Cost | Rev. at Risk | Inventory Buffer | Overall Disruption Risk |
|----------|----------|-------------------|---------------|-------------|-----------------|------------------------|
| Best Buy | Channel  | LOW               | LOW           | ~$40B       | ~4 weeks        | LOW                    |
| ...      |          |                   |               |             |                 |                        |
```
- Color-code risk cells: HIGH = red background, MEDIUM = amber, LOW = green
- Sort by Overall Disruption Risk descending
- "Rev. at Risk" = the customer's revenue that depends on products using the target's inputs
- "Inventory Buffer" = estimated weeks/months of the target's product the customer holds in RM inventory

### Section 8: Concentration Analysis

Summary of concentration risk on BOTH sides of the value chain:

**Upstream (Supplier) Concentration:**
- Supplier concentration: flag any supplier >20% of COGS
- Revenue dependency: flag any supplier where target is >25% of their revenue
- Geographic concentration: note country exposure (Taiwan, China, South Korea, etc.)
- Single-source dependencies: list sole-source suppliers

**Downstream (Customer) Concentration:**
- Customer concentration: flag any customer >15% of target's revenue
- Input criticality: flag any customer where target's product is a critical, hard-to-substitute input (high switching cost)
- Channel concentration: what % of revenue flows through the top 3 channels? Is there a single channel that could be disrupted (e.g., carrier subsidies ending, retail partner going bankrupt)?
- Geographic exposure: note country/region concentration in the customer base
- Contract risk: flag any large customer relationships that are up for renewal, at risk of in-sourcing, or where the customer is developing alternatives

**Bidirectional Risk Summary:**
- Which relationships have asymmetric power? (target depends on supplier more than supplier depends on target, or vice versa)
- Where are the mutual dependencies? (both parties depend heavily on each other — most stable but hardest to exit)
- What's the "weakest link"? Identify the single point of failure in the full chain that would cause the most damage if disrupted

### Section 10: Footer
```html
  <div class="page-footer">
    Prepared by {FIRM_NAME} | Data sourced from <a href="https://daloopa.com">Daloopa</a>. All financial figures link to original source filings.
    [Date]. Supply chain relationships are based on public filings, analyst research, and industry reports. Not investment advice.
  </div>
</div><!-- end container -->
</body>
</html>
```

---

## CRITICAL RULES

### Citation & Formatting Rules
Follow `../data-access.md` Section 4 for all citation requirements and `../design-system.md` for number formatting. Additional supply-chain-specific conventions:
- For estimated figures (% of COGS, % of revenue), always explain the methodology in the detail panel
- Use `~` prefix for all estimates (e.g., `~35%` of COGS)
- Use `&ndash;` for ranges, `&mdash;` for em-dashes, `&middot;` for separators

### Upstream Concentration Risk Classification
- **HIGH** (red): >15% of COGS, sole/single source, or geopolitical risk
- **MED** (amber): 5-15% of COGS, limited alternatives, or moderate switching costs
- **LOW** (green): <5% of COGS, multiple alternatives, easy to switch

### Downstream Criticality Classification
- **HIGH** (red): Customer is >15% of target's revenue, OR target's product is a critical input with high switching costs for the customer
- **MED** (amber): Customer is 5-15% of revenue, OR target's product is important but substitutable with 6-12 month transition
- **LOW** (green): Customer is <5% of revenue, AND target's product is a commodity input with multiple alternatives

### Supply Chain Data Quality
- Always distinguish between **disclosed** (from 10-K, investor reports) and **estimated** (from analyst research, proportional analysis)
- When estimating % of COGS, show your math: "TSMC Apple revenue ~$70B (per TSMC 10-K customer disclosure) / Apple TTM COGS ~$200B = ~35%"
- Use `~` prefix for all estimates
- Include source attribution for every data point in the detail panel
- If a figure cannot be reliably estimated, say "Not disclosed" rather than guessing

### Interactivity Rules
- Every company card (supplier AND customer) and network node must be clickable to open a detail overlay
- Detail overlays show: 10-quarter financials, 10-quarter inventory breakdown, Canvas inventory chart, relationship context panel, business description
- Close overlay with × button or clicking the backdrop
- Network visualization must redraw on window resize
- All interactions must be smooth and not reload the page

### DOM Safety Rules (CRITICAL)
- ALL JavaScript DOM construction MUST use `createElement()` + `textContent` + `appendChild()`
- NEVER use `innerHTML`, `outerHTML`, or any HTML-string-based injection methods
- NEVER use DOM write/writeln methods
- Define compact helper functions to keep DOM construction code readable:
  - `ce(tag)` → `document.createElement(tag)`
  - `ca(el, attrs)` → sets attributes/textContent on an element
  - `cA(parent, children)` → appends array of children to parent
- This is required because security hooks will block the file if HTML-string injection is detected

---

## EXECUTION SEQUENCE

Follow this exact sequence. Maximize parallelism — run independent searches and API calls concurrently. The 10-quarter pull is the most data-intensive step; batch aggressively.

1. **discover_companies** → get target company_id
2. **discover_company_series + get_company_fundamentals** → pull target company financials (revenue, COGS, margins) AND inventory series for 10 quarters
3. **search_documents + WebSearch** → identify suppliers AND customers (run in parallel, multiple queries for each direction)
4. **discover_companies** → look up each identified supplier AND customer by ticker (batch all at once)
5. **discover_company_series** → for each supplier AND customer, pull BOTH financial series (revenue, GP, NI, GM) AND inventory series (RM, WIP, FG, total) — batch these in parallel
6. **get_company_fundamentals** → pull 10 quarters of data for all suppliers AND customers (batch in parallel, group series_ids per company)
7. **search_documents + WebSearch** → determine revenue concentration for each supplier AND revenue attribution + input criticality for each customer (parallel)
8. **Repeat lighter version of 3-6** for Tier 2 suppliers (top 3-5 Tier 1 suppliers' suppliers) AND Tier 2 customers (top 3-5 Tier 1 customers' end markets)
9. **Upstream Shock Analysis** → classify suppliers by dependency, assess propagation, build upstream impact matrix
10. **Downstream Shock Analysis** → classify customers by input criticality and switching costs, assess disruption propagation, build downstream impact matrix
11. **Synthesize** → organize all data (suppliers, customers, financials, inventory breakdowns, both shock analyses) into the framework
12. **Write HTML** → generate the complete self-contained HTML file using DOM-safe JavaScript (no HTML-string injection)
13. **Save & Open** → save and open in browser

## Save Report

Save to `reports/{TICKER}_supply-chain.html` using the HTML Report Template from `../design-system.md` as the CSS base, extended with the dashboard-specific styles above. Write the full analysis as styled HTML with all CSS inlined. This is the final deliverable — no intermediate markdown step needed.

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight the key findings with a critical lens:
- **Upstream concentration risk**: Which suppliers represent the biggest single points of failure? Are there sole-source dependencies the market may be underpricing?
- **Downstream concentration risk**: Is the target overly dependent on a few customers? Are any major customers at risk of in-sourcing or switching?
- **Asymmetric exposure (upstream)**: Which suppliers depend heavily on the target for revenue — and what would happen to them in a demand shock?
- **Asymmetric exposure (downstream)**: Which customers depend heavily on the target as a critical input — and what would happen to them in a supply disruption?
- **Inventory signals (bidirectional)**: Supplier FG% rising = demand weakness. Customer RM% rising = stockpiling (bullish near-term, destocking risk later). Customer RM% falling = reduced orders ahead.
- **Pricing power**: Does the target have more leverage over its customers or do its suppliers have more leverage over it? Where does the target sit in the power hierarchy of its value chain?
- **What the market is missing**: Is there a supply chain vulnerability, customer concentration risk, or value chain shift that isn't widely discussed?
