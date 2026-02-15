"""
CQ-Eval MCP Server — Competency Question golden test set management and scoring.

Manages a catalog of competency questions (CQs) as structured JSON,
executes individual CQ steps against live MCP tools, and scores results
against gold standard paths.

Architecture context (prior-art-api-patterns.md §7.6):
  Competency questions serve dual purpose — scope definition AND benchmark validation.
  This server formalizes that into executable test infrastructure for data federation tools.

Prior art:
  - BTE-RAG (Xu et al. 2025): DrugMechDB-derived benchmarks for federated API evaluation
  - CQsBEN (Alharbi et al. 2024): Benchmark framework for CQ engineering
  - TRAPI (NCATS Translator): Standardized biomedical KG query patterns

Design principles:
  - CQs validate data federation (structured API access), not RAG over documents
  - Gold standards are mechanistic paths: Drug→Target→Gene→Disease
  - Scoring measures entity resolution accuracy, edge coverage, and path completeness
  - Catalog is versioned and extensible — start with 15 CQs, grow over time
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import json
import os
from datetime import datetime, timezone

mcp = FastMCP("cq_eval_mcp")

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

class EntityRef(BaseModel):
    """A gold-standard entity with its canonical CURIE."""
    model_config = ConfigDict(extra="forbid")
    name: str = Field(description="Human-readable entity name (e.g., 'Palovarotene')")
    curie: str = Field(description="Canonical CURIE (e.g., 'CHEMBL:2105648')")
    entity_type: str = Field(description="Entity type: drug, gene, protein, disease, variant, pathway")

class EdgeRef(BaseModel):
    """A gold-standard edge between two entities."""
    model_config = ConfigDict(extra="forbid")
    source: str = Field(description="Source entity CURIE")
    target: str = Field(description="Target entity CURIE")
    relation: str = Field(description="Relation type (e.g., 'agonist', 'regulates', 'causes')")
    evidence_tier: str = Field(
        default="tier1",
        description="Expected validation tier: tier1 (MCP tool), tier2 (curl skill), tier3 (literature)"
    )

class WorkflowStep(BaseModel):
    """A single step in the CQ validation workflow."""
    model_config = ConfigDict(extra="forbid")
    step_id: str = Field(description="Step identifier (e.g., 'anchor', 'mechanism', 'target_gene')")
    description: str = Field(description="What this step validates")
    tool_pattern: str = Field(description="Tool or curl pattern to use (e.g., 'chembl_search_compounds')")
    tier: str = Field(default="tier1", description="Architecture tier: tier1, tier2, tier3")
    expected_curie: Optional[str] = Field(default=None, description="Expected CURIE in result")

class CompetencyQuestion(BaseModel):
    """A complete competency question with gold standard path and workflow."""
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="CQ identifier (e.g., 'cq1')")
    title: str = Field(description="Short descriptive title")
    question: str = Field(description="The natural language question")
    category: str = Field(default="mechanistic", description="Question category: mechanistic, genetic, clinical, network")
    difficulty: str = Field(default="moderate", description="Difficulty: basic, moderate, advanced, expert")
    entities: List[EntityRef] = Field(default_factory=list, description="Gold standard entities")
    edges: List[EdgeRef] = Field(default_factory=list, description="Gold standard edges (mechanistic path)")
    workflow: List[WorkflowStep] = Field(default_factory=list, description="Ordered validation steps")
    tags: List[str] = Field(default_factory=list, description="Tags for filtering (e.g., 'pharmacology', 'rare_disease')")
    source: str = Field(default="manual", description="Source: manual, drugmechdb, bte-rag, literature")
    version: str = Field(default="1.0.0", description="Question version")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class StepResult(BaseModel):
    """Result of executing a single CQ workflow step."""
    model_config = ConfigDict(extra="forbid")
    step_id: str
    status: str = Field(description="pass, fail, partial, skip")
    expected_curie: Optional[str] = None
    actual_curie: Optional[str] = None
    tool_used: Optional[str] = None
    tier: str = "tier1"
    notes: str = ""

class CQResult(BaseModel):
    """Complete result of evaluating a competency question."""
    model_config = ConfigDict(extra="forbid")
    cq_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    step_results: List[StepResult] = Field(default_factory=list)
    entity_score: float = Field(default=0.0, description="Fraction of entities resolved correctly (0-1)")
    edge_score: float = Field(default=0.0, description="Fraction of edges validated (0-1)")
    path_complete: bool = Field(default=False, description="Whether full gold standard path was reconstructed")
    overall_score: float = Field(default=0.0, description="Weighted overall score (0-1)")
    notes: str = ""


# ---------------------------------------------------------------------------
# Catalog storage (JSON file on disk, versioned)
# ---------------------------------------------------------------------------

CATALOG_DIR = os.environ.get("CQ_CATALOG_DIR", os.path.join(os.path.dirname(__file__), "catalog"))
CATALOG_FILE = os.path.join(CATALOG_DIR, "cq-catalog.json")
RESULTS_DIR = os.path.join(CATALOG_DIR, "results")


def _ensure_dirs():
    os.makedirs(CATALOG_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)


def _load_catalog() -> Dict[str, Any]:
    _ensure_dirs()
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r") as f:
            return json.load(f)
    return {"version": "1.0.0", "questions": {}, "metadata": {"created": datetime.now(timezone.utc).isoformat()}}


def _save_catalog(catalog: Dict[str, Any]):
    _ensure_dirs()
    catalog["metadata"]["updated"] = datetime.now(timezone.utc).isoformat()
    with open(CATALOG_FILE, "w") as f:
        json.dump(catalog, f, indent=2)


def _save_result(result: CQResult):
    _ensure_dirs()
    filename = f"{result.cq_id}_{result.timestamp.replace(':', '-')}.json"
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(result.model_dump(), f, indent=2)


# ---------------------------------------------------------------------------
# MCP Tools — Catalog Management
# ---------------------------------------------------------------------------

@mcp.tool(
    name="cq_list",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}
)
async def cq_list(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    difficulty: Optional[str] = None
) -> str:
    """List competency questions in the catalog, optionally filtered.

    Args:
        category: Filter by category (mechanistic, genetic, clinical, network)
        tag: Filter by tag (e.g., 'pharmacology', 'rare_disease')
        difficulty: Filter by difficulty (basic, moderate, advanced, expert)

    Returns:
        Summary of matching CQs with id, title, category, difficulty, entity count, edge count.
    """
    catalog = _load_catalog()
    questions = catalog.get("questions", {})

    results = []
    for cq_id, cq_data in questions.items():
        if category and cq_data.get("category") != category:
            continue
        if tag and tag not in cq_data.get("tags", []):
            continue
        if difficulty and cq_data.get("difficulty") != difficulty:
            continue
        results.append({
            "id": cq_id,
            "title": cq_data.get("title", ""),
            "category": cq_data.get("category", ""),
            "difficulty": cq_data.get("difficulty", ""),
            "entities": len(cq_data.get("entities", [])),
            "edges": len(cq_data.get("edges", [])),
            "steps": len(cq_data.get("workflow", [])),
            "tags": cq_data.get("tags", []),
            "version": cq_data.get("version", "1.0.0")
        })

    return json.dumps({
        "total": len(results),
        "catalog_version": catalog.get("version", "1.0.0"),
        "questions": results
    }, indent=2)


@mcp.tool(
    name="cq_get",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}
)
async def cq_get(cq_id: str) -> str:
    """Get full details of a competency question including gold standard path and workflow.

    Args:
        cq_id: The CQ identifier (e.g., 'cq1')

    Returns:
        Complete CQ with entities, edges, workflow steps, and metadata.
    """
    catalog = _load_catalog()
    cq_data = catalog.get("questions", {}).get(cq_id)
    if not cq_data:
        return json.dumps({"error": f"CQ '{cq_id}' not found", "available": list(catalog.get("questions", {}).keys())})
    return json.dumps(cq_data, indent=2)


@mcp.tool(
    name="cq_add",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False}
)
async def cq_add(cq_json: str) -> str:
    """Add or update a competency question in the catalog.

    Args:
        cq_json: JSON string representing a CompetencyQuestion object.
                 Must include: id, title, question, entities, edges, workflow.

    Returns:
        Confirmation with the CQ id and entity/edge counts.
    """
    try:
        cq_data = json.loads(cq_json)
        cq = CompetencyQuestion(**cq_data)
    except Exception as e:
        return json.dumps({"error": f"Invalid CQ data: {str(e)}"})

    catalog = _load_catalog()
    is_update = cq.id in catalog.get("questions", {})
    catalog.setdefault("questions", {})[cq.id] = cq.model_dump()
    _save_catalog(catalog)

    return json.dumps({
        "status": "updated" if is_update else "created",
        "cq_id": cq.id,
        "entities": len(cq.entities),
        "edges": len(cq.edges),
        "workflow_steps": len(cq.workflow)
    })


@mcp.tool(
    name="cq_import_from_markdown",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False}
)
async def cq_import_from_markdown(markdown_path: str) -> str:
    """Import competency questions from a markdown catalog file.

    Parses the structured markdown format used in competency-questions-catalog.md
    and creates CQ entries in the catalog. This is the bootstrap path for
    initializing the golden test set from the existing catalog document.

    Args:
        markdown_path: Path to the competency-questions-catalog.md file.

    Returns:
        Summary of imported CQs with count and any parse warnings.
    """
    if not os.path.exists(markdown_path):
        return json.dumps({"error": f"File not found: {markdown_path}"})

    with open(markdown_path, "r") as f:
        content = f.read()

    # Parse markdown CQ sections — this is a structured format parser
    # The catalog uses ## cqN headers with entity tables and workflow steps
    import re
    cq_sections = re.split(r'^## (cq\d+)', content, flags=re.MULTILINE)

    imported = []
    warnings = []

    # cq_sections[0] is preamble, then pairs of (id, content)
    for i in range(1, len(cq_sections), 2):
        if i + 1 >= len(cq_sections):
            break
        cq_id = cq_sections[i].strip()
        section = cq_sections[i + 1]

        # Extract title from first line
        lines = section.strip().split("\n")
        title = ""
        question = ""
        for line in lines:
            if line.startswith("**Title"):
                title = re.sub(r'\*\*Title[:\s]*\*\*\s*', '', line).strip()
            elif line.startswith("**Question"):
                question = re.sub(r'\*\*Question[:\s]*\*\*\s*', '', line).strip()

        # Extract entities from table rows matching CURIE patterns
        entities = []
        entity_pattern = re.compile(r'\|\s*(\w+)\s*\|\s*([^|]+)\s*\|\s*([A-Z][A-Za-z_]+:[^\s|]+)')
        for match in entity_pattern.finditer(section):
            entities.append({
                "name": match.group(2).strip(),
                "curie": match.group(3).strip(),
                "entity_type": match.group(1).strip().lower()
            })

        # Extract gold standard path edges
        edges = []
        path_pattern = re.compile(r'(\w+:[^\s]+)\s*--\[(\w+)\]-->\s*(\w+:[^\s]+)')
        for match in path_pattern.finditer(section):
            edges.append({
                "source": match.group(1),
                "target": match.group(3),
                "relation": match.group(2),
                "evidence_tier": "tier1"
            })

        if title or question:
            cq = CompetencyQuestion(
                id=cq_id,
                title=title or f"Competency Question {cq_id}",
                question=question or title,
                entities=[EntityRef(**e) for e in entities],
                edges=[EdgeRef(**e) for e in edges],
                source="competency-questions-catalog.md"
            )
            catalog = _load_catalog()
            catalog.setdefault("questions", {})[cq_id] = cq.model_dump()
            _save_catalog(catalog)
            imported.append(cq_id)
        else:
            warnings.append(f"{cq_id}: could not parse title or question")

    return json.dumps({
        "imported": len(imported),
        "cq_ids": imported,
        "warnings": warnings,
        "note": "Review imported CQs with cq_get and refine entities/edges/workflow as needed"
    }, indent=2)


# ---------------------------------------------------------------------------
# MCP Tools — Scoring and Results
# ---------------------------------------------------------------------------

@mcp.tool(
    name="cq_record_step",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False}
)
async def cq_record_step(
    cq_id: str,
    step_id: str,
    status: str,
    expected_curie: Optional[str] = None,
    actual_curie: Optional[str] = None,
    tool_used: Optional[str] = None,
    tier: str = "tier1",
    notes: str = ""
) -> str:
    """Record the result of executing a single CQ workflow step.

    Called by the evaluation skill after each step in a CQ workflow.
    Results accumulate in a session buffer until cq_score is called.

    Args:
        cq_id: The CQ being evaluated
        step_id: Which workflow step (e.g., 'anchor', 'mechanism')
        status: Result — pass, fail, partial, skip
        expected_curie: Gold standard CURIE (if applicable)
        actual_curie: CURIE returned by the tool (if applicable)
        tool_used: Tool or curl pattern used
        tier: Architecture tier (tier1, tier2, tier3)
        notes: Additional context

    Returns:
        Confirmation with running step count.
    """
    result = StepResult(
        step_id=step_id,
        status=status,
        expected_curie=expected_curie,
        actual_curie=actual_curie,
        tool_used=tool_used,
        tier=tier,
        notes=notes
    )

    # Store in session buffer (in-memory, keyed by cq_id)
    if not hasattr(cq_record_step, "_buffers"):
        cq_record_step._buffers = {}
    cq_record_step._buffers.setdefault(cq_id, []).append(result.model_dump())

    return json.dumps({
        "cq_id": cq_id,
        "step_id": step_id,
        "status": status,
        "steps_recorded": len(cq_record_step._buffers[cq_id])
    })


@mcp.tool(
    name="cq_score",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False}
)
async def cq_score(cq_id: str) -> str:
    """Score a CQ evaluation by comparing recorded steps against gold standard.

    Calculates entity_score (fraction of entities resolved), edge_score
    (fraction of edges validated), path_complete (full path reconstructed),
    and overall_score (weighted composite).

    Scoring weights (aligned with BTE-RAG methodology):
      entity_score: 0.4 (node resolution accuracy)
      edge_score: 0.4 (relationship coverage)
      path_complete: 0.2 (end-to-end path bonus)

    Args:
        cq_id: The CQ to score

    Returns:
        Complete CQResult with scores and per-step details.
    """
    # Get gold standard
    catalog = _load_catalog()
    cq_data = catalog.get("questions", {}).get(cq_id)
    if not cq_data:
        return json.dumps({"error": f"CQ '{cq_id}' not found in catalog"})

    # Get recorded steps
    buffers = getattr(cq_record_step, "_buffers", {})
    steps = buffers.get(cq_id, [])
    if not steps:
        return json.dumps({"error": f"No steps recorded for '{cq_id}'. Run the workflow first."})

    # Score entities
    gold_entities = {e["curie"] for e in cq_data.get("entities", [])}
    resolved_entities = {s["actual_curie"] for s in steps if s.get("actual_curie") and s["status"] in ("pass", "partial")}
    entity_score = len(gold_entities & resolved_entities) / max(len(gold_entities), 1)

    # Score edges
    gold_edges = cq_data.get("edges", [])
    passed_steps = {s["step_id"] for s in steps if s["status"] == "pass"}
    edge_score = len(passed_steps) / max(len(gold_edges) + len(cq_data.get("workflow", [])), 1)

    # Path completeness — all entities resolved AND all edges validated
    path_complete = entity_score == 1.0 and all(s["status"] in ("pass", "partial") for s in steps)

    # Weighted overall
    overall_score = (entity_score * 0.4) + (edge_score * 0.4) + (0.2 if path_complete else 0.0)

    result = CQResult(
        cq_id=cq_id,
        step_results=[StepResult(**s) for s in steps],
        entity_score=round(entity_score, 3),
        edge_score=round(edge_score, 3),
        path_complete=path_complete,
        overall_score=round(overall_score, 3),
        notes=f"Scored against {len(gold_entities)} entities, {len(gold_edges)} edges"
    )

    _save_result(result)

    # Clear buffer
    buffers.pop(cq_id, None)

    return json.dumps(result.model_dump(), indent=2)


@mcp.tool(
    name="cq_results",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}
)
async def cq_results(cq_id: Optional[str] = None, limit: int = 10) -> str:
    """Retrieve past CQ evaluation results.

    Args:
        cq_id: Filter by CQ id (optional — returns all if not specified)
        limit: Maximum number of results to return (default 10)

    Returns:
        List of CQResult summaries ordered by timestamp (newest first).
    """
    _ensure_dirs()
    results = []
    for filename in sorted(os.listdir(RESULTS_DIR), reverse=True):
        if not filename.endswith(".json"):
            continue
        if cq_id and not filename.startswith(cq_id + "_"):
            continue
        filepath = os.path.join(RESULTS_DIR, filename)
        with open(filepath, "r") as f:
            result = json.load(f)
            results.append({
                "cq_id": result.get("cq_id"),
                "timestamp": result.get("timestamp"),
                "entity_score": result.get("entity_score"),
                "edge_score": result.get("edge_score"),
                "path_complete": result.get("path_complete"),
                "overall_score": result.get("overall_score")
            })
        if len(results) >= limit:
            break

    return json.dumps({"results": results, "total": len(results)}, indent=2)


@mcp.tool(
    name="cq_compare",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}
)
async def cq_compare(cq_id: str) -> str:
    """Compare all historical results for a CQ to show score trends over time.

    Useful for measuring whether skill/tool improvements affect CQ pass rates.

    Args:
        cq_id: The CQ to compare results for

    Returns:
        Time series of scores for the specified CQ.
    """
    _ensure_dirs()
    series = []
    for filename in sorted(os.listdir(RESULTS_DIR)):
        if not filename.startswith(cq_id + "_") or not filename.endswith(".json"):
            continue
        filepath = os.path.join(RESULTS_DIR, filename)
        with open(filepath, "r") as f:
            result = json.load(f)
            series.append({
                "timestamp": result.get("timestamp"),
                "entity_score": result.get("entity_score"),
                "edge_score": result.get("edge_score"),
                "overall_score": result.get("overall_score"),
                "path_complete": result.get("path_complete")
            })

    return json.dumps({
        "cq_id": cq_id,
        "evaluations": len(series),
        "series": series
    }, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
