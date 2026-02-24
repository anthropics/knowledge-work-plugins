# Common Room Plugin

GTM workflows powered by Common Room — account research, contact research, call prep, personalized outreach, prospecting, and weekly briefings.

## Overview

This plugin connects Claude to Common Room's MCP server and equips it with six skills covering the most common rep workflows. Every output is grounded in real Common Room signal data — 1st-party product signals, 2nd-party community signals, 3rd-party intent signals, and enrichment from RoomieAI and Spark.

## Requirements

- **Common Room MCP** (`mcp.commonroom.io/mcp`) must be connected and authenticated. This is the primary data source for all plugin functionality.
- **Calendar connector** (optional) — enables automatic meeting lookup in `call-prep` and `weekly-prep-brief`. If not connected, both skills ask the user for meeting details instead.

## Skills

Skills are triggered conversationally. Describe what you want and Claude will load the right skill automatically.

| Skill | Trigger phrases |
|-------|----------------|
| `account-research` | "Research [company]", "tell me about [domain]", "what's going on with [account]", "is [company] showing buying signals" |
| `contact-research` | "Who is [name]", "look up [email]", "research [contact]", "is [name] a warm lead" |
| `call-prep` | "Prep me for my call with [company]", "prepare for a meeting with [company]", "what should I know before talking to [company]" |
| `compose-outreach` | "Draft outreach to [person]", "write an email to [name]", "compose a message for [contact]" |
| `prospect` | "Find companies that match [criteria]", "build a prospect list", "find contacts at [type of company]" |
| `weekly-prep-brief` | "Weekly prep brief", "prepare my week", "what calls do I have this week" |

## Commands

Two commands for complex workflows that benefit from explicit invocation:

| Command | Usage |
|---------|-------|
| `/generate-account-plan <company>` | Comprehensive strategic account plan with stakeholder mapping, engagement analysis, opportunities, risks, and action items |
| `/weekly-brief [date range]` | Generate a full weekly prep briefing (defaults to next 7 days) |

## What Each Skill Produces

**Account Research** — Handles four patterns: full overviews, targeted field questions, honest sparse-data responses, and combined MCP data + LLM reasoning. Includes web search for recent news. Automatically scopes to "My Segments."

**Contact Research** — Lookup by email, name+company, or social handle. Returns enriched identity, CRM fields, scores, website visits, activity history, Spark analyses, and conversation starters.

**Call Prep** — Company snapshot, per-attendee profiles, signal highlights, tailored talking points, likely objections, and recommended call outcome. Prioritizes Gong/call recording activity. Calendar-aware if connected.

**Compose Outreach** — Three personalized formats (email, call script, LinkedIn message) grounded in Common Room signals and web search hooks. Tailored to the user's company positioning when available.

**Prospecting** — Distinguishes between net-new companies (ProspectorOrganization) and existing accounts (Organization). Supports iterative refinement and lookalike search ("find companies like [X]"). Web search enriches net-new results.

**Weekly Prep Brief** — Full briefing covering every external call in the next 7 days: company snapshot, attendee profiles, signals, and recommended objectives per meeting.

## Setup

1. Ensure the Common Room MCP server is connected and authenticated in your Cowork settings.
2. (Optional) Connect a calendar MCP server for automatic meeting lookup in call prep and weekly briefings.
3. Install this plugin. All skills and commands are available immediately.

## User Context

All skills that scope to a user's territory automatically fetch the `Me` object from Common Room. This provides the user's profile, role, and "My Segments" — ensuring queries default to their territory. See `references/me-context.md` for details.

When company context is available, skills tailor recommendations to the user's product and ICP. See `references/my-company-context.md` for details.

## Customization

See `CONNECTORS.md` for details on the calendar connector and how tool references work.
