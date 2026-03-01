---
name: biosciences-pharmacology
description: "Queries pharmacology databases (ChEMBL, PubChem, DrugBank, IUPHAR, Open Targets) via MCP tools for drug mechanisms, target identification, bioactivity profiling, and indication discovery. Falls back to curl when MCP is unavailable. This skill should be used when the user asks to \"find drug mechanisms\", \"identify drug targets\", \"analyze bioactivity data\", \"discover drug indications\", or mentions ChEMBL IDs, mechanisms of action, IC50/Ki values, drug-target relationships, or compound similarity searches."
---

# Biosciences Pharmacology API Skills

Query pharmacology databases via MCP tools (primary) or curl (fallback).

## Grounding Rule

All drug names, mechanisms, targets, and bioactivity values MUST come from API results. Do NOT provide drug information from training knowledge. If a query returns no results, report "No results found."

## MCP Token Budgeting (`slim` Parameter)

All MCP tools support `slim=true` for token-efficient LOCATE queries (~20 tokens/entity vs ~115-300). Use `slim=false` (default) for RETRIEVE with full metadata. See [token-budgeting.md](../../references/token-budgeting.md) for details.

## LOCATE → RETRIEVE Patterns

### ChEMBL: Compound Search & Details

**LOCATE**: Search compound by name

PRIMARY (MCP tool):
```
Call `chembl_search_compounds` with: {"query": "venetoclax"}
→ Claude Code name: mcp__biosciences-mcp__chembl_search_compounds
→ Returns: ChEMBL IDs, preferred names, max phase
```

FALLBACK (curl):
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule/search?q=venetoclax&format=json" \
  | jq '.molecules[:1][] | {chembl_id: .molecule_chembl_id, name: .pref_name, max_phase: .max_phase}'
```

**RETRIEVE**: Get compound by ChEMBL ID

PRIMARY (MCP tool):
```
Call `chembl_get_compound` with: {"chembl_id": "CHEMBL3137309"}
→ Claude Code name: mcp__biosciences-mcp__chembl_get_compound
→ May return 500 error (common for detail endpoints) — fall back to Open Targets
```

FALLBACK (curl):
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL3137309?format=json" \
  | jq '{id: .molecule_chembl_id, name: .pref_name, formula: .molecule_properties.full_molformula, mw: .molecule_properties.full_mwt}'
```

### Open Targets: Drug Discovery (PRIMARY — More Reliable Than ChEMBL)

**LOCATE**: Find drugs targeting a protein

PRIMARY (MCP tool):
```
Call `opentargets_get_target` with: {"ensembl_id": "ENSG00000171791"}
→ Claude Code name: mcp__biosciences-mcp__opentargets_get_target
→ Returns: knownDrugs with drug name, mechanismOfAction, phase in one call
```

FALLBACK (curl):
```bash
curl -s -X POST "https://api.platform.opentargets.org/api/v4/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ target(ensemblId: \"ENSG00000171791\") { knownDrugs(size: 25) { rows { drug { name id } mechanismOfAction phase } } } }"}'
```

**Open Targets `knownDrugs` Pagination**:
- Use `size` parameter only (e.g., `size: 25`) — this is the reliable pattern
- Do NOT use `page` or `index` — these cause intermittent failures
- For paginated results, use `cursor` (returned in the response) as the continuation token
- If first query fails, retry with `size` only (no other pagination params)

**Note**: Requires Ensembl Gene ID (ENSG...). Get this from HGNC cross-references or Ensembl lookup.

### ChEMBL: Drug Mechanisms (Critical for Graph Edges) — curl only

**RETRIEVE**: Get mechanism for drug (Drug → Target edge)
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL3137309&format=json" \
  | jq '.mechanisms[] | {action: .action_type, mechanism: .mechanism_of_action, target_id: .target_chembl_id}'
```

**RETRIEVE**: Find all drugs for target (Target → Drugs edge)
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?target_chembl_id=CHEMBL4860&format=json" \
  | jq '.mechanisms[] | {drug_id: .molecule_chembl_id, action: .action_type, mechanism: .mechanism_of_action}'
```

### ChEMBL: Drug Indications — curl only

**RETRIEVE**: Get indications for drug (Drug → Disease edge)
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/drug_indication?molecule_chembl_id=CHEMBL3137309&format=json" \
  | jq '.drug_indications[:5][] | {disease: .mesh_heading, efo: .efo_term, phase: .max_phase_for_ind}'
```

### ChEMBL: Bioactivity Data (Potency Metrics) — curl only

**RETRIEVE**: Get activity data (IC50, Ki, EC50)
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/activity?molecule_chembl_id=CHEMBL3137309&format=json&limit=10" \
  | jq '.activities[] | {target: .target_pref_name, type: .standard_type, value: .standard_value, units: .standard_units}'
```

### ChEMBL: Structure Search — curl only

```bash
# Similarity search (find analogs)
SMILES="CC1=CC=CC=C1"  # Example SMILES
curl -s "https://www.ebi.ac.uk/chembl/api/data/similarity/$SMILES/70?format=json" \
  | jq '.molecules[:3][] | {id: .molecule_chembl_id, name: .pref_name, similarity: .similarity}'

# Substructure search
curl -s "https://www.ebi.ac.uk/chembl/api/data/substructure/$SMILES?format=json&limit=5" \
  | jq '.molecules[] | {id: .molecule_chembl_id, name: .pref_name}'
```

### ChEMBL: Target Information — curl only

```bash
# Get target details
curl -s "https://www.ebi.ac.uk/chembl/api/data/target/CHEMBL4860?format=json" \
  | jq '{id: .target_chembl_id, name: .pref_name, type: .target_type, organism: .organism}'

# Search targets by gene
curl -s "https://www.ebi.ac.uk/chembl/api/data/target/search?q=BCL2&format=json" \
  | jq '.targets[:3][] | {id: .target_chembl_id, name: .pref_name, type: .target_type}'
```

### PubChem: Compound Data

**LOCATE**: Get compound by name

PRIMARY (MCP tool):
```
Call `pubchem_search_compounds` with: {"query": "aspirin"}
→ Claude Code name: mcp__biosciences-mcp__pubchem_search_compounds
→ Returns: CID, molecular formula, properties
```

FALLBACK (curl):
```bash
curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/JSON" \
  | jq '.PC_Compounds[0] | {cid: .id.id.cid}'
```

**RETRIEVE**: Get properties by CID

PRIMARY (MCP tool):
```
Call `pubchem_get_compound` with: {"cid": "2244"}
→ Claude Code name: mcp__biosciences-mcp__pubchem_get_compound
→ Returns: molecular formula, weight, IUPAC name
```

FALLBACK (curl):
```bash
curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularFormula,MolecularWeight,IUPACName/JSON" \
  | jq '.PropertyTable.Properties[0]'
```

### IUPHAR/GtoPdb: Pharmacology

**LOCATE**: Search ligands

PRIMARY (MCP tool):
```
Call `iuphar_search_ligands` with: {"query": "ibuprofen"}
→ Claude Code name: mcp__biosciences-mcp__iuphar_search_ligands
→ Returns: ligand ID, name, type, approved status
```

FALLBACK (curl):
```bash
curl -s "https://www.guidetopharmacology.org/services/ligands?name=ibuprofen" \
  | jq '.[:1][] | {id: .ligandId, name, type, approved}'
```

**RETRIEVE**: Get ligand-target interactions

PRIMARY (MCP tool):
```
Call `iuphar_get_ligand` with: {"ligand_id": "2713"}
→ Claude Code name: mcp__biosciences-mcp__iuphar_get_ligand
→ Returns: target interactions, action types, affinities
```

FALLBACK (curl):
```bash
curl -s "https://www.guidetopharmacology.org/services/ligands/2713/interactions" \
  | jq '.[:3][] | {target: .targetName, action: .action, affinity}'
```

### DrugBank: Drug Data (API Key Required) — curl only

```bash
# Search drugs (commercial API)
curl -s "https://api.drugbank.com/v1/drugs?q=venetoclax" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  | jq '.[:1][] | {drugbank_id, name, description}'
```

## Drug Repurposing Workflow (LOCATE → RETRIEVE Chain)

```bash
# Step 1: LOCATE — Find target for known drug (curl — mechanism endpoint)
TARGET=$(curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL3137309&format=json" \
  | jq -r '.mechanisms[0].target_chembl_id')

# Step 2: RETRIEVE — Find other drugs for same target
curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?target_chembl_id=$TARGET&format=json" \
  | jq '.mechanisms[] | {drug: .molecule_chembl_id, mechanism: .mechanism_of_action}'

# Step 3: RETRIEVE — Get indications for alternative drug
curl -s "https://www.ebi.ac.uk/chembl/api/data/drug_indication?molecule_chembl_id=CHEMBL2107358&format=json" \
  | jq '.drug_indications[:3][] | {disease: .mesh_heading, phase: .max_phase_for_ind}'
```

## Quick Reference

| Task | Pattern | MCP Tool (primary) | Curl Endpoint (fallback) |
|------|---------|-------------------|--------------------------|
| Search compounds | LOCATE | `chembl_search_compounds` | ChEMBL `/molecule/search` |
| Get compound | RETRIEVE | `chembl_get_compound` | ChEMBL `/molecule/{id}` |
| Drug mechanism | RETRIEVE | (curl only) | ChEMBL `/mechanism` |
| Drug indications | RETRIEVE | (curl only) | ChEMBL `/drug_indication` |
| Bioactivity data | RETRIEVE | (curl only) | ChEMBL `/activity` |
| Find drugs for target | LOCATE | `opentargets_get_target` | Open Targets GraphQL `knownDrugs` |
| Compound by name | LOCATE | `pubchem_search_compounds` | PubChem `/compound/name/{name}` |
| Ligand interactions | RETRIEVE | `iuphar_get_ligand` | IUPHAR `/ligands/{id}/interactions` |
| DrugBank search | LOCATE | (curl only) | DrugBank `/v1/drugs` |

## ID Format Reference

| Database | API Argument (bare) | Graph CURIE | Example |
|----------|---------------------|-------------|---------|
| ChEMBL compound | `CHEMBL3137309` | `CHEMBL:3137309` | Bare for API (no colon) |
| ChEMBL target | `CHEMBL4860` | `CHEMBL:4860` | Same pattern |
| PubChem | `2244` (CID) | `PubChem:2244` | Bare numeric for API |

## API Reliability & Fallback Patterns

| Primary | Fallback | When to Switch |
|---------|----------|----------------|
| ChEMBL `chembl_get_compound` (detail) | Open Targets `opentargets_get_target` | On HTTP 500 (common for detail endpoints) |
| ChEMBL `chembl_search_compounds` (search) | (generally reliable — uses Elasticsearch) | Retry once, then report failure |
| ChEMBL `/mechanism` | Open Targets `mechanismOfAction` field | On HTTP 500 |

**Critical**: ChEMBL **detail endpoints** (`/molecule/{id}`) frequently return 500 errors (EBI server issues). ChEMBL **search endpoints** (`/molecule/search?q=...`) are generally reliable because they use Elasticsearch. When detail fails, use Open Targets as primary drug discovery source.

## Rate Limits

| API | Limit | Auth Required | Production Throttle |
|-----|-------|---------------|---------------------|
| ChEMBL | ~2 req/s | No | 0.5s delay in production |
| PubChem | 5 req/s | No | — |
| IUPHAR | 10 req/s | No | — |
| DrugBank | Varies | Yes (commercial) | — |

## Query Best Practices

### Drug Discovery vs Repurposing
- **Drug repurposing**: Use `max_phase >= 2` filter (want clinical validation, shorter approval path)
- **General discovery**: No phase filter (include preclinical tools, mechanism probes, research reagents)
- **Target validation**: No phase filter needed for mechanism studies

### Gain-of-Function Disease Filter
For diseases caused by protein overactivation (e.g., FOP from constitutive ACVR1):
- INCLUDE: inhibitors, antagonists, negative modulators
- EXCLUDE: agonists, positive modulators, activators
- Check `mechanismOfAction` field from Open Targets or `action_type` from ChEMBL

### Query Efficiency
- Check mechanisms (`/mechanism` endpoint) before bioactivity data
- Use `target_chembl_id` for reverse lookups (find drugs for target)
- Limit activity queries with `&limit=10` for exploration

## See Also

- **biosciences-graph-builder**: Orchestrator for full Fuzzy-to-Fact protocol
- **biosciences-clinical**: Open Targets, ClinicalTrials.gov clinical endpoints
