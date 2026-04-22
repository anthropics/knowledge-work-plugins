---
name: mumo
description: Consult a multi-model panel via mumo's MCP server for contested decisions where a single model's answer might be confidently wrong. Use when the user is making an architecture decision with non-obvious tradeoffs (storage, transport, consistency, caching), reviewing a plan or design doc, pressure-testing a pre-launch spec ("what would we regret"), resolving a product or pricing tradeoff with multiple defensible framings, or explicitly asking "what do different models think" or "get me a panel." Also use when the user uploads a plan/spec and asks for a review, or when a decision has strategic weight that merits more than one voice. Do NOT use for factual lookups, syntax questions, routine refactoring, or code generation from a clear spec. Requires the mumo MCP server to be connected.
---

# mumo — multi-model deliberation panel

The mumo MCP server runs structured deliberations across 2–3 models with claim-level steering. Reach for it when a single model's answer would be too confident on a contested question — architecture, strategy, pricing, plan review.

## Prerequisites

The mumo MCP server is provided by this plugin, but it needs a platform API key via the `MUMO_API_KEY` environment variable. If tools come back with an auth error or the server isn't connected, tell the user and stop — don't try to proceed without it:

1. Create a key at https://mumo.chat/settings/api-keys (keys start with `mmo_live_`)
2. Export it: `export MUMO_API_KEY=mmo_live_…`
3. Restart Claude Code

Full setup at https://mumo.chat/mcp.

## Default workflow

**Start with a single round.** Call `create_deliberation` with `rounds: 1` and pass `application: "Claude Code"`. The first response contains each model's prose plus a cross-model claim map showing where the panel agrees and where it splits.

**Read the claim map before continuing.** Agreements collapse into single rows; splits fan out with each model's position. If the panel has converged on the parts that matter, you may be done. If there are unresolved splits worth steering, call `append_round`.

**Steer with typed snippets, not freeform prompts.** When appending, pass `snippets[]` with verbatim quotes from prior responses tagged by type:

- `KEEP` — this resonates
- `EXPLORE` — go deeper
- `CHALLENGE` — I'm not sold
- `CORE` — this is what it comes down to
- `SHIFT` — this shifted my perspective

The model receiving a snippet sees the framing. A freeform prompt without snippets is a weaker signal.

## Tool map

| When | Call |
|---|---|
| New question | `create_deliberation` |
| Follow-up on existing session | `append_round` |
| Inspect state / poll autonomous | `get_session` |
| User names specific models | `list_models` first |
| Find sessions awaiting next round | `list_sessions` with `status: "ready"` |

## Modes

- **remote** (default) — you drive rounds. Omit `moderator_model`. After round 1 you decide whether to `append_round` or stop, based on what you see.
- **autonomous** — set `moderator_model` and `rounds` (1–14). The AI moderator runs the full arc. Poll `get_session` until `status: "ready"`.

## Moderator name

Pass `moderator_name` on `create_deliberation` set to your own model identity (e.g., "Opus 4.7", "GPT-5.4", "Gemini 3.1 Pro") — the audit trail should reflect who's actually steering the deliberation. Don't use the user's name; their identity is already on the session.

## Surfacing to humans

By default MCP returns per-model prose + a cross-model claim map — the highest-signal artifacts for driving the next round from. If the user will read the output directly (not just your summary of it), also pass `distill` on `create_deliberation`:

- `distill: "summary"` — flowing narrative prose of the deliberation
- `distill: "brief"` — structured: narrative + agreements + disagreements + `continuation.recommendation` (stop / continue / explore)
- `distill: "both"` — both

Distill fires an extra LLM call per round; skip it for pure agent-loop work where you're consuming the output yourself.

## Model picks

If the user doesn't specify models, omit `models` and let mumo select a default roster. If the user names models, call `list_models` first to confirm availability on their tier.

When selecting participant models yourself, the goal is **diverse voices**, not another copy of you:

- **One frontier model from a different provider family than the agent running this session.** If you're Claude, reach for GPT-5.4, Gemini 3.1 Pro, or Grok 4.1. If you're GPT, reach for Opus 4.7, Gemini 3.1 Pro, or Grok 4.1. This is the load-bearing pick — the panel's value comes from a capable voice that wasn't trained alongside yours.
- **One or two lower-cost but capable models** to round out the panel: GLM, Qwen, or Kimi. These add genuine diversity at a fraction of frontier cost and often catch things the frontier misses.

Avoid nano/fast variants (GPT-5.4-nano, Gemini Flash, Haiku) unless the user explicitly asks for a cheap gut-check — the cost delta is usually small and the signal gap is large.

## After the deliberation

If you didn't pass `distill`, summarize the claim map's agreements and disagreements back to the user in plain prose. Either way, offer a link to the session at `https://mumo.chat/s/{session_id}` for the full transcript.

## Confidence scores

If responses include `claim_confidence` or `snippets[].comment_confidence`, these are **self-reported and not calibrated across models.** Surface the `confidence_disclaimer` string if displaying scores.

## Full reference

- Marketing + overview: https://mumo.chat/mcp
- MCP reference: https://mumo.chat/docs/mcp/reference
- REST API (same shapes): https://mumo.chat/docs/api
