# mumo — Claude Code + Cowork plugin

Multi-model deliberation as MCP tools, with an auto-triggering skill. Consult a panel of models (Claude, GPT, Gemini, Grok, Qwen, and more) on contested decisions — architecture, plan review, pricing, strategy — where a single model might be confidently wrong.

Works in both Claude Code (developer audience) and Claude Cowork (knowledge-worker audience). Same plugin, same skill, different distribution marketplaces.

## What's in the box

- **MCP server** — `https://mumo.chat/api/mcp`, five tools: `create_deliberation`, `append_round`, `get_session`, `list_sessions`, `list_models`
- **Auto-triggering skill** — `skills/mumo/SKILL.md` tells the agent *when* to reach for the panel (architecture tradeoffs, plan reviews, contested decisions) so you don't have to

## Install — Claude Code

Inside Claude Code:

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin install mumo
```

## Install — Claude Cowork

Open Claude Desktop → **Cowork** tab → **Customize** → **Browse plugins** → search for `mumo` → **Install**. Or browse the full catalog at [claude.com/plugins](https://claude.com/plugins/).

> **Note:** Claude Code and Cowork have separate plugin panels backed by different marketplaces. Installing in one surface does **not** auto-install in the other — install in each separately.

## API key setup

Both surfaces need a mumo API key:

1. Sign up at https://mumo.chat and create a platform key at [Settings → API Keys](https://mumo.chat/settings/api-keys) (keys start with `mmo_live_`)
2. Export it in your shell:
   ```bash
   export MUMO_API_KEY=mmo_live_YOUR_KEY_HERE
   ```
3. Restart Claude Code or Claude Cowork

## Using the panel

The skill auto-triggers on architecture tradeoffs, plan and design reviews, pre-launch pressure tests, and contested product or pricing decisions — situations where multiple perspectives change the answer. It deliberately skips factual lookups, routine refactoring, and code generation from a clear spec. You can also invoke it explicitly: "run this by a mumo panel" or "get me a second opinion from mumo."

### Try it first

Ask Claude Code something the panel will want to engage with:

> Postgres or MongoDB for our event store given 50k events/day, a Postgres-experienced team, and a 3-month runway? What would we regret 6 months in?

The first round returns each model's prose plus a cross-model claim map showing where the panel agrees and where it splits. You can stop there, or `append_round` with typed snippets (KEEP / EXPLORE / CHALLENGE / CORE / SHIFT) to steer further.

See [mumo.chat/mcp](https://mumo.chat/mcp) for the tool reference, the deliberation loop, and prompt patterns. The canonical trigger language lives in [`skills/mumo/SKILL.md`](skills/mumo/SKILL.md) — that's what Claude Code loads.

## Links

- Product — https://mumo.chat
- MCP reference — https://mumo.chat/docs/mcp/reference
- REST API — https://mumo.chat/docs/api
- Issues — https://github.com/mumo-chat/mumo-mcp/issues

## License

MIT
