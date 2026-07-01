# Xquik Plugin for Claude Code and Cowork

Use Xquik to research X content, monitor accounts or keywords, collect media, export followers, and prepare confirmation-gated actions from Claude.

## MCP Integration

This plugin configures the Xquik MCP server:

```json
{
  "xquik": {
    "type": "http",
    "url": "https://xquik.com/mcp"
  }
}
```

Set `XQUIK_API_KEY` before using the MCP server. Create an API key from the Xquik dashboard.

## Included Skill

| Skill | What it does |
| --- | --- |
| `/xquik:x-research` | Plans X research workflows, chooses the narrowest Xquik MCP action, and formats results for analysis or export |

## Common Workflows

- Search posts and replies for a topic
- Inspect public profile context
- Export follower or following lists
- Collect tweet media for analysis
- Prepare monitor and webhook workflows
- Draft confirmation-gated X actions

## Installation

### Claude Code

```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install xquik@knowledge-work-plugins
```

Then set `XQUIK_API_KEY` in your environment and restart Claude Code.

## Links

- Docs: https://docs.xquik.com/mcp/overview
- Dashboard: https://dashboard.xquik.com
- Repository: https://github.com/Xquik-dev/x-twitter-scraper
- npm: https://www.npmjs.com/package/x-twitter-scraper

## License

Apache-2.0. See [LICENSE](LICENSE).
