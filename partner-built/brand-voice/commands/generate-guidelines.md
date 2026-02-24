---
description: Generate brand voice guidelines from documents, transcripts, discovery reports, or any combination
argument-hint: "<sources — documents, transcripts, or description of what you have>"
---

**MANDATORY FIRST STEP — do this before anything else, including reading sources or processing arguments.** Check whether the user has a working folder selected for this session. You must verify this before starting any guideline generation work. If there is no working folder, stop and warn the user: "You don't have a working folder selected. Without one, I can't save guidelines to a file — they'll only exist in this conversation and won't persist to future sessions. Please select a working folder and re-run this command. If you'd like to proceed anyway, let me know."  Wait for the user to confirm before continuing.

Generate comprehensive, LLM-ready brand voice guidelines from whatever sources the user provides — brand documents, conversation transcripts, a discovery report from `/brand-voice:discover-brand`, or direct input.

Process the sources specified in $ARGUMENTS. If none specified, check:
1. Whether a discovery report was generated in this session
2. `.claude/brand-voice.local.md` for known brand material locations
3. Connected platforms (Notion, Confluence, Google Drive, Box, SharePoint, Gong) for existing materials
4. If nothing is available, suggest running `/brand-voice:discover-brand` first

Follow the guideline-generation skill instructions to:
1. Identify and classify all available sources (discovery report, documents, transcripts)
2. Delegate to document-analysis and conversation-analysis agents as needed
3. Synthesize findings into unified guidelines with "We Are / We Are Not" table and tone-by-context matrix
4. Assign confidence scores per section
5. Surface open questions with agent recommendations for any ambiguity
6. Present key findings and offer next steps
7. Save guidelines to `.claude/brand-voice-guidelines.md` inside the user's working folder (archiving any existing file first). Do NOT use a relative path from the agent's current working directory — in Cowork, the agent runs from a plugin cache directory, not the user's project.

After generation, guidelines are saved locally so `/brand-voice:enforce-voice` can automatically find them in future sessions.

Supported document formats: PDF, PowerPoint, Word, Markdown, plain text.
Supported transcript sources: Gong (MCP), Granola (MCP), Notion meeting notes, manual uploads.
