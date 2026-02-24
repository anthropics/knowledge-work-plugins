---
description: Apply brand guidelines to content creation
argument-hint: "<content request>"
---

**MANDATORY FIRST STEP — do this before anything else, including loading guidelines or processing the content request.** Check whether the user has a working folder selected for this session. You must verify this before starting any enforcement work. If there is no working folder, stop and warn the user: "You don't have a working folder selected. Without one, I can't load saved guidelines from a previous session, and any guidelines generated in this conversation won't be saved for future sessions either. Please select a working folder and re-run this command. If you'd like to proceed anyway (guidelines will only be usable in this session), let me know."  Wait for the user to confirm before continuing.

Load the user's brand guidelines and apply them to the content request provided in $ARGUMENTS.

Find brand guidelines using this sequence (stop as soon as found):
1. Session context — check if guidelines were generated earlier in this conversation
2. Local guidelines file — check for `.claude/brand-voice-guidelines.md` inside the user's working folder. Do NOT use a relative path from the agent's current working directory (in Cowork, the agent runs from a plugin cache directory). If no working folder is set, skip this step.
3. If not found, ask the user to run `/brand-voice:discover-brand`, `/brand-voice:generate-guidelines`, or paste guidelines directly

Once guidelines are loaded, follow the brand-voice-enforcement skill instructions to:
1. Analyze the content request (type, audience, key messages, requirements)
2. Apply voice constants ("We Are / We Are Not") and flex tone for context (formality, energy, technical depth)
3. Generate content applying voice, tone, messaging, and terminology guidelines
4. Validate output against brand do's and don'ts
5. Present the content with a brief explanation of brand choices made
6. Note any open questions from guidelines that affect this content
7. Offer to refine based on feedback
