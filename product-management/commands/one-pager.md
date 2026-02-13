---
description: Synthesize multiple inputs into a concise one-page executive summary under 500 words
argument-hint: "<topic or documents to synthesize>"
---

# One-Pager

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Distill complex information into a one-page executive summary.

## Workflow

### 1. Understand the Purpose

Ask the user:
- What is this one-pager for? (Board meeting, executive review, stakeholder alignment, project kickoff)
- Who is the audience? (C-suite, board, cross-functional leaders, investors)
- What is the core topic or initiative?
- What outcome do you want from the reader? (Decision, approval, awareness, funding)

### 2. Gather Source Material

Ask the user for the documents or data to synthesize. Accept any combination of:
- PRDs, spec documents, or project plans
- Research reports or analysis documents
- Sprint reviews or progress updates
- Metrics dashboards or data exports
- Strategy documents or OKR updates
- Meeting notes or decision records

### 3. Pull Context from Connected Tools

If **~~knowledge base** is connected:
- Search for related documents, specs, and reports
- Pull relevant meeting notes and decision records
- Find related strategy documents or OKR updates

If **~~product analytics** is connected:
- Pull key metrics related to the topic
- Search for trend data and benchmarks
- Find usage data that supports the narrative

If **~~project tracker** is connected:
- Pull status on related initiatives
- Search for milestone progress and timeline updates

If these tools are not connected, work entirely from what the user provides. Ask the user to paste or describe the source material.

### 4. Generate the One-Pager

Produce a concise executive summary. See the **executive-synthesis** skill for detailed guidance on the pyramid principle, audience adaptation, and synthesis process.

Strict constraint: **Under 500 words.** Every word must earn its place.

- **Title**: Clear and specific. "[Initiative] — [Status/Purpose]"
- **TL;DR**: 2-3 sentences capturing the full message. If the reader stops here, they should have the essential point.
- **Context**: Minimum background needed for a new reader (2-3 sentences maximum, not a full history)
- **Key Findings**: 3-5 most important data points or insights, each in one sentence. Quantify wherever possible.
- **Recommendation**: What should happen next, stated clearly and directly (1-2 sentences)
- **Next Steps**: 2-3 specific actions with owners and timelines

### 5. Follow Up

After generating the one-pager:
- Offer to create a TL;DR version for Slack using `/tldr`
- Offer to expand into a full presentation using `/stakeholder-update`
- Offer to adjust the tone for a different audience
- Offer to add an appendix with supporting data

## Output Format

Use markdown with clear headers. The document must fit on one printed page — approximately 400-500 words. Use bullet points sparingly and only when they improve scannability.

## Tips

- Start with the recommendation, not the background. Executives want your answer before your analysis.
- Every claim should be backed by a specific data point. "Significant improvement" is not useful; "40% reduction in search time" is.
- Three sentences of context maximum. Assume the reader knows the background or can ask.
- If you cannot state the TL;DR in 2-3 sentences, you have not synthesized enough. Go back and clarify the governing thought.
- Cut adverbs and qualifiers. "Very significant improvement of approximately 40%" becomes "40% improvement."
- Test the one-pager: can someone unfamiliar with the project understand the recommendation and next steps? If not, revise.
