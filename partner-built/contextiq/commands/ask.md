---
description: Query enterprise knowledge sources for a cited, evidence-backed answer
argument-hint: "<your question>"
---

Query ContextIQ for a governed, cited answer to the question in $ARGUMENTS.

1. Call the `contextiq` MCP server's `query` tool with the question from $ARGUMENTS.

2. Present the answer with full citations:
   - Lead with the direct answer — no preamble
   - List each source used: document name, relevant excerpt, and relevance to the question
   - If multiple sources contribute different facts, attribute each fact to its source

3. If the query returns no results:
   - Tell the user no authorized sources matched their question
   - Suggest rephrasing or narrowing the question
   - Offer to run `/contextiq:sources` to show what knowledge is available

4. Never fabricate or infer beyond what the sources explicitly state. If the answer is partial, say so and cite what was found.

5. If the MCP server is not connected, guide the user to run `./contextiq-setup` with the setup URL or config file provided by their admin. If they are the admin, point them to the quickstart guide: https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md
