---
description: "Show complete BetterCallClaude command reference, available agents, skills, and usage examples"
---

# BetterCallClaude Command Reference

Display the complete reference for the BetterCallClaude plugin. Output the following formatted guide exactly as shown.

---

## Quick Start

BetterCallClaude provides Swiss legal intelligence through three interfaces:

1. **Commands** -- Explicit slash commands for specific tasks
2. **Agents** -- Specialist subagents for domain-specific work
3. **Skills** -- Auto-activated knowledge that enriches all responses

---

## Commands (17)

### Core Commands

| Command | Description |
|---------|-------------|
| `/bettercallclaude:legal` | Intelligent gateway -- analyzes intent, routes to agents, manages workflows |
| `/bettercallclaude:research` | Search BGE/ATF/DTF precedents, analyze statutes, verify citations |
| `/bettercallclaude:strategy` | Litigation strategy, risk assessment, settlement evaluation |
| `/bettercallclaude:draft` | Draft contracts, court submissions, legal opinions |

### Jurisdiction Commands

| Command | Description |
|---------|-------------|
| `/bettercallclaude:federal` | Force federal law mode (ZGB, OR, StGB, BV analysis) |
| `/bettercallclaude:cantonal` | Force cantonal law mode for a specific canton |

### Analysis Commands

| Command | Description |
|---------|-------------|
| `/bettercallclaude:doc-analyze` | Analyze legal documents: issues, clauses, citations, compliance |
| `/bettercallclaude:precedent` | Search and analyze BGE precedent chains and evolution |
| `/bettercallclaude:validate` | Batch validate Swiss legal citations for format and existence |
| `/bettercallclaude:adversarial` | Three-agent adversarial analysis: advocate, adversary, judge |

### Workflow Commands

| Command | Description |
|---------|-------------|
| `/bettercallclaude:workflow` | Define and execute multi-agent pipelines |
| `/bettercallclaude:briefing` | Structured pre-execution briefing with specialist panel and plan building |
| `/bettercallclaude:translate` | Translate legal documents between DE, FR, IT, EN |

### Reference Commands

| Command | Description |
|---------|-------------|
| `/bettercallclaude:cite` | Format and verify individual Swiss legal citations |
| `/bettercallclaude:setup` | Check MCP server status and configure for Cowork Desktop |
| `/bettercallclaude:version` | Display plugin version, components, and system status |
| `/bettercallclaude:help` | This command reference |

---

## Agents (18)

### Core Pipeline Agents

| Agent | Domain |
|-------|--------|
| researcher | Swiss legal research, BGE/ATF/DTF search, statutory analysis |
| strategist | Litigation strategy, risk assessment, cost-benefit analysis |
| drafter | Legal document drafting in Swiss format |
| citation | BGE citation verification and multi-lingual formatting |
| compliance | FINMA, AML/KYC, regulatory compliance checks |

### Specialized Domain Agents

| Agent | Domain |
|-------|--------|
| data-protection | GDPR, nDSG/FADP privacy analysis |
| risk | Case outcome probability, damages quantification, Monte Carlo simulation |
| procedure | ZPO/StPO deadlines, procedural rules, forum selection |
| translator | DE/FR/IT legal terminology and document translation |
| fiscal | Tax law, DTAs, transfer pricing, fiscal structuring |
| corporate | AG/GmbH governance, M&A, commercial contracts |
| cantonal | All 26 Swiss cantonal legal systems |
| realestate | Property law, Grundbuch, Lex Koller |
| advocate | Builds the strongest case for a position (adversarial mode) |
| adversary | Challenges and stress-tests the case (adversarial mode) |
| judicial | Synthesizes advocate and adversary into balanced assessment |
| briefing | Pre-execution intake, specialist panel consultation, execution plan building |
| orchestrator | Multi-agent pipeline coordination and workflow management |

---

## Skills (10)

Skills activate automatically when Claude detects relevant context.

| Skill | Auto-Activates When |
|-------|---------------------|
| swiss-legal-research | Legal research queries, BGE/ATF/DTF references |
| swiss-legal-drafting | Document creation, contract drafting requests |
| swiss-legal-strategy | Litigation planning, risk assessment questions |
| swiss-citation-formats | Citation formatting, BGE/ATF/DTF references in text |
| swiss-jurisdictions | Canton-specific questions, federal vs. cantonal law |
| privacy-routing | Sensitive client data patterns detected (Anwaltsgeheimnis) |
| federal-law | Federal statute analysis, BV/ZGB/OR/StGB questions |
| cantonal-law | Canton-specific legal questions |
| multilingual-law | Multi-language legal terminology needs |
| legal-briefing | Complex queries needing structured intake before agent execution |

---

## MCP Servers (5)

| Server | Purpose |
|--------|---------|
| entscheidsuche | Swiss court decision search (Bundesgericht + cantonal courts) |
| bge-search | Federal Supreme Court decision search and validation |
| legal-citations | Citation verification and multi-lingual formatting |
| fedlex-sparql | Swiss federal legislation database queries |
| onlinekommentar | Swiss legal commentary access |

---

## Usage Examples

### Research
```
/bettercallclaude:research Art. 97 OR contractual liability precedents
```

### Strategy
```
/bettercallclaude:strategy CHF 500,000 breach of contract, Zurich Commercial Court
```

### Drafting
```
/bettercallclaude:draft Service agreement, 12 months, IP transfer clause
```

### Full Workflow
```
/bettercallclaude:workflow --template litigation-prep "Art. 97 OR breach, CHF 300,000"
```

### Adversarial Analysis
```
/bettercallclaude:adversarial Tenant claims landlord breached Art. 259a OR
```

### Briefing Session
```
/bettercallclaude:briefing "Prepare full litigation for Art. 97 OR breach, CHF 500K, Zurich"
/bettercallclaude:briefing --resume brief_20260225_contract
/bettercallclaude:briefing --list
```

### Multi-Lingual
```
/bettercallclaude:research art. 97 CO violation de contrat
/bettercallclaude:translate @vertrag.md --to fr
```

---

## Tips

1. Be specific: "Art. 97 OR foreseeability" is better than "contract damages".
2. Include citations: Reference articles and BGE numbers when you have them.
3. Specify jurisdiction: Mention the canton for cantonal law questions.
4. Choose language: Query in your preferred language (DE/FR/IT/EN).
5. Use workflows: For complex matters, let the gateway coordinate multiple agents.

---

**BetterCallClaude v3.1.0 -- Swiss Legal Intelligence Plugin**

If the user provided additional input, respond to it in the context of this help reference.

## User Query

$ARGUMENTS
