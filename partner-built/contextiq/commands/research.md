---
description: Produce a structured research briefing on a topic from authorized enterprise knowledge sources
argument-hint: "<research topic or question>"
---

Produce a structured research briefing on the topic in $ARGUMENTS using ContextIQ's governed knowledge sources.

1. Call the `contextiq` MCP server's `query` tool with the research topic from $ARGUMENTS.

2. If initial results are thin or low-confidence, refine and retry with a more specific formulation of the same topic — up to two additional attempts. Use the strongest results across all attempts.

3. Structure the output as a research briefing with the following sections:

   **Executive Summary**
   Two to three sentences summarising the key finding and its significance.

   **Key Findings**
   Bulleted findings drawn directly from the sources. Each finding must be attributed to its source with an inline citation. Do not include findings that cannot be traced to a specific source.

   **Sources**
   For each source used: document name, relevant excerpt, and how it contributed to the findings.

   **Coverage Gaps**
   Topics or questions within scope that the available sources did not address. Be specific — name what is missing, not just that information was limited.

   **Open Questions**
   Questions the research raises that would require additional sources or expertise to answer.

4. Never speculate or infer beyond what the sources explicitly state. If the evidence is partial, say so in the Executive Summary.

5. If the query returns no results across all attempts:
   - State that no authorized sources matched the research topic
   - Suggest a narrower or differently framed topic
   - Offer to run `/contextiq:sources` to show what knowledge is available

6. If the MCP server is not connected, guide the user to run `./contextiq-setup` with the setup URL or config file provided by their admin. If they are the admin, point them to the quickstart guide: https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md
