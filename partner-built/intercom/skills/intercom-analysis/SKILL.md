---
name: intercom-analysis
license: MIT
description: >
  Analyze Intercom conversations to identify support patterns, investigate
  customer issues, and look up contacts and companies. Use when the user asks
  to "analyze conversations", "find support patterns", "search Intercom",
  "look up a customer", "investigate a customer issue", "check contact info",
  or asks questions about their Intercom data.
---

# Intercom Analysis

Use the Intercom MCP server to analyze customer conversations, look up contacts and companies, identify support patterns, and investigate customer issues.

Refer to `references/mcp-tools.md` for detailed tool reference, query DSL syntax, search strategies, and field-level documentation for each MCP tool.

## Pattern Analysis Workflow

When the user asks to analyze patterns or trends in their support data, follow this workflow:

1. **Define scope.** Clarify what the user wants to analyze — a time period, topic, customer segment, or conversation state. Ask if unclear.

2. **Fetch a representative sample.** Search for conversations matching the scope. Retrieve at least 10–20 conversations to establish meaningful patterns. Paginate if the first page is insufficient.

3. **Read conversation details.** For each relevant conversation, fetch the full conversation to read the actual messages. Summaries from search results alone are often insufficient for pattern analysis.

4. **Identify recurring themes.** Group conversations by:
   - Common topics or keywords
   - Product areas or features mentioned
   - Error messages or symptoms reported
   - Resolution approaches used
   - Time to resolution

5. **Quantify and summarize.** Present findings with counts and proportions (e.g., "8 of 15 conversations mention timeout errors"). Highlight the most common patterns first.

6. **Recommend actions.** Based on patterns, suggest concrete next steps — knowledge base articles to create, bugs to investigate, or process improvements.

**Output artifact:** Produce a markdown report with the following structure:

- **Theme Summary** — Table of identified themes with conversation counts and percentage of total
- **Top Issues** — The 3–5 most common issues with representative conversation excerpts
- **Recommended Actions** — Prioritized list of concrete next steps based on the patterns found

## Issue Investigation Steps

When a user asks you to investigate a specific customer issue or incident:

1. **Identify the customer.** Look up the contact by email, name, or ID. Get their full profile to understand their account context (plan, company, location, custom attributes).

2. **Trace the timeline.** Search for all conversations from this contact, ordered by date. Fetch each conversation to build a chronological narrative of their interactions.

3. **Check for multi-customer impact.** Search for conversations from other contacts mentioning the same symptoms, error messages, or affected feature. This determines if the issue is isolated or widespread.

4. **Examine conversation details.** For the most relevant conversations, read through the full thread including internal notes. Notes from teammates often contain diagnostic information and root cause analysis.

5. **Summarize findings.** Present:
   - A timeline of the customer's interactions
   - The core issue and any error messages
   - What was tried and what resolved it (if anything)
   - Whether other customers are affected
   - Links to the relevant conversations

**Output artifact:** Produce a timeline summary with:

- **Customer Context** — Contact details, company, plan, and account attributes
- **Interaction Timeline** — Chronological list of conversations with dates, channels, and outcomes
- **Impact Assessment** — Whether the issue affects other customers, with links to related conversations

## Best Practices

- **Start broad, then narrow.** Begin with a general search to understand the landscape, then apply filters to focus on what matters.

- **Always cite conversation links.** When referencing specific conversations, include their IDs so the user can find them in the Intercom inbox. Format as: `Conversation #12345`.

- **State data limitations.** If search results are paginated and you've only seen the first page, say so. If the data doesn't support a conclusion, be explicit about what would be needed to confirm it.

- **Respect data freshness.** The MCP server returns live data from the Intercom workspace. Results reflect the current state — if the user asks about historical trends, note that conversation states may have changed since the events occurred.

- **Combine tools effectively.** A typical workflow involves `search` or `search_conversations` to find relevant items, then `get_conversation` or `get_contact` to get full details. Don't try to answer complex questions from search results alone.

- **Handle empty results gracefully.** If a search returns no results, suggest alternatives: broaden the query with fewer or different keywords, try a different object type (contacts instead of conversations, or vice versa), check for typos in email addresses or names, or run an unfiltered search first to confirm data exists.

- **Format search results for scannability.** Present results as clean tables. For conversations: ID | Subject | State | Last Updated (with relative timestamps). For contacts: ID | Name | Email | Last Seen. After displaying results, offer to fetch full details (e.g., "Want me to pull up the full thread for conversation #12345?" or "I can get the complete profile — want to see it?").

## Troubleshooting

### MCP Server Disconnected
Error: Tool calls fail with connection/timeout errors
Cause: MCP server unreachable or authentication expired
Solution: Re-authenticate, check network, try again later

### Search Returns 0 Results
Error: Empty result set when matches expected
Cause: Query too narrow, wrong field names, or no matching data
Solution: Broaden filters, try different object type, run unfiltered search first

### Workspace Has No Conversations
Error: All conversation searches return empty
Cause: New/unused workspace or access scope limitation
Solution: Confirm workspace has data, try contact/company searches instead
