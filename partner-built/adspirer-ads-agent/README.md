# Adspirer MCP Plugin for Claude Code

Cross-platform ad management plugin for Claude Code. Create, analyze, and optimize campaigns across **Google Ads, Meta Ads, TikTok Ads, and LinkedIn Ads** via natural language.

## Installation

```bash
/plugin install adspirer-mcp-plugin
```

Or browse for it in `/plugin > Discover` within Claude Code.

## What It Does

**91 tools** across 4 ad platforms:

| Platform | Tools | Key Capabilities |
|----------|-------|-----------------|
| Google Ads | 39 | Keyword research, Search campaigns, Performance Max, performance analysis, asset management, ad extensions |
| LinkedIn Ads | 28 | Sponsored content, lead gen forms, audience targeting, campaign analytics |
| Meta Ads | 20 | Image campaigns, carousel campaigns, audience management, performance tracking |
| TikTok Ads | 4 | In-feed campaigns, asset validation |

## Plugin Components

### Slash Commands

- `/campaign-performance [platform] [time_period]` -- Analyze campaign performance across any connected platform
- `/keyword-research [business or keywords]` -- Research Google Ads keywords with real CPC data

### Skills

- **ad-campaign-best-practices** -- Campaign creation workflows, budget guidelines, platform-specific strategies, and safety rules

### MCP Server

Connects to the Adspirer remote MCP server at `https://mcp.adspirer.com/mcp` via OAuth 2.1 with PKCE.

## Example Usage

**Performance Analysis:**
```
/campaign-performance google_ads last 30 days
```

**Keyword Research:**
```
/keyword-research emergency plumbing business in Chicago
```

**Campaign Creation (conversational):**
```
Create a Google Performance Max campaign for luxury watches
targeting New York with a $50/day budget
```

**Multi-Platform Strategy:**
```
I want to advertise my SaaS product across Google and LinkedIn.
Research keywords for Google Ads and create a LinkedIn sponsored
content campaign targeting marketing directors.
```

## Authentication

On first use, you'll complete an OAuth 2.1 flow to connect your Adspirer account and ad platform accounts. Requires an Adspirer account ([sign up](https://www.adspirer.com)).

## Links

- [Website](https://www.adspirer.com)
- [MCP Server Repo](https://github.com/amekala/ads-mcp)
- [Privacy Policy](https://github.com/amekala/ads-mcp/blob/main/PRIVACY.md)
- [Terms of Service](https://github.com/amekala/ads-mcp/blob/main/TERMS.md)
- [Support](mailto:abhi@adspirer.com)
