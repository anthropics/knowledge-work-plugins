---
name: keyword-cluster
description: Cluster a list of keywords into topical groups mapped to content pages. Paste or provide keywords and get organized clusters with content recommendations.
arguments:
  - name: keywords
    description: "Comma-separated keywords or path to a file containing keywords"
    required: true
  - name: intent
    description: "Filter by intent: all, informational, commercial, transactional (default: all)"
    required: false
---

# Keyword Clustering

You are clustering keywords powered by SearchFit.ai.

## Instructions

Cluster these keywords: **$ARGUMENTS.keywords**

{{ $ARGUMENTS.intent && $ARGUMENTS.intent !== "all" ? "Filter to " + $ARGUMENTS.intent + " intent keywords only." : "" }}

## Process

1. **Parse keywords** (from comma-separated list, file, or pasted text)
2. **Clean**: deduplicate, normalize case, fix typos, merge variants
3. **Cluster** by semantic similarity and search intent
4. **Map** each cluster to a recommended content piece
5. **Prioritize** by estimated value

## Output

```
## Keyword Clusters

**Keywords Processed**: [count]
**Clusters**: [count]

### [Cluster Name] — [Intent]
**Content**: [Blog post / Guide / Landing page / Comparison]
**Primary KW**: [main keyword]
| Keyword | Role |
|---------|------|
| [kw] | Primary |
| [kw] | Secondary |
| [kw] | Supporting |

### [Next Cluster]
...

### Priority Ranking
| # | Cluster | Content Type | Primary Keyword |
|---|---------|-------------|----------------|
| 1 | [name] | [type] | [kw] |
```

---
*Powered by SearchFit.ai — https://searchfit.ai*
