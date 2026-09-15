# Use Zapier

The build path when discovery turned up no native Claude connector. This file covers using the Zapier MCP server itself: authenticating, checking whether an app or action exists, connecting the app's account, enabling exactly the actions the scope named, testing against the owner's actual use case from Step 1 of the skill, and the task bill.

---

## Two modes — say which one, out loud

**On-demand actions (the default).** Zapier's MCP server exposes the tool's actions and Claude calls them only when a skill runs. Nothing is scheduled, nothing polls, no Zap exists in the owner's dashboard, and tasks burn only on actual use. This is what most scopes need — a lead pull when the morning brief runs, a record lookup when the owner asks. Every step below is this mode.

**A Zap (the exception).** A standing automation on Zapier's side that runs without Claude — event fires, Zap acts, around the clock. Build one only when the owner needs something to happen while nobody is talking to Claude. It keeps running and billing on its own, so it gets named in the consent step explicitly, named so it is identifiable in the owner's dashboard six months from now ("Claude: ServiceTrade open work orders," not "Zap 47"), and turned on only after a test run passes.

Owners hear "Zapier" and picture Zaps. If the build is on-demand actions, say so — "no Zaps, nothing runs in the background, Zapier is just the pipe" — or the owner will wonder what invisible machinery got installed.

---

## Step 1 — Authenticate to Zapier

Check whether this is already connected before doing anything else: call `ToolSearch` for `discover_zapier_actions`. If it doesn't resolve — only an `authenticate` / `complete_authentication` pair of tools show up — Zapier isn't connected yet.

**If not connected:** call the platform's Zapier authentication tool. It returns an authorization URL — share it with the owner and ask them to complete it in their browser. The rest of the tool set becomes available automatically once they finish. If the redirect page errors out, have the owner retry from the connector's own settings page; never ask them to paste the callback URL or an authorization code into chat — that puts a credential in the transcript, which Step 3 of the skill forbids.

This authenticates the Zapier platform connection only — it is **not** yet the specific app (ServiceTrade, QuickBooks, whatever). That's Step 3, below, and it's a separate step per app.

---

## Step 2 — Check whether the app and action exist

Call `discover_zapier_actions` with the exact product name from Step 1 of the skill, and read back the counts: read/write/search action totals and category. If nothing comes back, the app isn't on Zapier — continue with `discovery.md`, section 3. **`selected_api` must come verbatim from this call — never guess or construct it.** Zapier's own example: Gmail is `GoogleMailV2CLIAPI`, not `GmailCLIAPI`.

Then pick the actions from the scope, not from the app page: find the one search or read action, and the fewest write actions, that deliver exactly what Step 1 defined, and ignore everything else the app offers. Check each action's fields before promising anything — if the owner's scope needs a field the action doesn't return, that is a deviation to surface before building, not after. An app that is on Zapier but lacks the specific action the scope needs is not a match; say why, plainly, and continue with `discovery.md`, section 3.

---

## Step 3 — Connect the app's own account

Call `manage_zapier_connections` with the `selected_api` from Step 2 to check the connection. If none exists yet, it returns an auth URL (Zapier calls it `connectAuthUrl` in its own error text) — share it with the owner and ask them to confirm once they've connected on Zapier's page. The owner signs into their tool on Zapier's page, never in chat; nothing can run until they do, which makes the click the natural consent moment. Then:

1. Call `list_zapier_connections` to find the new `connection_id`.
2. Call `manage_zapier_connections` again with that `connection_id` as `default_connection_id`. **An app requires a default connection before any of its actions can run — even with only one connection.** This is by design: Zapier makes the owner choose consciously rather than picking one silently when multiple accounts exist.
3. **If the owner has multiple accounts for the same app** (two Slack workspaces, a personal and a work Gmail), don't fight over which one is default — pass that connection's specific `connection_id` on each `execute_zapier_read_action` / `execute_zapier_write_action` call instead.

---

## Step 4 — Enable the action, then trim to the scope

Call `enable_zapier_action` with the `selected_api` and the specific action Step 2 chose, plus `app_display_name` so confirmations read as "Gmail," never a raw API ID.

**Enabling does not behave like a menu.** An enable call with no action named turns on every action the app has — including delete, send-email, and raw API request — and enabling one action can switch on a related bundle (asking for one "find" action may enable four). So, every time: enable, then call `inspect_zapier_actions` to read back what is actually on, then `disable_zapier_action` for everything the scope didn't name. The shipped list matches the approved scope exactly — an owner who approved read-only lead pulls must not end up with a live delete action they never heard about.

If a call still fails with a message like:

```
No default connection is set for Outreach, which is required before running
its actions.
```

Step 3 above wasn't completed — the error message itself names the fix; follow it rather than treating it as a dead end.

---

## Step 5 — Test against the owner's actual use case

1. Call `inspect_zapier_actions` with the `tool_name` for the read action Step 2 chose, to get its exact parameter schema.
2. **Resolve ambiguous matches carefully.** If the owner gave partial or ambiguous information — a first name, a search term with several close matches — a lookup returning one result is not proof it's the right one. Enumerate the candidates and let the owner pick rather than guessing.
3. Call `execute_zapier_read_action`, show the real data it pulled, and ask if it's correct. That's the only way to confirm the connection is reading their actual data and nothing quietly wasn't mapped.

**Write actions get the same scrutiny plus a confirmation gate.** They have real, often irreversible side effects — confirm the target whenever there's any doubt, and every write gets an approval gate regardless of what the owner asked for.

---

## Estimating the task bill

Zapier bills per task — roughly, every `execute_zapier_*_action` call that runs. The estimate goes in front of the owner before any build.

1. **Volume:** how many calls per month, from the owner's own numbers in Step 1. 40 work orders a day is about 1,200 a month.
2. **Tier:** see `zapier.com/pricing.md` for current plans and task allowances. **Never quote pricing from memory** — Zapier changes tiers and allowances regularly.
3. **Overage:** say what happens past the limit — plans differ on whether calls pause or bill as overage. A paused plan is silent; see "How this breaks."

**If it is a Zap,** the arithmetic changes: every action step that runs on every record that gets through is a task, so count steps per event, and put a Filter by Zapier step immediately after the trigger, before any action that costs a task, on the narrowest condition the scope defines. Filtered-out runs are cheaper than full runs, and most scopes only want a subset (open work orders, not all work orders). That filter is the single biggest lever on the monthly bill.

If the volume makes per-task billing absurd — a nightly pull of two thousand records — stop and say so plainly rather than presenting a bad Zapier bill as the only option. This is still not a reason to hand-build against the app's raw API; a scheduled export (`discovery.md`, section 4) is usually the right answer at that volume.

---

## How this breaks

- **The owner disconnects the app account inside Zapier**, which breaks every call using that connection at once.
- **Zapier deprecates a trigger or action version**, usually with notice in their changelog and nowhere the owner looks.
- **The task limit is reached**, which can block calls silently depending on the owner's plan settings.

The failure signature is the same for all three: nothing errors, it just produces nothing. **Empty output from a Zapier action is broken until proven empty** — check `inspect_zapier_actions` (or, for a Zap, its run history) before reporting "no records."

---

## The tool set

| Tool | Does |
|---|---|
| `discover_zapier_actions` | Searches Zapier's app catalog — `app` is a free-text query |
| `inspect_zapier_actions` | Inspects currently enabled apps/actions and resolves the exact schema before executing. Call this before every execute call — never guess action names, they aren't intuitive and will fail |
| `enable_zapier_action` | Enables an action for an app, using the `selected_api` from `discover_zapier_actions` |
| `disable_zapier_action` | Removes an action — the trim step after every enable |
| `list_zapier_connections`* | Lists the owner's connected accounts for an app |
| `manage_zapier_connections`* | Connects a new account and/or sets the app's default connection |
| `execute_zapier_read_action` | Runs a search/read action |
| `execute_zapier_write_action` | Runs a write/create action — real, often irreversible side effects |

\* Not documented in `docs.zapier.com/mcp/how-tools-work.md` (see References below), and what Step 3 depends on.

Zapier's own tool descriptions sometimes reference an old name, `list_enabled_zapier_actions` — that tool no longer exists; use `inspect_zapier_actions` instead.

---

## References

**Zapier:**

- `zapier.com/apps/<slug>/integrations.md` — per-app triggers and actions
- `zapier.com/pricing.md` — current plan tiers and task billing
- `zapier.com/llms.txt` — Zapier's machine-readable documentation index
- `zapier.com/.well-known/ai-catalog.json` — Zapier's discovery manifest for its MCP server, SDK, and app directory
- `docs.zapier.com/mcp/how-tools-work.md` — the meta-tools referenced above, markdown mirror

**Claude:**

- `code.claude.com/docs/en/mcp.md` — how Claude Code connects to and manages MCP servers, markdown mirror
- `support.claude.com/en/articles/13837440-use-plugins-in-claude` — how plugins, including bundled connectors, work in Claude Cowork specifically
