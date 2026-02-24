---
name: discover-brand
description: >
  This skill orchestrates autonomous discovery of brand materials across enterprise
  platforms (Notion, Confluence, Google Drive, Box, SharePoint, Figma, Gong, Granola, Slack).
  It should be used when the user asks to "discover brand materials",
  "find brand documents", "search for brand guidelines", "audit brand content",
  "what brand materials do we have", "find our style guide", "where are our brand docs",
  "do we have a style guide", "discover brand voice", "brand content audit",
  or "find brand assets".
---

# Brand Discovery

Orchestrate autonomous discovery of brand materials across enterprise platforms. This skill coordinates the discover-brand agent to search connected platforms (Notion, Confluence, Google Drive, Box, Microsoft 365, Figma, Gong, Granola, Slack), triage sources, and produce a structured discovery report with open questions.

## Discovery Workflow

### 0. Orient the User

Before starting, briefly explain what's about to happen so the user knows what to expect:

"Here's how brand discovery works:

1. **Search** — I'll search your connected platforms (Notion, Google Drive, Slack, etc.) for brand-related materials: style guides, pitch decks, templates, transcripts, and more.
2. **Analyze** — I'll categorize and rank what I find, pull the best sources, and produce a discovery report with what I found, any conflicts, and open questions.
3. **Generate guidelines** — Once you've reviewed the report, I can generate a structured brand voice guideline document from the results.
4. **Save** — Guidelines are saved to `.claude/brand-voice-guidelines.md` in your working folder once you approve them. Nothing is written until that step.

The search usually takes a few minutes depending on how many platforms are connected. Ready to get started?"

Wait for the user to confirm before proceeding. If they have questions about the process, answer them first.

### 1. Check Settings

Read `.claude/brand-voice.local.md` if it exists. Extract:
- Company name
- Which platforms are enabled (notion, confluence, google-drive, box, microsoft-365, figma, gong, granola, slack)
- Search depth preference (standard or deep)
- Max sources limit
- Any known brand material locations listed under "Known Brand Materials"

If no settings file exists, proceed with all connected platforms and standard search depth.

### 2. Validate Platform Coverage

Before confirming scope, check which platforms are actually connected and classify them:

**Document platforms** (where brand guidelines, style guides, templates, and decks live):
- Notion, Confluence, Google Drive, Box, Microsoft 365 (SharePoint/OneDrive)

**Supplementary platforms** (valuable for patterns, but not where brand docs are stored):
- Slack, Gong, Granola, Figma

Apply these rules:

1. **If zero document platforms are connected**: **Stop.** Tell the user: "You don't have any document storage platforms connected (Google Drive, SharePoint, Notion, Confluence, or Box). Brand guidelines and style guides almost always live on one of these. Please connect at least one before running discovery. Gong/Granola/Slack transcripts are valuable supplements but unlikely to contain formal brand documents."

2. **If no Google Drive AND no Microsoft 365 AND no Box**: **Warn** (but proceed): "None of your primary file storage platforms (Google Drive, SharePoint, Box) are connected. Brand documents frequently live on these platforms. Discovery will proceed with [connected platforms], but results may have significant gaps. Consider connecting Google Drive or SharePoint."

3. **If only one platform total is connected**: **Warn** (but proceed): "Only [platform] is connected. Discovery works best with 2+ platforms for cross-source validation. Results from a single platform will have lower confidence scores."

### 3. Confirm Scope with User

Before launching discovery, confirm:
- Which platforms to search (default: all connected)
- Whether to include conversation transcripts (Gong, Granola) or just documents
- Any known locations to prioritize

Keep this brief — one question, not a questionnaire.

### 4. Delegate to Discover-Brand Agent

Launch the discover-brand agent via the Task tool. Provide:
- Company name (from settings or user input)
- Enabled platforms
- Search depth
- Any known URLs or locations to check first

The agent executes the 4-phase discovery algorithm autonomously:
1. **Broad Discovery** — parallel searches across platforms
2. **Source Triage** — categorize and rank sources
3. **Deep Fetch** — retrieve and extract from top sources
4. **Discovery Report** — structured output with open questions

### 5. Present Discovery Report

When the agent returns, present the report to the user with a summary:
- Total sources found and analyzed
- Key brand elements discovered
- Any conflicts between sources
- Open questions requiring team input

### 6. Offer Next Steps

After presenting the report, offer:
1. **Generate guidelines now** — chain to `/brand-voice:generate-guidelines` using discovery report as input
2. **Resolve open questions first** — work through high-priority questions before generating
3. **Save report** — store the discovery report to Notion or as a local file
4. **Expand search** — search additional platforms or deeper if coverage is low

## Open Questions

Open questions arise when the discovery agent encounters ambiguity it cannot resolve:
- Conflicting documents (e.g., 2023 style guide vs. 2024 brand update)
- Missing critical sections (e.g., no social media guidelines found)
- Inconsistent terminology across platforms

Every open question includes an agent recommendation. Present questions as "confirm or override" — not dead ends.

## Integration with Other Skills

- **Guideline Generation**: The discovery report is returned by the discover-brand agent via the Task tool. Pass it directly to the guideline-generation skill as structured input, replacing the need for users to manually gather sources.
- **Brand Voice Enforcement**: Once guidelines are generated from discovery, enforcement uses them automatically.

## Error Handling

- If zero platforms are connected, inform the user which platforms the plugin supports and how to connect them.
- If all searches return empty results, flag the discovery as "low coverage" and suggest the user provide documents manually or check platform connections.
- If a platform is connected but returns permission errors, note the gap and continue with other platforms.

## Reference Files

For detailed discovery patterns and algorithms, consult:

- **`references/search-strategies.md`** — Platform-specific search queries, query patterns by platform, and tips for maximizing discovery coverage
- **`references/source-ranking.md`** — Source category definitions, ranking algorithm weights, and triage decision criteria
