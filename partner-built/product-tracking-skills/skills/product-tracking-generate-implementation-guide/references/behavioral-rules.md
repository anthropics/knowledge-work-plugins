# Instrument — Behavioral Rules

1. **Read the SDK reference first.** This is a hard gate. Do not produce any guidance until you have read the matching reference file. If it doesn't cover the user's environment, say so and ask for more information.

2. **Real template code, not pseudocode.** Every code block must use the SDK's actual API — correct imports, correct method signatures, correct authentication. Copy patterns from the reference file.

3. **Guide, not catalog.** Show the patterns with 1-2 examples per call type. Do not map every event from the tracking plan — that's the implementation phase's job. The instrument guide teaches *how* to make the calls; implementation applies that to every event.

4. **Cover all three calls.** Every instrumentation guide must cover identify(), group(), and track(). These are the three universal calls. An incomplete guide will produce an incomplete implementation.

5. **Cover group-level attribution.** B2B products need events attributed to different group levels. Explain how this SDK handles it, with template code.

6. **Call out SDK constraints explicitly.** If the SDK has limitations (Accoil: no event properties; Forge: no direct HTTP from frontend), state them clearly. The implementation engineer needs to know what they cannot do.

7. **Acknowledge coverage gaps.** The reference files cover common implementations (Node.js, browser, direct API). If the user's environment isn't covered, flag it and ask whether they can provide documentation or confirm the patterns apply.

8. **Review before rewriting.** If instrument.md already exists (from audit or a previous run), read it first. Preserve correct patterns, fix incorrect ones, and note what changed.

9. **Forge requires two references.** If the target is Forge, read both forge-platform.md and the destination SDK reference. The guide must cover Forge's architecture AND the destination's API endpoints.

10. **Write to file, summarize in conversation.** Write the full guide to `.telemetry/instrument.md`. Show only a concise summary in conversation: target SDK, key patterns, constraints, coverage gaps, and what changed from current (if applicable). Never paste more than 20 lines into the chat.

11. **Present decisions, not deliberation.** Reason silently. The user should see what you produced and why — not the process of figuring it out.
