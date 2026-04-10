---
name: nimble-agent-builder
description: >
  A building experience: create, test, validate, refine, and publish extraction workflows
  based on existing or new Nimble agents. For users who want to invest in a durable,
  reusable workflow for a specific domain — not get data immediately.
  Trigger phrases: "set up extraction for X site", "I need to extract from this site regularly",
  "build an agent for", "create a reusable scraper", "generate a Nimble agent",
  "refine my agent", "add a field to my agent", or when the user wants to run extraction at scale.
  For getting data immediately, use nimble-web-expert instead.
allowed-tools:
  # All operations available via CLI (Bash):
  #   nimble agent list --limit 100
  #   nimble agent get --template-name <name>
  #   nimble agent run --agent <name> --params '{...}'
  #   nimble agent generate --agent-name <name> --prompt "<prompt>" --url "<url>"
  #   nimble agent get-generation --generation-id <id>
  #   nimble agent publish --agent-name <name> --version-id <id>
  #   nimble search --query "<query>" --max-results 5
  #   nimble map --url <url> --limit 50
  # MCP tools (fallback when CLI is not installed):
  - Bash
  - Task
  - mcp__plugin_nimble_nimble-mcp-server__nimble_agents_generate
  - mcp__plugin_nimble_nimble-mcp-server__nimble_agents_status
  - mcp__plugin_nimble_nimble-mcp-server__nimble_agents_publish
  - mcp__plugin_nimble_nimble-mcp-server__nimble_agents_update_from_agent
  - mcp__plugin_nimble_nimble-mcp-server__nimble_agents_update_session
license: MIT
metadata:
  version: "0.17.0"
  author: Nimbleway
  repository: https://github.com/Nimbleway/agent-skills
---

# Nimble Agent Builder

Build, refine, and publish reusable extraction agents on the Nimble platform. Always finish with executed results or runnable code.

User request: $ARGUMENTS

## Prerequisites

**Quick check:** `nimble --version && echo "${NIMBLE_API_KEY:+API key: set}"`

If CLI is missing or API key is not set, load `rules/setup.md` for one-time setup (CLI install, API key, MCP server).

## Startup check — run this before anything else

**Verify CLI is available:**

```bash
nimble --version && echo "${NIMBLE_API_KEY:+API key: set}"
```

**If CLI and API key are set** → proceed with the user's request normally.

**If CLI is missing** → check if the MCP server is connected as a fallback:

```bash
claude mcp list 2>/dev/null | grep -q nimble-mcp-server && echo "MCP: connected" || echo "MCP: not connected"
```

- **MCP connected** → proceed using MCP tools instead of CLI commands.
- **Neither CLI nor MCP available** → load `rules/setup.md` for one-time setup (CLI install, API key). CLI is the preferred setup path.

---

## Skill ecosystem

nimble-agent-builder and nimble-web-expert work as a pair in the Nimble toolkit:

| Skill                                 | Best for                                                                                          | Key commands                                     |
| ------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **nimble-agent-builder** (this skill) | Build reusable agents — create, refine, and publish named extraction templates with fixed schemas | CLI: `generate`, `get-generation`, `publish`     |
| **nimble-web-expert**                 | Real-time data access — fetch any URL, search, map, crawl, run published agents                   | `extract`, `search`, `map`, `crawl`, `agent run` |

### Stay in nimble-agent-builder for

- Generating a new agent for a domain
- Refining or updating an existing agent (add fields, fix selectors, change schema)
- Publishing an agent
- Running a published agent via `nimble agent run` (CLI)
- Validating agent output quality
- Any task phrased as "build", "refine", "update", "add a field to", "publish"

### When to route to nimble-web-expert

**After publishing an agent** — run it directly here via `nimble agent run` (CLI). Route to nimble-web-expert only when the workflow needs tools this skill doesn't have:

- Need a list of input URLs to feed into the agent? → Switch to nimble-web-expert, run `nimble map --url <site>` to crawl and generate the input list, then return here to run at scale.
- Need to search for input params? → Switch to nimble-web-expert, run `nimble search`, then return here with the results.

**When the task is not about building an agent:**

- One-off URL fetch, web search, site mapping, bulk crawl → nimble-web-expert
- Tell the user: _"This is a direct data access task, not an agent-building task. Use nimble-web-expert for this."_

### When agent generation needs site investigation

If `nimble_agents_generate` or `nimble_agents_update_from_agent` cannot produce a working agent because the site's data structure is unknown (wrong selectors, missing XHR patterns, unexpected JS rendering):

**Step 1 — Announce:** _"I can't generate a reliable agent without investigating the live page first. Spawning a site investigation..."_

**Step 2 — Spawn a Task agent** (`Task(subagent_type="general-purpose", run_in_background=False)`):

```
Investigate {url} to find CSS selectors and/or XHR API endpoints needed to extract: {fields_needed}.

Use Playwright to probe the live page:
python3 << 'EOF'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    api_calls = []
    page.on("request", lambda req: api_calls.append(req) if req.resource_type in ("xhr","fetch") else None)
    page.goto("{url}")
    page.wait_for_timeout(5000)
    for sel in ["[data-price]",".price","h1","[data-testid*=title]","[data-testid*=price]",".product-title"]:
        el = page.query_selector(sel)
        if el: print(f"SELECTOR: {sel!r} -> {el.inner_text()[:80]!r}")
    for req in api_calls[:20]:
        print(f"XHR: {req.method} {req.url[:120]}")
    browser.close()
EOF

Also run a quick nimble extract to check raw rendered HTML:
nimble extract --url "{url}" --render --format markdown | head -100

Return a structured report:
- SELECTORS: working CSS selectors for each required field
- XHR_URLS: any relevant API endpoints found
- RENDER_REQUIRED: yes/no
- SUGGESTED_EXTRACT_COMMAND: the nimble extract command that would work
- NOTES: login walls, pagination, lazy loading, or anything unusual

Do NOT use AskUserQuestion.
```

**Step 3 — Use the report** to retry agent generation: pass the selector/XHR context and suggested extract command in the `nimble_agents_update_session` call.

**Step 4 — If investigation also fails:** Tell the user: _"This site requires complex browser automation that can't be captured in an agent at this stage. Use nimble-web-expert's Tier 4/5 commands with `--browser-action` or `--network-capture` to access the data directly."_

---

## Core principles

- **Fastest path to data.** Default route: discover agent → get schema → run → display results. Planning and generation are escalation paths.
- **Always search existing agents first.** Run `nimble agent list --limit 100 --search "<domain or vertical>"` (CLI) before considering generate. Hard rule.
- **Update over generate — always.** When a close-match agent exists (same domain/type, even if missing fields or different scope), update it rather than generating from scratch. Updating preserves proven extraction logic and is faster, cheaper, and more reliable. Only generate a new agent when the `--search` query returns 0 matches for the target domain. Never offer "Create new agent" as the recommended option when a close match exists.
- **AskUserQuestion at every decision point in the foreground — no exceptions.** Always present the standard `AskUserQuestion` prompts shown in each step. Never skip them, never auto-advance without asking. Never present choices as plain numbered lists. Constraints: 2–4 options, header max 12 chars, label 1–5 words. Recommended option goes first with "(Recommended)". Note: Task agents NEVER use AskUserQuestion — all decisions are pre-made before launching the Task.
- **Schema before run — always.** Run `nimble agent get --template-name <name>` (CLI) before `nimble agent run`. Present input parameters and output fields in markdown tables. This applies when switching agents too.
- **Script generation (Step 2B) is ONLY for large-scale, high-volume tasks.** Never generate code for normal interactive requests. Script mode requires ALL of: scale >50 items AND the user explicitly asks for code/script/CSV/batch output. Multi-source requests, dataset requests, and comparison requests do NOT automatically trigger script mode — run them interactively first. The default path is always: discover → run → display results.
- **Verify response shape before script generation.** Check `skills` and `entity_type` from `nimble agent get --template-name` (CLI) to determine REST API response nesting. See **`references/agent-api-reference.md`** > "Response shape inference" and **`references/sdk-patterns.md`** > "Response structure verification".
- **`google_search` is not a general search tool.** It is a SERP analysis agent for rank tracking and SEO analysis. For finding information, use `nimble search` (CLI). See **`references/error-recovery.md`**.
- **All web search MUST use `nimble search` (CLI).** Never use `WebSearch`, `WebFetch`, `curl`, or `wget`. See [Guardrails](#guardrails).
- **Agent creation/update runs in background Task agents.** Generation takes 1-3 minutes — run the generate → poll → publish loop as a Task agent so the user isn't blocked. See [Delegation model](#delegation-model).

## Delegation model

The foreground conversation orchestrates and presents results. Task agents handle
long-running work (generation, discovery, script generation).

**Foreground — direct CLI calls via Bash:**

| CLI command                          | Purpose                          | Max calls    |
| ------------------------------------ | -------------------------------- | ------------ |
| `nimble agent list --limit 100 --search "<domain>"` | Route to existing agent | 1 per domain |
| `nimble agent get --template-name`   | Display schema before run        | 1 per agent  |
| `nimble agent run --agent --params`  | Interactive execution (≤5 items) | 1 per item   |
| `nimble search`                      | Web search / discovery           | As needed    |

**Task agents — long-running operations:**

| Phase                                                                                            | Task agent | Foreground does        |
| ------------------------------------------------------------------------------------------------ | ---------- | ---------------------- |
| Discovery (`nimble search` + `nimble map`)                                                       | Step 1D    | Launch, present report |
| Agent create/update (`nimble agent generate` → `get-generation` poll → `publish`)                | Step 3     | Launch, present report |
| Script generation (write code to call existing agent)                                            | Step 2B    | Launch, present script |

Agent creation runs in a Task agent because generation takes 1-3 minutes (poll loop).
The Task agent uses CLI commands via Bash. If CLI is unavailable, it falls back to MCP
tools.

For **multi-source workflows**, launch Task agents sequentially (one per source/phase). Gather reports, then present the combined plan.

### CLI commands for Task agents

All Task agent prompts should include this block so the subagent knows the available commands:

```
**CLI tools (use via Bash):**
- `nimble agent list --limit 100 --search "<domain or vertical>"` — search agents by domain/vertical
- `nimble agent get --template-name <name>` — get agent schema
- `nimble agent run --agent <name> --params '{...}'` — run an agent
- `nimble agent generate --agent-name <name> --prompt "<prompt>" --url "<url>"` — create/refine agent
- `nimble agent generate --agent-name <name> --from-agent <name> --prompt "<prompt>"` — iterate on existing agent
- `nimble agent get-generation --generation-id <id>` — poll generation status
- `nimble agent publish --agent-name <name> --version-id <id>` — publish agent
- `nimble search --query "<query>"` — web search (deep by default)
- `nimble map --url <url> --limit 50` — discover URL patterns on a site

**MCP fallback (only if CLI is not installed):**
| CLI command | MCP tool |
|---|---|
| `nimble agent generate` | `mcp__plugin_nimble_nimble-mcp-server__nimble_agents_generate` |
| `nimble agent get-generation` | `mcp__plugin_nimble_nimble-mcp-server__nimble_agents_status` |
| `nimble agent publish` | `mcp__plugin_nimble_nimble-mcp-server__nimble_agents_publish` |

**CRITICAL: Prefer CLI for all operations. Use MCP only when CLI is unavailable. NEVER use WebSearch, WebFetch, curl, or wget. NEVER construct MCP endpoint URLs manually.**
```

## Response shapes

| Layer                                 | Path                           | Shape                     | When used                   |
| ------------------------------------- | ------------------------------ | ------------------------- | --------------------------- |
| CLI (`nimble agent run`) — SERP       | `data.parsing`                 | `list` (array)            | Interactive run (Step 2A)   |
| CLI (`nimble agent run`) — PDP        | `data.parsing`                 | `dict` (flat)             | Interactive run (Step 2A)   |
| REST API — ecommerce SERP             | `data.parsing`                 | `list` (array)            | Script generation (Step 2B) |
| REST API — non-ecommerce SERP         | `data.parsing.entities.{Type}` | `dict` with nested arrays | Script generation (Step 2B) |
| REST API — PDP                        | `data.parsing`                 | `dict` (flat)             | Script generation (Step 2B) |

Always check `typeof`/`isinstance` before iterating REST responses.

## Step 1: Route

From `$ARGUMENTS`, detect 3 things:

**1. Clarity** — `clear` (default) or `needs-planning`

Only `needs-planning` when ALL of these are absent: a target URL/site/domain, clear data to extract, a single well-scoped task. Most requests are `clear`.

**2. Agent match** — run `nimble agent list --limit 100 --search "<domain or vertical>"` (CLI, Bash). Use the user's named domain/site as the search term (e.g. `--search "amazon"`, `--search "jobs"`, `--search "ecommerce"`). This is ALWAYS the first action. For multi-source requests (e.g., "compare Amazon and Walmart prices"), run one search per source. If no match found for a source, route it to Discovery (Step 1D).

| Result                                                            | Route                                                                                                                                                                                                          |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Exact match                                                       | Show schema summary + `AskUserQuestion`: "Use this agent" (Recommended) / "Create new agent" → Step 3                                                                                                          |
| Close match (same domain/type, missing fields or different scope) | Show schema gaps + `AskUserQuestion`: "Update this agent" (Recommended) / "Create new agent". **Always recommend update** — it preserves existing extraction logic and is faster than generating from scratch. |
| 2+ plausible matches                                              | Show table + `AskUserQuestion` with top matches + "Update closest agent" (Recommended). Pick the agent with the most field overlap.                                                                            |
| 0 matches                                                         | Launch **Discovery Task agent** (Step 1D) → results inform Step 3. **This is the ONLY case where generating a new agent is appropriate.**                                                                      |

**3. Execution mode** — `interactive` (default) or `script`

**Interactive is ALWAYS the default.** Route to script generation (Step 2B) ONLY when BOTH conditions are met: (a) scale is explicitly >50 items or the user provides a batch input file, AND (b) the user explicitly asks for code, a script, a CSV export, or batch processing. Words like "dataset", "compare", "multi-source", or "2 sources" do NOT trigger script mode — run these interactively. **Script generation writes code that calls an existing agent** — it does not create new agents. If no agent exists yet, resolve that first (Step 3) before generating a script.

### Step 1P: Plan mode (rare — only when `needs-planning`)

1. **Clarify** — `AskUserQuestion` to resolve critical unknowns (max 2 questions). Focus on: what site(s), what data fields, what output format.
2. **Explore** — `nimble agent list --limit 100 --search "<domain>"` (CLI, once per domain). For unfamiliar domains, launch Discovery Task agents (Step 1D).
3. **Present plan** — gap analysis table:

| #   | Site / Data Source   | Agent                  | Status   |
| --- | -------------------- | ---------------------- | -------- |
| 1   | amazon.com products  | amazon-product-details | Existing |
| 2   | walmart.com products | —                      | Generate |

4. **Execute** — Step 2 for existing agents, Step 3 for generations (as Task agents).

### Step 1D: Discovery (Task agent — for unfamiliar domains)

Launch when `nimble agent list --limit 100 --search "<domain>"` returns 0 matches for the target domain and it needs exploration. Runs as `Task(subagent_type="general-purpose", run_in_background=False)`. The foreground tells the user: _"Exploring {domain} to understand available data..."_

**Task prompt template:**

```
Explore {domain} for {user_intent}.

Use the Nimble CLI to discover the site structure and available data:

1. **Map the site** (understand URL patterns and sections):
   ```bash
   nimble map --url "https://{domain}" --limit 50
   ```
   This reveals listing pages, detail pages, site sections, and URL patterns.

2. **Search for real examples** (deep content extraction):
   ```bash
   nimble search --query "{domain} {keywords}" --max-results 5
   ```
   This fetches and extracts full page content from each result, giving you product listings, field structures, and example data.

**Return a structured report:**
- DOMAIN: {domain}
- ESTIMATED_ITEMS: count matching query
- LISTING_URL_PATTERN: e.g., /category/filter?color=green
- DETAIL_URL_PATTERN: e.g., /p/{slug}-{SKU}.html
- AVAILABLE_FIELDS: list of extractable fields (name, price, description, materials, etc.)
- MISSING_FIELDS: fields the user wants but the site doesn't have (e.g., ratings, reviews)
- RECOMMENDED_APPROACH: generate custom agent / use existing agent from {alternative} / combine sources
- SAMPLE_URLS: 2–3 example URLs for agent generation
- LIMITATIONS: login walls, pagination limits, JS rendering, etc.

Do NOT use AskUserQuestion. Do NOT use nimble_find_search_agent, nimble_run_search_agent, or nimble_url_extract.
Do NOT use WebSearch, WebFetch, or any non-Nimble-CLI search/fetch method.
```

On receiving the report, the foreground conversation:

1. Presents key findings to the user.
2. If data gaps exist (e.g., missing ratings), asks the user via `AskUserQuestion` how to proceed.
3. Routes to Step 3 (generate) with the discovery context, or Step 2 if existing agents cover the need.

## Step 2: Run existing agent

Two sub-paths based on execution mode.

### 2A: Interactive (small scale, display output)

**2A-1.** Run `nimble agent get --template-name <name>` (CLI). Present schema in markdown tables:

- **Input parameters:** name, required, type, description, example
- **Output fields:** key fields from `skills` dict

See **`references/agent-api-reference.md`** > "Input Parameter Mapping" for the full `input_properties` format and mapping rules.

**2A-2.** Always confirm before running via `AskUserQuestion`:

```
question: "Run {agent_name} with these parameters?"
header: "Confirm"
options:
  - label: "Run agent (Recommended)"
    description: "Execute {agent_name} with {summary of inferred parameters}"
  - label: "Change parameters"
    description: "Adjust input parameters before running"
  - label: "Create new agent"
    description: "Create a custom agent instead (Step 3)"
```

**2A-3.** Run `nimble agent run --agent <name> --params '{...}'` (CLI). Present results as markdown table. Always ask what to do next:

```
question: "What next?"
header: "Next step"
options:
  - label: "Done"
    description: "Finish with these results"
  - label: "Run again"
    description: "Re-run with different parameters"
```

Do NOT offer script generation as a next step unless the user explicitly mentions needing large-scale extraction (>50 items) or batch processing. Script generation is not a natural follow-up to interactive runs.

**Bulk (2–5 URLs):** Run per URL, aggregate results, handle individual failures without aborting. See **`references/batch-patterns.md`** > "Interactive batch extraction".

### 2B: Script generation (ONLY for large-scale, high-volume tasks)

**This step is ONLY reached when the user explicitly needs to process >50 items at scale or requests batch code/script generation.** Normal requests — even multi-source or "dataset" requests — are handled interactively via Step 2A. Writes a runnable script that calls an existing Nimble agent at scale via the SDK/REST API. This does NOT create new agents — the agent must already exist. Runs as a Task agent. The foreground infers language, launches the agent, and presents the generated script for confirmation.

**2B-1.** Infer language from project context (foreground, before launching):

| Project file                                 | Language          |
| -------------------------------------------- | ----------------- |
| `pyproject.toml`, `requirements.txt`, `*.py` | Python            |
| `package.json`, `tsconfig.json`              | TypeScript/Node   |
| `go.mod`                                     | Go (REST API)     |
| None of the above                            | Default to Python |

**2B-2.** Launch script generation Task agent: `Task(subagent_type="general-purpose", run_in_background=False)`.

**Task prompt template:**

```
Write a {language} script that calls existing Nimble agent(s) at scale via SDK/REST API.

**Use the Nimble CLI to inspect agent schemas (via Bash, NOT MCP):**
```bash
nimble agent get --template-name <agent_name>
```
This returns the full input/output schema for the agent.

**CRITICAL: Use CLI (Bash) for all Nimble operations. NEVER use WebSearch, WebFetch, curl, or wget. NEVER construct MCP endpoint URLs manually.**

**Existing agents to call:** {agent_names}
**User intent:** {user_prompt}
**Output format:** {csv/json/etc}
**Scale:** {number of items/queries}

This is SCRIPT GENERATION — writing code that calls existing agents. Do NOT create new agents
(no nimble_agents_generate/update/publish). The agents listed above already exist.

Steps:
1. Run `nimble agent get --template-name <agent>` (CLI) for each agent to inspect input_properties and skills.
2. Read the reference files:
   - `references/sdk-patterns.md` (Python) or `references/rest-api-patterns.md` (other languages)
   - `references/batch-patterns.md` (for multi-store normalization)
3. Write a complete, ready-to-run script with:
   - Smoke test first — validate a single query before full batch. Abort on failure.
   - Progress reporting — compact single-line status after each poll cycle.
   - Pagination handling for large result sets.
   - Multi-store field normalization (if applicable).
   - Output to {format}.
   - Incremental file writes for large pipelines (50+ jobs).

Return the complete script and a brief summary of:
- Agent schemas used (input params, key output fields)
- Normalization mappings (if multi-store)
- Total estimated API calls

Do NOT use AskUserQuestion. Do NOT use nimble_find_search_agent or nimble_run_search_agent.
Do NOT call nimble_agents_generate, nimble_agents_update_from_agent, nimble_agents_update_session, or nimble_agents_publish.
Do NOT use WebSearch, WebFetch, bash curl, or any non-MCP search/fetch method.
```

**2B-3.** Present the generated script and confirm execution via `AskUserQuestion` (foreground):

```
question: "Run this script?"
header: "Confirm"
options:
  - label: "Run script (Recommended)"
    description: "Execute the generated script"
  - label: "Edit first"
    description: "Review and modify the script before running"
```

**No agent validation step here.** The 50-input validation flow (Step 3) is only for agent creation/update. Script generation uses an existing, already-validated agent — just write the script and run it.

## Step 3: Update existing agent or create new (on the Nimble platform)

Updates an existing agent (preferred) or creates a new one on Nimble's platform. **Default to update** when a close-match agent was found in Step 1 — pass the existing agent name to the Task agent so it uses `nimble_agents_update_from_agent` instead of `nimble_agents_generate`. Only create a new agent when Step 1 returned 0 matches. This is NOT code/script generation — it creates/modifies an extraction definition callable via Step 2A or 2B. ALWAYS runs as a Task agent (`run_in_background=False`).

### 3-1. Create a stable `session_id` (UUID v4).

### 3-2. Ask the user ONCE (foreground only — agent creation/update ONLY, never for script generation):

```
question: "Run refinement-validation before publishing?"
header: "Validate"
options:
  - label: "Yes, validate (Recommended)"
    description: "Discovery → generate → validate 50 inputs (80% pass) → publish. Auto-retries on failure."
  - label: "No, generate only"
    description: "Generate → publish immediately without validation testing"
```

### 3-3. Launch Task agent

Set `refine_validate` to the user's choice. Launch `Task(subagent_type="general-purpose", run_in_background=False, max_turns=50)` using the prompt template from **`references/generate-update-and-publish.md`** (includes MCP tool registry, lifecycle phases, and all rules). Tell the user: "Agent generation started. I'll report results when complete."

The Task agent executes a closed-loop lifecycle: Discovery → Create/Update → Poll → Validate → Publish → Report. On failure, it auto-triggers an update loop (max 2 cycles, 15-minute wall-clock timeout). See the reference file for complete details.

### 3-4. Present report

When the Task agent completes, present the report. On success, route to Step 2A or 2B. On failure after max cycles, offer:

```
question: "Agent validation did not reach 80% pass rate. How to proceed?"
header: "Next step"
options:
  - label: "Publish anyway"
    description: "Publish with current pass rate ({rate}%)"
  - label: "Update agent"
    description: "Provide specific instructions to refine the agent"
```

## Step 4: Final response

End with a concise summary table:

| Field             | Value                      |
| ----------------- | -------------------------- |
| Agent(s) used     | `agent_name`               |
| Source            | Existing / Generated       |
| Records extracted | count                      |
| Output            | Displayed / `filename.csv` |

Include the extraction results (or top N if large).

## Additional references

Load reference files **only during large-scale script generation (Step 2B)** or agent creation (Step 3). Do NOT load these for interactive runs (Step 2A) — MCP tool schemas are sufficient.

**For script generation (Step 2B) only:**

- **`references/sdk-patterns.md`** — Running agents, async endpoint, batch pipelines, incremental file writes.
- **`references/rest-api-patterns.md`** — REST API patterns for TypeScript, Node, curl, and other non-Python languages.
- **`references/batch-patterns.md`** — Multi-store comparison, normalization, interactive batch, codegen walkthrough.

**For agent creation/update (Step 3) only:**

- **`references/generate-update-and-publish.md`** — Full agent creation/update lifecycle: discovery, creation, polling, SDK validation (50 inputs, 80% threshold), publish, reporting, update loop.

**General (any step, load as needed):**

- **`references/agent-api-reference.md`** — MCP tools reference plus input parameter mapping.
- **`references/error-recovery.md`** — Error handling and recovery patterns.

## Guardrails

- **Agent creation/update runs in Task agents.** Generation takes 1-3 minutes — use a background Task agent for the generate → poll → publish loop. See [Delegation model](#delegation-model).
- **All operations use CLI (Bash).** MCP tools are a fallback only when CLI is unavailable.
- **All web search MUST use `nimble search` (CLI).** NEVER use `WebSearch`, `WebFetch`, `curl`, or `wget` — in foreground or Task agents.
- **Every Task agent prompt MUST include the CLI commands block** (see [Delegation model](#delegation-model)).
- **Never** use `nimble_find_search_agent`, `nimble_run_search_agent`, or any WSA template tools.
- **Update state machine:** use `nimble agent generate --from-agent` to iterate on existing agents. Each iteration creates a new generation to poll.
- **Hard 429 rule.** On quota errors: stop, report exhaustion. Do not retry or switch tools.
- Published agents are automatically forked when updated. UBCT-based agents cannot be updated — generate a new one instead.
- **Never load SDK/batch references for interactive runs (Step 2A).** CLI output from `nimble agent get --template-name` is sufficient. Load references only for Step 2B (script generation) and Step 3 (agent creation).
- Present results in markdown tables. Never show raw JSON.
