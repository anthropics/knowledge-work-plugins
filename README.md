# Knowledge Work Plugins — Legal

Legal productivity plugin for Claude, available in English and Czech. Built for [Claude Cowork](https://claude.com/product/cowork), also compatible with [Claude Code](https://claude.com/product/claude-code).

## Available Plugins

| Plugin | Language | How it helps |
|--------|----------|--------------|
| **[legal-en](./legal/en)** | English | Review contracts, triage NDAs, navigate compliance, assess risk, prep for meetings, and draft templated responses. |
| **[legal-cs](./legal/cs)** | Čeština | Revize smluv, triage NDA, compliance (GDPR, NIS2, DORA), posouzení rizika, příprava jednání a šablonové odpovědi. Napojeno na **DirectCase MCP** (`https://mcp.directcase.ai/mcp`) — cca 1,4 M ověřených českých a EU právních zdrojů. |

### DirectCase MCP — co umí

MCP server [`https://mcp.directcase.ai/mcp`](https://mcp.directcase.ai/mcp) nabízí (více na [blog.directcase.ai/cs](https://blog.directcase.ai/cs/)):

> ⚠️ **Pozor — URL změna od 1. 5. 2026:** Aktuální endpoint `https://mcp.directcase.ai/mcp` obsahuje **pouze české právní zdroje**. Od **1. 5. 2026** bude tento endpoint nahrazen lokalizovanými endpointy pro jednotlivé země ve tvaru `https://mcp.directcase.ai/{country}/mcp` (např. `https://mcp.directcase.ai/cs/mcp` pro ČR, `https://mcp.directcase.ai/sk/mcp` pro SR, atd.). Po tomto datu aktualizujte `.mcp.json` ve vašem pluginu. Do 1. 5. 2026 zůstává `/mcp` funkční jako český zdroj.

| Nástroj | Použití |
|---------|---------|
| `search_caselaw_parallel` | Paralelní vyhledávání v judikatuře (NS, ÚS, NSS, vrchní a krajské soudy) |
| `search_law_parallel` | Paralelní vyhledávání v zákonech a právních předpisech ČR |
| `search_regulatory_parallel` | Paralelní vyhledávání v regulatorních dokumentech (ČNB, ÚOOÚ, ÚOHS a další) |
| `search_keyword` | Klíčové vyhledávání napříč celou databází |
| `search_identifier` | Vyhledávání podle identifikátoru (ECLI, Sb., č.j.) |
| `search_similar` | Najít podobné dokumenty k zadanému |
| `search_company` | Vyhledat společnost v obchodním rejstříku |
| `search_company_documents` | Vyhledat dokumenty spojené s konkrétní společností |
| `get_document` | Načíst plný text dokumentu |
| `get_law_detail` | Detail konkrétního ustanovení zákona |
| `get_company_document_pdf` | Stáhnout PDF dokumentu společnosti |
| `convert_pdf_to_text` | Převést PDF na text |

## Installation

### Cowork

Install plugins from [claude.com/plugins](https://claude.com/plugins/).

### Claude Code

```bash
# Add the marketplace first
claude plugin marketplace add directcase/knowledge-work-plugins

# Then install a plugin
claude plugin install legal-en@knowledge-work-plugins
# or
claude plugin install legal-cs@knowledge-work-plugins
```

Once installed, plugins activate automatically. Skills fire when relevant, and slash commands are available in your session (e.g., `/legal-en:review-contract`, `/legal-cs:review-contract`).

## Structure

```
.
├── .claude-plugin/marketplace.json
├── legal/
│   ├── en/                          # English plugin
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── README.md
│   │   ├── CONNECTORS.md
│   │   └── skills/
│   │       ├── review-contract/SKILL.md
│   │       ├── triage-nda/SKILL.md
│   │       ├── compliance-check/SKILL.md
│   │       ├── legal-response/SKILL.md
│   │       ├── legal-risk-assessment/SKILL.md
│   │       ├── meeting-briefing/SKILL.md
│   │       ├── brief/SKILL.md
│   │       ├── vendor-check/SKILL.md
│   │       └── signature-request/SKILL.md
│   └── cs/                          # Czech plugin
│       ├── .claude-plugin/plugin.json
│       ├── .mcp.json                # includes DirectCase MCP
│       ├── README.md
│       ├── CONNECTORS.md
│       └── skills/
│           ├── revize-smlouvy/SKILL.md
│           ├── triage-nda/SKILL.md
│           ├── kontrola-souladu/SKILL.md
│           ├── pravni-odpoved/SKILL.md
│           ├── posouzeni-pravniho-rizika/SKILL.md
│           ├── priprava-jednani/SKILL.md
│           ├── prehled-pravni/SKILL.md
│           ├── kontrola-dodavatele/SKILL.md
│           └── zadost-o-podpis/SKILL.md
└── README.md
```

## How Plugins Work

- **Skills** encode domain expertise, best practices, and workflows Claude draws on automatically when relevant.
- **Commands** are explicit actions you trigger (e.g., `/legal-cs:review-contract`).
- **Connectors** wire Claude to external tools via [MCP servers](https://modelcontextprotocol.io/). The Czech plugin includes [DirectCase](https://mcp.directcase.ai/mcp) — ~1.4M Czech legal sources (case law, legislation, regulation).

Every component is file-based — markdown and JSON, no code, no infrastructure, no build steps.

## Customization

- **Swap connectors** — edit `.mcp.json` to point at your specific tool stack.
- **Add company context** — drop terminology, org structure, and processes into skill files.
- **Adjust workflows** — modify skill instructions to match how your team actually does things.

## Contributing

Plugins are just markdown files. Fork the repo, make your changes, and submit a PR.
