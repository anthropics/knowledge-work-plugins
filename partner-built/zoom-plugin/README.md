# Zoom Plugin

A Claude plugin for planning, building, and debugging Zoom integrations. It helps choose the right Zoom surface, shape implementations, debug failures, and route into the right Zoom references without making the user read the whole doc tree first.

## Installation

Install this directory as a local Claude plugin. The plugin manifest is at [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and the bundled Zoom MCP connectors are defined in [`.mcp.json`](.mcp.json).

Before using the bundled MCP servers, export bearer tokens for the Zoom surfaces you want Claude to use:

```bash
export ZOOM_MCP_ACCESS_TOKEN="your_zoom_user_oauth_access_token"
export ZOOM_DOCS_MCP_ACCESS_TOKEN="your_zoom_docs_mcp_access_token"
export ZOOM_WHITEBOARD_MCP_ACCESS_TOKEN="your_zoom_user_oauth_access_token"
```

## Slash Workflows

Explicit slash workflows implemented as skills under `skills/`:

| Workflow | Description |
|---|---|
| [`/start`](skills/start/SKILL.md) | Start with a Zoom app idea and get routed to the right product and build path |
| [`/setup-zoom-oauth`](skills/setup-zoom-oauth/SKILL.md) | Choose the auth model, scopes, and redirect flow for a Zoom app |
| [`/build-zoom-meeting-app`](skills/build-zoom-meeting-app/SKILL.md) | Build an embedded or managed Zoom meeting flow |
| [`/build-zoom-bot`](skills/build-zoom-bot/SKILL.md) | Build bots, recorders, and real-time meeting processors |
| [`/debug-zoom`](skills/debug-zoom/SKILL.md) | Triage a broken Zoom integration and isolate the failing layer |
| [`/setup-zoom-mcp`](skills/setup-zoom-mcp/SKILL.md) | Decide when Zoom MCP fits and set up a safe Claude workflow |
| [`/build-zoom-rest-api-app`](skills/rest-api/SKILL.md) | Route into Zoom REST endpoints, scopes, and resource patterns |
| [`/build-zoom-meeting-sdk-app`](skills/meeting-sdk/SKILL.md) | Route into embedded Zoom meeting implementation details |
| [`/build-zoom-video-sdk-app`](skills/video-sdk/SKILL.md) | Route into custom video-session implementation details |
| [`/setup-zoom-webhooks`](skills/webhooks/SKILL.md) | Set up Zoom webhook subscriptions, signature verification, and handlers |
| [`/setup-zoom-websockets`](skills/websockets/SKILL.md) | Set up Zoom WebSocket event delivery when it fits better than webhooks |
| [`/build-zoom-team-chat-app`](skills/team-chat/SKILL.md) | Build Team Chat user or chatbot integrations |
| [`/build-zoom-phone-integration`](skills/phone/SKILL.md) | Build Zoom Phone integrations around Smart Embed, APIs, and events |
| [`/build-zoom-contact-center-app`](skills/contact-center/SKILL.md) | Build Contact Center app, web, or native integrations |
| [`/build-zoom-virtual-agent`](skills/virtual-agent/SKILL.md) | Build Virtual Agent web or mobile wrapper integrations |

## Internal Routing Skills

These remain in the plugin as automatic routing helpers, but they are no longer part of the public slash-command surface:

- [`start`](skills/start/SKILL.md)
- [`plan-zoom-product`](skills/plan-zoom-product/SKILL.md)
- [`plan-zoom-integration`](skills/plan-zoom-integration/SKILL.md)
- [`choose-zoom-approach`](skills/choose-zoom-approach/SKILL.md)
- [`design-mcp-workflow`](skills/design-mcp-workflow/SKILL.md)
- [`debug-zoom-integration`](skills/debug-zoom-integration/SKILL.md)

## Deep References

The plugin also keeps the original Zoom product-specific reference library under `skills/`. These are supporting references, not the primary entry surface:

- [`skills/general/`](skills/general/)
- [`skills/rest-api/`](skills/rest-api/)
- [`skills/meeting-sdk/`](skills/meeting-sdk/)
- [`skills/video-sdk/`](skills/video-sdk/)
- [`skills/webhooks/`](skills/webhooks/)
- [`skills/websockets/`](skills/websockets/)
- [`skills/oauth/`](skills/oauth/)
- [`skills/zoom-mcp/`](skills/zoom-mcp/)

## Example Workflows

### Starting from a Zoom app idea

```text
/start Build an internal meeting assistant that joins calls, extracts action items, and stores summaries
```

### Planning a new app

```text
/start Build a React app that lets customers schedule and join Zoom meetings from our product
```

### Debugging a broken webhook

```text
/debug-zoom My Zoom webhook signature verification fails in production but not locally
```

### Designing an MCP flow

```text
/setup-zoom-mcp I want Claude to search meetings, pull recording resources, and create follow-up docs
```

## Connectors

See [CONNECTORS.md](CONNECTORS.md). The plugin works standalone from the bundled skills, and gets supercharged when Claude can use the bundled Zoom MCP servers from [`.mcp.json`](.mcp.json).

## Cross-Platform Notes

This repo is packaged first as a Claude plugin, but it also includes [AGENTS.md](AGENTS.md) for agent ecosystems that use a repo-level discovery file. The reusable core remains the `skills/` tree and its `SKILL.md` files.

## Structure

```text
Zoom Plugin/
├── .claude-plugin/plugin.json
├── .mcp.json
├── CONNECTORS.md
├── skills/
│   ├── plan-zoom-product/
│   ├── plan-zoom-integration/
│   ├── debug-zoom/
│   ├── setup-zoom-mcp/
│   ├── start/
│   ├── choose-zoom-approach/
│   ├── setup-zoom-oauth/
│   ├── build-zoom-meeting-app/
│   ├── build-zoom-bot/
│   ├── design-mcp-workflow/
│   ├── debug-zoom-integration/
│   └── ... existing Zoom reference skills
└── README.md
```

## License

MIT
