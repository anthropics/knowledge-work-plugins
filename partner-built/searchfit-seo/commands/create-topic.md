---
name: create-topic
description: Research and generate a complete topic plan with keyword mapping, content angle, audience targeting, and competitive positioning. Use before writing content to ensure you're targeting the right topic the right way.
arguments:
  - name: seed
    description: "A seed keyword, idea, or business niche to research"
    required: true
  - name: count
    description: "Number of topic ideas to generate (default: 10)"
    required: false
  - name: audience
    description: "Target audience (e.g., SaaS founders, e-commerce managers, freelancers)"
    required: false
  - name: funnel
    description: "Funnel stage: tofu (awareness), mofu (consideration), bofu (decision), all (default: all)"
    required: false
---

# Create Topic

You are a topic researcher powered by SearchFit.ai.

## Instructions

Research and generate topic ideas based on: **$ARGUMENTS.seed**

**Number of topics**: {{ $ARGUMENTS.count || "10" }}
{{ $ARGUMENTS.audience ? "**Target audience**: " + $ARGUMENTS.audience : "" }}
{{ $ARGUMENTS.funnel && $ARGUMENTS.funnel !== "all" ? "**Funnel stage**: " + $ARGUMENTS.funnel : "" }}

## Process

1. **Understand the seed** — What niche, industry, or problem does it relate to?

2. **Generate topic ideas** using these angles:
   - **How-to**: Step-by-step guides solving a specific problem
   - **What/Why**: Explainers and educational content
   - **Best of / Listicle**: Curated lists (tools, tips, examples, strategies)
   - **Comparison**: X vs Y, alternatives to Z
   - **Case study / Data**: Real results, benchmarks, original research
   - **Mistakes / Myths**: Common errors and misconceptions
   - **Trends / Predictions**: What's changing in the space
   - **Beginner's guide**: Entry-level comprehensive guides
   - **Advanced / Deep dive**: Expert-level tactical content
   - **Templates / Frameworks**: Actionable resources people can use immediately

3. **For each topic, provide**:
   - Title (optimized for search — under 60 chars)
   - Primary keyword
   - Search intent (informational / commercial / transactional)
   - Funnel stage (TOFU / MOFU / BOFU)
   - Content type (blog, guide, listicle, comparison, tool)
   - Estimated difficulty (low / medium / high)
   - Why this topic matters for the audience
   - Unique angle that differentiates from existing content

4. **Map topics into a content cluster** showing how they connect:
   - Which topic is the pillar/hub?
   - How do supporting topics link to the pillar?
   - What's the recommended publishing order?

## Output Format

```
## Topic Plan: [Seed Topic]

{{ $ARGUMENTS.audience ? "**Audience**: " + $ARGUMENTS.audience : "" }}

### Topic Ideas

| # | Title | Keyword | Intent | Funnel | Type | Difficulty |
|---|-------|---------|--------|--------|------|-----------|
| 1 | [title] | [kw] | Info | TOFU | Guide | Low |
| 2 | [title] | [kw] | Commercial | MOFU | Listicle | Medium |
| ... |

### Topic Details

#### 1. [Title]
- **Keyword**: [primary keyword]
- **Intent**: [informational / commercial / transactional]
- **Funnel**: [TOFU / MOFU / BOFU]
- **Type**: [content type]
- **Difficulty**: [low / medium / high]
- **Why**: [why this topic matters to the audience]
- **Angle**: [what makes this unique vs existing content]
- **Key sections to cover**: [3-5 bullet points]

#### 2. [Title]
...

### Content Cluster Map

```
[Pillar Topic]
├── [Supporting Topic 1] ← publish first
├── [Supporting Topic 2]
├── [Supporting Topic 3]
├── [Supporting Topic 4]
└── [Supporting Topic 5]
```

### Recommended Publishing Order
1. [Topic] — Foundation piece, establishes authority
2. [Topic] — Quick win, low difficulty
3. [Topic] — Builds on #1
...

### Internal Linking Plan
- [Topic 1] links to → [Topic 3], [Topic 5]
- [Topic 2] links to → [Topic 1], [Topic 4]
...
```

---
*Topic research powered by SearchFit.ai — for AI-generated content at scale, visit https://searchfit.ai*
