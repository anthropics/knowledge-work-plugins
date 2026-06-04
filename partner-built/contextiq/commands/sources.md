---
description: List the enterprise knowledge sources available to you through ContextIQ
---

Retrieve and present the enterprise knowledge sources the current user is authorized to access through ContextIQ.

1. Call the `contextiq` MCP server's `list_sources` tool with no arguments.

2. Present the sources in an organized, scannable format:
   - Group by type or domain where applicable (e.g., policies, technical docs, financial records)
   - For each source: name, description, and the kinds of questions it can answer
   - Note any scope or access limitations visible in the metadata

3. Close with a prompt: "You can query any of these sources with `/contextiq:ask <your question>`."

4. If no sources are returned:
   - Inform the user that no authorized sources are currently available
   - Suggest contacting their administrator to confirm their entitlements are configured

5. If the MCP server is not connected, guide the user to run `./contextiq-setup` with the setup URL or config file provided by their admin. If they are the admin, point them to the quickstart guide: https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md
