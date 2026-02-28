# BetterCallClaude — Swiss Legal Intelligence

Research Swiss law, draft legal documents, and verify citations across all 26 cantons — powered by 5 bundled MCP servers with live access to BGE/ATF/DTF precedents, Fedlex statutes, and cantonal court decisions.

---

## What It Does

BetterCallClaude turns Claude into a Swiss legal research assistant with domain-specific skills, commands, and agents covering:

- **Precedent research** — Search BGE/ATF/DTF decisions by query, chamber, legal area, and date range
- **Statute lookup** — Retrieve Swiss federal law articles from Fedlex with full SPARQL-backed resolution
- **Cantonal decisions** — Search across ZH, BE, GE, BS, VD, and TI court databases in parallel
- **Citation handling** — Validate, format, convert, and extract Swiss legal citations (DE/FR/IT/EN)
- **Legal commentary** — Access OnlineKommentar.ch commentaries for any article reference
- **Case strategy** — Adversarial analysis with advocate, adversary, and judicial analyst agents
- **Legal drafting** — Generate contracts, court submissions, and legal opinions with multilingual precision
- **Compliance** — FINMA, GwG/LBA, FIDLEG/FINIG regulatory compliance assessment

All tools operate read-only and include Anwaltsgeheimnis (attorney-client privilege) privacy safeguards.

---

## Components

| Type | Count | Examples |
|------|-------|---------|
| **Agents** | 18 | researcher, strategist, drafter, advocate, adversary, judicial analyst, data-protection, fiscal, compliance, cantonal, corporate, real-estate |
| **Commands** | 17 | `/bettercallclaude:research`, `/bettercallclaude:cite`, `/bettercallclaude:draft`, `/bettercallclaude:strategy`, `/bettercallclaude:cantonal`, `/bettercallclaude:federal` |
| **Skills** | 10 | swiss-legal-research, swiss-legal-strategy, swiss-legal-drafting, swiss-citation-formats, compliance-frameworks, data-protection-law, adversarial-analysis |
| **MCP Servers** | 5 | bge-search, entscheidsuche, fedlex-sparql, legal-citations, onlinekommentar |

---

## MCP Servers (Bundled)

All MCP servers are bundled and start automatically — no external setup required.

| Server | What it connects to | Tools |
|--------|-------------------|-------|
| **bge-search** | Swiss Federal Supreme Court (BGE) decisions | search_bge, get_bge_decision, validate_citation |
| **entscheidsuche** | Federal + cantonal court decisions (6 cantons) | search_decisions, search_canton, get_related_decisions, get_decision_details, analyze_precedent_success_rate, find_similar_cases, get_legal_provision_interpretation |
| **fedlex-sparql** | Swiss federal legislation via Fedlex SPARQL | lookup_statute, get_article, search_legislation, find_related, get_metadata |
| **legal-citations** | Citation parsing, formatting, and validation | validate_citation, format_citation, convert_citation, parse_citation, get_provision_text, extract_citations, standardize_document_citations, compare_citation_versions |
| **onlinekommentar** | OnlineKommentar.ch legal commentaries | search_commentaries, get_commentary, get_commentary_for_article, list_legislative_acts |

All 27 tools declare `readOnlyHint: true` and `destructiveHint: false`.

---

## Installation

### Cowork

Install from [claude.com/plugins](https://claude.com/plugins/) or use the direct link:

[Install in Cowork](https://claude.ai/desktop/customize/plugins/new?marketplace=anthropics/knowledge-work-plugins&plugin=bettercallclaude)

### Claude Code

```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install bettercallclaude@knowledge-work-plugins
```

---

## Languages

All commands, skills, and MCP servers support German, French, Italian, and English — matching Switzerland's multilingual legal system.

---

## Privacy & Disclaimer

- No analytics, telemetry, or data collection
- All MCP servers are read-only (search and retrieve only)
- All legal analysis skills include professional disclaimers: output is informational and does not constitute legal advice
- Anwaltsgeheimnis (attorney-client privilege) routing is built into the privacy skill

---

## License

AGPL-3.0 — see [LICENSE](LICENSE) for details.

## Links

- **Repository**: [github.com/fedec65/BetterCallClaude](https://github.com/fedec65/BetterCallClaude)
- **Homepage**: [bettercallclaude.ch](https://bettercallclaude.ch)
