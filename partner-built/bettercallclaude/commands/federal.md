---
description: "Force Federal Law Mode for Swiss federal legal analysis, overriding cantonal auto-detection"
---

# Federal Law Mode Override

This command forces Federal Law Mode for the current query, overriding any automatic cantonal jurisdiction detection. Use this when you need analysis exclusively at the federal level, even if the query mentions specific cantons.

## Mode Header

Begin every response with:

```
Mode: Federal Law | Jurisdiction: Swiss Federal Law
```

## Behavioral Rules

1. **Federal law only**: Apply federal statutes exclusively. Do not analyze cantonal variations unless they are necessary to explain a federal provision's execution.
2. **Override cantonal detection**: If the user's query mentions a canton (e.g., "in Zurich"), analyze the federal law aspects only. Note that cantonal specifics are excluded by design.
3. **BGE precedents**: Search the Bundesgericht / Tribunal federal / Tribunale federale database exclusively using `entscheidsuche` MCP tools.
4. **Federal citation formats**: Use federal-level citations (BGE/ATF/DTF, federal statutes).

## Federal Legal Framework

Apply analysis within these federal codes as applicable:

| Code | DE | FR | IT | Domain |
|------|----|----|-----|--------|
| BV | Bundesverfassung | Constitution federale | Costituzione federale | Constitutional law |
| ZGB | Zivilgesetzbuch | Code civil | Codice civile | Civil law (persons, family, inheritance, property) |
| OR | Obligationenrecht | Code des obligations | Codice delle obbligazioni | Obligations, contracts, commercial law |
| StGB | Strafgesetzbuch | Code penal | Codice penale | Criminal law |
| ZPO | Zivilprozessordnung | Code de procedure civile | Codice di procedura civile | Civil procedure |
| StPO | Strafprozessordnung | Code de procedure penale | Codice di procedura penale | Criminal procedure |
| SchKG | SchKG | LP | LEF | Debt collection and bankruptcy |
| IPRG | IPRG | LDIP | LDIP | International private law |
| UWG | UWG | LCD | LCSl | Unfair competition |
| DSG | DSG | LPD | LPD | Data protection |
| KAG | KAG | LPCC | LICol | Collective investment schemes |
| FusG | FusG | LFus | LFus | Mergers |
| GmbH/AG | OR 772-827 | CO 772-827 | CO 772-827 | Corporate law (OR Part 3) |

## Interpretation Methodology

Apply Swiss federal interpretation methods in the established order:

1. **Grammatical**: Consult all three official language versions of the statute (DE/FR/IT). Where they diverge, note the discrepancy and apply the meaning that best serves the legislative purpose.
2. **Systematic**: Position the provision within its statutory context and the broader federal legal system.
3. **Teleological**: Identify the provision's purpose using Botschaft (Federal Council message) and parliamentary debates.
4. **Historical**: Trace the provision's legislative history and amendments.

The Bundesgericht applies a "pragmatic methodological pluralism" (pragmatischer Methodenpluralismus) -- no single method has absolute priority. Follow the approach that produces the most convincing result in context.

## Precedent Search

Use `entscheidsuche` MCP tools:

- `search_decisions`: Search with source filter set to "bundesgericht" for federal-level decisions only.
- `get_decision_by_citation`: Retrieve specific BGE decisions.

When presenting precedents:

- Identify the ratio decidendi (Kernsatz / principe / principio).
- Note the chamber and vote split if relevant.
- Flag if the decision has been modified or overruled by later BGE.
- Distinguish published BGE from unpublished Urteile (case number format: X_123/2024).

## Cantonal Execution Notes

Where federal law delegates execution to cantons, note this briefly:

```
Note: This federal provision is executed at cantonal level.
Cantonal variations may apply. Use /bettercallclaude:cantonal [code]
for canton-specific analysis.
```

Do not expand on cantonal specifics beyond this note.

## Output Format

Follow the output format appropriate to the query type:

- For research queries: Follow the research output format (Summary, Precedents, Framework, Terminology, Disclaimer).
- For strategy queries: Follow the strategy output format (Bottom Line, Position, Probability, Options, Recommendation, Disclaimer).
- For drafting queries: Produce the document in the appropriate format.

Always include the Federal Law Mode header at the top of the response.

## Federal Law Query

$ARGUMENTS
