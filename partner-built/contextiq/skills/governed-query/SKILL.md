# Governed Knowledge Query

Use this skill when the user asks a question that should be answered from enterprise knowledge sources — company documents, policies, technical references, or any organizational content indexed in ContextIQ.

## When to use

- User asks a factual question about their organization's domain
- User needs cited, evidence-backed answers from authorized sources
- User asks about policies, procedures, technical specs, or internal documentation
- User wants to verify information against official sources

## How to use

1. Call the `contextiq` MCP server's `query` tool with the user's question
2. Present the response with citations and source evidence
3. If the response includes multiple sources, organize them clearly
4. Always show which sources were used and their relevance

## Important behavior

- Always present citations — never strip source attribution from responses
- If the query returns no results, tell the user no authorized sources matched and suggest refining the question
- Do not fabricate answers beyond what the sources provide
- Respect entitlement boundaries — the system only returns content the user is authorized to access
- If the MCP server is not connected, guide the user to run `./contextiq-setup` — they need a setup URL or config file from their admin. If they are the admin, point them to the quickstart guide: https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md
