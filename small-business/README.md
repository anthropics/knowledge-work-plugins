# Small Business Plugin

Pre-built small business workflows for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — also works in Claude Code. Install it once and you get 15 building-block skills, 15 ready-to-use workflows, and a router that understands plain English.

You don't need to memorize anything. Just tell Claude what you need — "I'm stressed about making payroll," "a customer is angry," "what should I charge?" — and it figures out the right workflow and walks you through it. Every workflow pauses before taking action, so nothing happens without your say-so.

> **Important**: This plugin assists with small business workflows but does not provide financial, tax, legal, or HR advice. All outputs should be reviewed by you (and where appropriate, a qualified professional) before use.

## Installation

### Cowork

Install from [claude.com/plugins](https://claude.com/plugins/).

### Claude Code

```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install small-business@knowledge-work-plugins
```

Once installed, say **"set me up"** to run the `smb-onboard` skill — it'll help Claude understand your business, your pain points, and the tools you already use.

## What you'll need to connect

Run `/smb-onboard` or ask Claude to "set me up."

**Core tools** (connect these first for the best experience):
- **QuickBooks** — powers all financial workflows (cash forecasts, margins, month-end close, tax prep)
- **PayPal** — transaction data, invoices, disputes, and refunds
- **HubSpot** — CRM, leads, campaigns, and customer support tickets

**Marketing & communication:**
- **Canva** — generates on-brand social and email assets
- **Gmail / Outlook** — email drafts, ticket handling, contract review
- **Google Calendar / Outlook Calendar** — meeting prep, call blocking, weekly commitments
- **Slack** — brief delivery and notifications

**Optional** (adds depth when connected):
- **Stripe** — payment and subscription data
- **Square** — POS transaction data
- **Google Drive / OneDrive** — file storage and templates
- **DocuSign** — contract review from pending envelopes

You don't need all of these to start. Connect one or two and you'll immediately see value — the plugin tells you when connecting another tool would unlock more.

## How it works

Three layers working together:

1. **Skills** — the building blocks. Each skill knows how to do one thing really well (forecast cash, score leads, draft an invoice reminder). There are 15 of these.

2. **Commands** — the workflows. Commands chain skills together into multi-step recipes with checkpoints where you approve before anything happens. There are 15 of these.

3. **The Router** — the front door. You talk to Claude in plain English. The router listens, figures out which workflow fits, and gets you there. You never need to memorize a command name.

## All 15 commands

Commands are workflows that chain skills together. Each one pauses at checkpoints for your approval before taking action.

### Money & finance

| Command | What it does | Just say... | Skills used | Required | Optional |
|---|---|---|---|---|---|
| `/plan-payroll` | Cash forecast + overdue invoice chase so you know payroll is covered. | "can I make payroll", "cash is tight", "who owes me money" | cash-flow-snapshot, invoice-chase | QuickBooks | PayPal, Stripe, Square, Mail |
| `/month-heads-up` | 30-day cash outlook with early risk flags. | "what does next month look like", "cash forecast", "runway" | cash-flow-snapshot | QuickBooks | PayPal |
| `/close-month` | Month-end close: reconcile, flag gaps, write P&L, export packet. | "close the books", "month-end", "reconcile" | month-end-prep | QuickBooks | PayPal, Stripe, Square |
| `/price-check` | Margin-by-product table and three pricing scenarios. | "what are my margins", "should I raise prices", "cost per unit" | margin-analyzer | QuickBooks | PayPal |
| `/tax-prep` | Tax prep materials for your accountant (quarterly estimates or year-end 1099s). | "tax stuff", "estimated taxes", "1099s", "accountant needs..." | tax-season-organizer | QuickBooks | PayPal, Stripe |

### Sales & marketing

| Command | What it does | Just say... | Skills used | Required | Optional |
|---|---|---|---|---|---|
| `/call-list` | Top 5 leads to call today with talking points and calendar blocks. | "who should I call", "any hot leads", "pipeline" | lead-triage | HubSpot | Mail, Google Calendar |
| `/run-campaign` | End-to-end campaign: sales analysis → content brief → Canva assets → HubSpot send. | "run a campaign", "sales are down", "I need more customers" | content-strategy, canva-creator, lead-triage | HubSpot, Canva | QuickBooks, PayPal |
| `/sales-brief` | Top and bottom sellers with a 2-week content brief. | "what's selling", "what should I promote" | content-strategy | QuickBooks or PayPal | HubSpot |

### Customers & operations

| Command | What it does | Just say... | Skills used | Required | Optional |
|---|---|---|---|---|---|
| `/customer-pulse-check` | Customer feedback themes with response templates. | "what are customers saying", "complaints", "reviews" | customer-pulse, ticket-deflector | PayPal or HubSpot | -- |
| `/handle-complaint` | End-to-end complaint resolution: pull context, draft response, suggest operational fix. | "a customer is upset", "handle this complaint", "angry email" | ticket-deflector, customer-pulse | -- (works with pasted text) | Gmail, HubSpot, PayPal |
| `/crm-cleanup` | HubSpot hygiene: stale deals, duplicates, missing fields — fixes what you approve. | "clean up the CRM", "HubSpot is a mess", "stale deals" | crm-maintenance | HubSpot | -- |
| `/review-contract` | Plain-English contract review with red flags and severity ratings. | "review this contract", "NDA", "should I sign this" | contract-review | -- (works with file upload) | DocuSign |

### Business intelligence

| Command | What it does | Just say... | Skills used | Required | Optional |
|---|---|---|---|---|---|
| `/monday-brief` | Monday morning briefing: cash, sales, pipeline, week ahead, top 3 to-dos. | "Monday brief", "what's on my plate", "start of week" | business-pulse | -- (degrades gracefully) | QuickBooks, PayPal, HubSpot, Calendar, Gmail, Slack |
| `/friday-brief` | Friday end-of-week pulse: revenue vs last week, wins, and things to watch. | "end of week", "how'd we do", "Friday recap" | business-pulse | PayPal or HubSpot | -- |
| `/quarterly-review` | Full QBR narrative: revenue, margin, customer health, opportunities, risks. | "quarterly review", "board deck", "QBR" | business-pulse | QuickBooks | PayPal, HubSpot |

## All 15 skills

Skills are the atomic building blocks. Each one does one thing well.

### Money & finance

| Skill | What it does | Just say... | Required | Optional |
|---|---|---|---|---|
| **cash-flow-snapshot** | 30/60/90-day cash forecast with confidence bands and named risk flags. Chat summary + XLSX. | "forecast my cash flow", "will I make payroll", "runway", "cash crunch" | QuickBooks, PayPal, Stripe, or Square (any one) | Others as secondary sources |
| **invoice-chase** | Drafts overdue-invoice reminders matched to each customer's payment history and tone. Sends via PayPal with approval. | "who owes me money", "overdue invoices", "follow up on unpaid" | QuickBooks | PayPal, Stripe, Gmail |
| **margin-analyzer** | Unit economics by product or service with inflation benchmarks and three pricing scenarios. | "what are my margins", "should I raise prices", "costs eating into profit", "what to charge" | QuickBooks | PayPal, Square, CSV upload |
| **month-end-prep** | Month-end close: reconciles QB against payment processors, flags gaps, writes P&L narrative, exports close packet. | "close the month", "reconcile", "P&L", "why revenue changed" | QuickBooks | PayPal, Stripe, Square |
| **tax-season-organizer** | Quarterly estimated tax calc or year-end 1099-NEC prep with accountant handoff packet. | "quarterly taxes", "estimated tax payment", "1099s", "1099-NEC", "year-end tax prep" | QuickBooks | PayPal, Stripe |

### Sales & marketing

| Skill | What it does | Just say... | Required | Optional |
|---|---|---|---|---|
| **lead-triage** | Scores HubSpot leads by engagement, fit, and urgency to produce a ranked call list with talking points. | "prioritize leads", "who to call first", "pipeline" | HubSpot | Gmail, Google Calendar |
| **content-strategy** | Analyzes sales data to find top performers and slow movers, produces a prioritized 30-day content brief. | "what should I post", "content plan", "what's selling", "what to promote" | QuickBooks or PayPal | Square |
| **canva-creator** | Takes a content brief and executes the full campaign: posting calendar, Canva assets, caption copy, HubSpot staging. | "make the content", "generate the posts", "create the assets", "turn this into a campaign" | Canva, HubSpot | -- |

### Customers & operations

| Skill | What it does | Just say... | Required | Optional |
|---|---|---|---|---|
| **customer-pulse** | Aggregates disputes, tickets, email sentiment, and reviews into a themes report with a "do these three things this week" list. | "how are customers feeling", "what people are saying", "disputes", "review analysis" | -- (degrades gracefully) | PayPal, HubSpot, Gmail |
| **ticket-deflector** | Reads a customer email or ticket, pulls order/refund status, drafts a tone-matched reply. Can issue PayPal refunds with approval. | "draft a response", "answer this customer", "where's my order", "I want a refund" | PayPal, HubSpot, Mail | Intercom, Square |
| **crm-maintenance** | Keeps HubSpot current: creates/updates contacts and deals, logs calls and notes, flags stale records. | "update the CRM", "log a call", "clean up HubSpot", "add context to a deal" | HubSpot | Gmail, Google Calendar |
| **contract-review** | Plain-English contract review with risk flags, severity ratings, and a marked-up redline DOCX. | "review this contract", "what am I signing", "flag any concerns", "check the payment terms" | -- (works with file upload) | Gmail, DocuSign |

### Hiring

| Skill | What it does | Just say... | Required | Optional |
|---|---|---|---|---|
| **job-post-builder** | Builds a complete hiring packet: job post, structured interview guide with scoring rubric, and offer letter template. | "help me hire", "write a job post", "job description", "open role", "interview questions", "draft an offer letter" | -- (works standalone) | DocuSign, Google Drive |

### Business intelligence & onboarding

| Skill | What it does | Just say... | Required | Optional |
|---|---|---|---|---|
| **business-pulse** | One-page business snapshot: cash, sales, pipeline, commitments, watch-list, and the single most important thing needing attention today. | "how's the business doing", "snapshot", "weekly summary", "catch me up" | -- (degrades gracefully) | QuickBooks, PayPal, HubSpot, Google Calendar, Gmail, Slack |
| **smb-onboard** | Walks you through connecting tools, runs a demo recipe, captures your business context, and sets a weekly check-in cadence. | "set me up", "setup", "get started", "help me get set up", "I'm new to this", "what can you do" | -- | All connectors |

## Customizing

These workflows are generic starting points. They become much more useful when you customize them for how your business actually works:

- **Add business context** — Drop your industry, products, customers, and processes into skill files so Claude understands your world.
- **Adjust thresholds** — Tune the alert thresholds in `business-pulse` and `cash-flow-snapshot` to match your scale.
- **Swap connectors** — Point skills at the tools you actually use.
