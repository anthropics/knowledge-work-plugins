# Sales Plugin

A sales plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application, though it also works in Claude Code. It helps with the whole sales day: prepping calls, summarizing and following up, researching accounts, working deals, reviewing pipeline and writing the forecast. It works with the tools your team already uses (your CRM, email, calendar, chat and call recorder) or with files you upload when nothing is connected.

## Installation

```bash
claude plugins add knowledge-work-plugins/sales
```

## What's new in 2.0

- **From 9 to 36 skills.** New skills cover deal reviews, close plans, stakeholder maps, renewals, customer health, lead routing, CRM updates, meeting booking, inbox sweeps and team pipeline views.
- **Works across CRMs and email providers.** Skills read your CRM's own stages and fields instead of assuming one vendor's setup, and work the same on Gmail or Outlook, Slack or Teams. No settings file is needed; a skill asks once for anything it cannot find.
- **Uses uploaded files when nothing is connected.** Upload a pipeline export, a transcript or a list of accounts, and the skill works from that.
- **Acts when you ask.** Skills can update CRM records, create email drafts or send email, post to chat and book meetings, within each connector's permissions. Changes a skill suggests on its own are shown to you first, with the evidence behind them.
- **Treats outside content as information.** Emails, call transcripts, chat messages and documents are read as information, never as instructions. If an email or transcript asks for an action, the skill shows you the action before anything happens.
- **Existing skill names still work.** `account-research`, `call-summary`, `forecast`, `call-prep`, `daily-briefing`, `draft-outreach`, `pipeline-review`, `competitive-intelligence` and `create-an-asset` keep their names, rebuilt on the new skills. Two behave differently: `create-an-asset` now builds decks, one-pagers and leave-behinds from your account data rather than landing pages or interactive demos, and `forecast` writes a commit, best-case and pipeline narrative instead of best, likely and worst scenarios.

## Skills

Skills run when your request matches, or directly by name (for example `/sales:call-summary`).

### Your day

| Skill | Description |
|---|---|
| `setup` | First-run setup: shows what's connected and what each tool unlocks, learns how you write, and renders a starter dashboard |
| `daily-briefing` | Morning rundown: today's meetings with account context, deals closing soon, customer emails waiting, top actions |
| `call-prep` | Pre-call brief: attendees, account history, prior call context, open opportunity status, discovery questions |
| `call-summary` | Turn a transcript or call notes into a follow-up email draft, a team summary and proposed CRM updates |
| `inbox-sweep` | Sort unread customer emails by priority and draft replies |
| `schedule-meeting` | Find a time, draft the invite, book it on your calendar and log it to the CRM |
| `log-activity` | Log a call, meeting or email to the right account, opportunity and contact in the CRM |
| `end-of-day` | Close out the day: calls processed, CRM current, commitments captured, tomorrow's top three |
| `weekly-wrap` | End-of-week summary of what closed, moved and slipped, and what's on deck Monday |

### Accounts and prospecting

| Skill | Description |
|---|---|
| `account-research` | Research a company or contact: overview, recent news, likely priorities and fit against your ICP |
| `account-context` | One brief on an account from CRM data, email, docs, transcripts and team chat |
| `stakeholder-map` | Map the people in a deal: roles, influence, sentiment, who's missing and your best way in |
| `draft-outreach` | Draft a personalized email or multi-touch sequence, and add the contact to a sequence when asked |
| `lead-triage` | Score an inbound lead or rank a lead backlog against your ICP and recommend next actions |
| `route-lead` | Decide who owns an unrouted lead or opportunity and draft the handoff notes |
| `account-tiering` | Score and tier a list of accounts or your whole book by fit and engagement |
| `account-plan` | Build or refresh a strategic account plan and sync key fields to the CRM |
| `expansion-whitespace` | Find expansion plays in an account or book, with evidence and the opportunities to create |

### Deals

| Skill | Description |
|---|---|
| `deal-review` | Deep-dive on one opportunity: health score, risks, qualification gaps and next actions |
| `deal-advance-gap` | What is missing to move a deal to the next stage and to close, with owners and dates |
| `deal-signals` | Alerts across your book: deals gone quiet, slipping close dates, champion changes, competitor mentions |
| `deal-slip-scenario` | Model the effect on your number if a deal slips, shrinks or is lost |
| `close-plan` | Business case and mutual action plan: why buy, why now, and the dated path to signature |
| `handle-objection` | Work through an objection or competitive threat with responses and proof points from your own history |
| `competitive-intelligence` | The play against a named competitor in a deal, plus win/loss patterns and battlecards across the book |
| `create-an-asset` | Build a customer deck, one-pager or leave-behind from your account data, with no made-up numbers |
| `update-opportunity` | Update stage, close date, next steps, amount or forecast category, with a before and after |

### Pipeline and forecast

| Skill | Description |
|---|---|
| `pipeline-review` | Stage-by-stage pipeline health: coverage, aging, conversion and at-risk deals |
| `crm-hygiene-check` | Read-only audit of opportunities for missing fields, stale dates and stage mismatches |
| `forecast` | The commit, best-case and pipeline narrative for a forecast call or a 1:1 with your manager |
| `team-pipeline` | Leader view of a team's pipeline by rep and stage, with at-risk deals and coaching moments |
| `rep-context` | Leader prep for a 1:1 with a rep: pipeline, recent activity and where they may need help |
| `win-loss-review` | Patterns in recently closed deals: where deals are lost, common objections, what wins |

### Customers

| Skill | Description |
|---|---|
| `customer-health` | Health check on a customer and QBR prep: relationship, engagement, risks and value delivered |
| `customer-voice` | Direct, attributed customer quotes on a topic from call transcripts and email |
| `renewal-radar` | Upcoming renewals with timing, risk and uplift potential |

## Example workflows

### After a call

```
/sales:call-summary
```

Paste your notes or transcript, or name the call if your call recorder is connected. You get a summary, a follow-up email draft, a team summary and proposed CRM updates. Nothing is written to the CRM or sent until you say so.

### Forecast call

```
Write my forecast for this quarter
```

The `forecast` skill reads your open opportunities (or an uploaded pipeline export) and writes the commit, best-case and pipeline story, what changed and where the risk is.

### Researching a prospect

```
Research Acme Corp before my call tomorrow
```

The `account-research` skill gives you a company overview, recent news, likely priorities and fit against your ICP, and checks whether the company is already in your CRM.

## Works with files, better with your tools

Every skill works without any connectors:

| What you can do | With nothing connected | With connected tools |
|---|---|---|
| Summarize a call and follow up | Paste notes or a transcript | Call recorder, email, CRM, chat |
| Review pipeline and forecast | Upload a pipeline export | CRM |
| Research accounts | Web search and your context | Data enrichment, CRM |
| Prep for calls | Describe the meeting | Calendar, CRM, email, call recorder |
| Draft outreach | Web search and your context | Email, CRM, sales engagement |
| Update the CRM | Get a checklist to apply by hand | CRM |
| Book meetings | Get a draft invite to send yourself | Calendar, CRM |

With nothing connected, a skill says plainly what it used and what it could not see.

## Connectors

> To check which tools are included and what else works, see [CONNECTORS.md](CONNECTORS.md).

| Category | Examples | What it enables |
|---|---|---|
| **CRM** | HubSpot, Close, Salesforce | Opportunities, accounts, contacts, record updates |
| **Email and calendar** | Gmail, Google Calendar, Calendly, Microsoft 365 | Customer threads, drafts, meetings, booking |
| **Call recorder** | Gong, Fireflies, Zoom, Otter.ai | Transcripts and call history |
| **Data enrichment** | Clay, ZoomInfo, Apollo, Lusha, Crunchbase | Company and contact data |
| **Chat** | Slack, Microsoft Teams | Team context and summaries posted to channels |

**Salesforce and Microsoft 365 (Outlook, Teams, SharePoint) connect through the Claude connector directory.**

See [CONNECTORS.md](CONNECTORS.md) for every included server and other options.

## For admins

Connector permissions are where your team controls what runs. Each connector can allow, ask or block each of its tools, and the skills never go beyond those settings. If a write tool is blocked, the skill keeps working and hands the person a checklist to apply by hand.

For scheduled runs (a morning briefing, a weekly deal signals digest), set send, post and write tools to **ask**, so nothing goes out or changes without a person approving it.
