# Discovery

This file gives instructions on how to discover ways to connect to the named tool, in a specific order. Once a section turns up a match, stop — no need to go down the other paths. Most of the time something already exists, and finding it takes ten minutes against an hour of building.

---

## 1. Search Claude native connectors

**Primary — `ToolSearch`.** Check whether Claude can already reach this tool:

1. Call `ToolSearch` with the exact product name as the query, e.g. `ToolSearch({query: "ServiceTrade", max_results: 5})`.
2. If that returns nothing relevant, retry once with the vendor's category instead of the brand name (e.g. `"field service management"`).

`ToolSearch` only finds connectors already configured for this session — a miss here doesn't rule out a server existing that just hasn't been added yet. A hit may come back twice, as the owner's own entry and as the plugin's `small-business:<name>` registration; that is one connector: use whichever entry is authorized, the owner's if both (`../../../shared/connector-neutrality.md`, "One connector, two registrations").

**Secondary — search the MCP Registry.** If `ToolSearch` comes up empty, check whether an MCP server exists for this tool anywhere in the open ecosystem:

1. Check `ToolSearch` for a `SearchMcpRegistry` tool — some hosts expose this natively. If it's available, call it with the product name.
2. Otherwise, call `WebFetch` on `https://registry.modelcontextprotocol.io/v0.1/servers?search=<exact product name>` — a public, no-auth API with the same underlying data.

If any of the above turns up a match, this is the answer: guiding the owner through connecting it is the whole job, and the best outcome. Otherwise, continue to section 2.

---

## 2. Search Zapier connections

**Primary path — the Zapier MCP is present.** This plugin declares it in `.mcp.json`, so this is normally the case:

1. Call `ToolSearch` for `discover_zapier_actions` — Zapier's own app/action discovery tool — then run it with the exact product name from Step 1.
2. If it's listed, check for the specific trigger or action this use case needs, not just that the app itself is on Zapier. An app that is on Zapier but lacks the one action the scope needs is not a match — say so plainly and continue to section 3.

**Fallback — the Zapier MCP isn't installed or isn't reachable.** Check the public app directory directly instead:

1. WebFetch `zapier.com/apps/<product-slug>/integrations.md` — the markdown mirror, not the HTML page — to see if the app is listed and what it integrates with.
2. Treat this as lower-confidence than the MCP path — it confirms the app exists on Zapier, but not which specific trigger or action is available. Confirm that once the MCP connection is available.
3. If it's still unclear which surface to use, `zapier.com/llms.txt` and `zapier.com/.well-known/ai-catalog.json` are Zapier's own machine-readable indexes of its discovery surfaces (MCP, SDK, app directory) — a map of where to look, not a search tool themselves.

**Fit and cost.** Zapier is a good fit when the need is a lookup or an action on demand, the volume is low, or the alternative is a fragile custom build. It is a poor fit for pulling large volumes of historical data, or anywhere a per-task cost would add up — Zapier bills per task. See `zapier.com/pricing.md` for plan tiers and how tasks are billed before committing to this path; the estimate goes in front of the owner (`use-zapier.md`, "Estimating the task bill").

If no connection is found for this app or service, continue to section 3.

---

## 3. Search for a documented API

Most modern SaaS has an API, even when the pricing page doesn't mention it. This is for context on what's technically possible — never a path to hand-build against, per the skill's own rule.

1. WebFetch `docs.<vendor>.com` or `developer.<vendor>.com` — most vendors publish API docs at one of these.
2. If neither resolves, search the vendor's support knowledge base for "API," and check the owner's account settings for an API key section — a key section is proof one exists even when undocumented.
3. If still nothing, check the vendor's community forum for integration questions — API existence often surfaces there before it's officially documented.

What to establish once found — auth, endpoints, and limits; skip the SDK docs, tutorials, and marketing pages:

| Question | Why it matters |
|---|---|
| Auth method | OAuth and tokens are fine. Password-only is a problem worth flagging. |
| Rate limits | Determines whether a daily pull is viable |
| The specific endpoints needed | Not the whole API, just what Step 1 scoped |
| Whether the owner's plan includes API access | Frequently gated to higher tiers — check before building |
| Whether writes are supported | Determines what is possible, and what gates are needed |
| The changelog | How often the API breaks — context on the tool's overall reliability, even though nothing gets built against it |

**Check the plan tier early.** Building against an API the owner's subscription doesn't include is a wasted afternoon, and it happens often.

**Documented API or not, this never stops the search — it's context for what you'll say next, never a build path.** Continue to section 4.

---

## 4. Check for a scheduled export

Underrated and often the best answer.

Many systems can email a report or drop a CSV on a schedule — daily, weekly, monthly. If the need is "pull work orders each morning," a scheduled export into a watched inbox does it with almost nothing to break, and nothing to connect on Claude's side — the owner configures it in their own settings.

Where to look: reporting settings, scheduled reports, subscriptions, automated delivery.

**This is not a lesser option.** It has no tokens to expire, no rate limits, no vendor API changes, and no per-task bill. For a once-daily need it is often strictly better than a live integration. Its weakness is latency and a quiet failure mode — the setup and the staleness check are in `paths.md`, section 3.

---

## 5. Genuinely nothing

Rarer than it looks, but real — some older on-premise and vertical systems have no external surface at all.

Say so honestly, and give the options that remain:

```
Straight answer: JobBoss on-premise has no API and isn't on Zapier. Nothing
clean here.

Two things that would work:
  - It can export to CSV manually. If you drop that file weekly, everything
    downstream works from it.
  - There's a scheduled report feature that emails a PDF. Messier to parse,
    but automatic.

The CSV is more reliable. Want to try that?
```

An honest no with a workaround is more useful than a fragile screen-scraping build the owner cannot maintain.

---

## Reporting the finding

Before building anything, state what was found and what it means in time:

```
ServiceTrade isn't in the Claude connector directory, but it's on Zapier
with work-order searches that cover what you need.

One thing: at your volume this lands on Zapier's paid tier. Worth knowing
before we build.

Setup is about twenty minutes on your side. Want me to walk you through it?
```

Remember the rule from the skill: even when the discovery turns up a clean documented API, that is context, not a build path — the build path is Zapier, or a scheduled export when Zapier lacks the tool.

Cost, effort, and blocker in three lines. That is enough for the owner to decide.
