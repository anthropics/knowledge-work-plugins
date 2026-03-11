---
name: rules-export
description: Export business rules from the knowledge graph in standard machine-readable formats — DMN XML, JSON, CSV, and Gherkin BDD scenarios. Runs after Phase 2 business rules generation to produce files that feed directly into BRMS tools, rule engines, and test frameworks.
---

# Business Rules Export

You produce machine-readable exports of the business rules discovered during
Phase 2. The `business_rules.md` deliverable is the human-readable layer; these
exports are the machine-readable layer that feeds into BRMS tools (Camunda,
Drools, IBM ODM), lightweight JSON rule engines, spreadsheet review, and BDD
test frameworks.

## Output Files

Per domain, generate these files in `.magellan/domains/<domain>/deliverables/`:

| Format | File | Use Case |
|--------|------|----------|
| DMN XML | `rules_<domain>.dmn` | BRMS import (Camunda, Drools, IBM ODM) |
| JSON | `rules_<domain>.json` | Lightweight engines (json-rules-engine, similar) |
| CSV | `rules_<domain>.csv` | Spreadsheet review, bulk editing |
| Gherkin | `rules_<domain>.feature` | BDD test scenarios for QA teams |

## When to Generate

- After business rules are generated in Phase 2 (Step 12)
- On demand when an architect requests rule exports

## Process

For each domain discovered via Glob on `.magellan/domains/*/`:

1. Use the Read tool to read `.magellan/domains/<domain>/summary.json` for the
   domain overview.
2. Use Glob on `.magellan/domains/<domain>/entities/*.json` to discover entities,
   then Read the entities tagged with `business_rule`.
3. Read the existing `business_rules.md` from the deliverables directory for
   the classification (HARD/SOFT/QUESTIONABLE) and condition/action pairs.
4. Model each rule as a structured object (see Rule Structure below).
5. Generate all four export formats from the structured rules.
6. Write each file immediately after generating it.

## Rule Structure

Model each rule internally before generating exports:

```json
{
  "rule_id": "BR-FIN-001",
  "domain": "financial_management_payments",
  "name": "Invoice Manager Approval Threshold",
  "classification": "HARD",
  "condition": "invoice_amount > 15000",
  "action": "require_manager_approval",
  "decision_table": null,
  "source_entity": "billing:invoice_approval",
  "source_document": "CBBLKBOOK.cblle",
  "source_quote": "IF WS-INV-AMT > 15000 PERFORM MANAGER-APPROVAL-PARA",
  "confidence": 0.85,
  "notes": "Threshold value conflicts with QA manual ($10k) — see C-001",
  "tags": ["financial", "approval", "threshold"]
}
```

For rules with multiple conditions, use a decision table:

```json
{
  "rule_id": "BR-SAL-015",
  "name": "Sale Reversal Eligibility",
  "classification": "HARD",
  "decision_table": {
    "inputs": ["sale_age_hours", "settlement_status", "title_transferred"],
    "output": "reversal_allowed",
    "rules": [
      {"conditions": ["<= 24", "pending", "false"], "result": "yes"},
      {"conditions": ["<= 24", "pending", "true"], "result": "manual_review"},
      {"conditions": ["> 24", "*", "*"], "result": "no"}
    ]
  }
}
```

## DMN XML Format (`rules_<domain>.dmn`)

Generate valid DMN 1.3 XML. Each rule becomes a decision element. Decision
tables become `decisionTable` elements with input and output columns.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/"
             xmlns:dmndi="https://www.omg.org/spec/DMN/20191111/DMNDI/"
             id="definitions_billing"
             name="billing Business Rules"
             namespace="https://magellan.example.com/rules/billing">

  <decision id="BR-FIN-001" name="Invoice Manager Approval Threshold">
    <description>HARD — Source: billing:invoice_approval (CBBLKBOOK.cblle)
    Confidence: 0.85</description>
    <decisionTable id="dt_BR-FIN-001" hitPolicy="UNIQUE">
      <input id="input_1" label="invoice_amount">
        <inputExpression typeRef="number">
          <text>invoice_amount</text>
        </inputExpression>
      </input>
      <output id="output_1" label="action" typeRef="string"/>
      <rule id="rule_1">
        <inputEntry><text>&gt; 15000</text></inputEntry>
        <outputEntry><text>"require_manager_approval"</text></outputEntry>
      </rule>
      <rule id="rule_2">
        <inputEntry><text>&lt;= 15000</text></inputEntry>
        <outputEntry><text>"auto_approve"</text></outputEntry>
      </rule>
    </decisionTable>
  </decision>

</definitions>
```

Rules:
- Use DMN 1.3 namespace (`https://www.omg.org/spec/DMN/20191111/MODEL/`)
- Each rule is a `<decision>` element with the rule_id as its id attribute
- Simple condition/action rules become single-row decision tables
- Multi-condition rules use their decision_table structure directly
- Include classification and source in the `<description>` element
- Escape XML entities properly (`&gt;`, `&lt;`, `&amp;`)

## JSON Format (`rules_<domain>.json`)

Generate a JSON array of rule objects compatible with lightweight rule engines:

```json
{
  "domain": "billing",
  "generated": "2026-02-23T10:00:00Z",
  "rule_count": 25,
  "distribution": {
    "HARD": 8,
    "SOFT": 12,
    "QUESTIONABLE": 5
  },
  "rules": [
    {
      "rule_id": "BR-FIN-001",
      "name": "Invoice Manager Approval Threshold",
      "classification": "HARD",
      "condition": {
        "field": "invoice_amount",
        "operator": ">",
        "value": 15000
      },
      "action": {
        "type": "require_manager_approval"
      },
      "source_entity": "billing:invoice_approval",
      "source_document": "CBBLKBOOK.cblle",
      "confidence": 0.85,
      "tags": ["financial", "approval", "threshold"]
    }
  ]
}
```

For decision table rules, use a `conditions` array instead of a single condition:

```json
{
  "rule_id": "BR-SAL-015",
  "name": "Sale Reversal Eligibility",
  "classification": "HARD",
  "conditions": [
    {"field": "sale_age_hours", "operator": "<=", "value": 24},
    {"field": "settlement_status", "operator": "==", "value": "pending"},
    {"field": "title_transferred", "operator": "==", "value": false}
  ],
  "action": {
    "type": "allow_reversal"
  }
}
```

## CSV Format (`rules_<domain>.csv`)

Standard CSV with headers. Opens cleanly in Excel/Google Sheets:

```csv
rule_id,name,classification,condition,action,source_entity,source_document,confidence,tags,notes
BR-FIN-001,Invoice Manager Approval Threshold,HARD,"invoice_amount > 15000",require_manager_approval,billing:invoice_approval,CBBLKBOOK.cblle,0.85,"financial;approval;threshold","Threshold conflicts with QA manual — see C-001"
```

Rules:
- Quote fields that contain commas, quotes, or newlines
- Use semicolons to separate tags within the tags field
- Decision table rules expand to one row per rule combination
- Include a header row

## Gherkin Format (`rules_<domain>.feature`)

Generate BDD scenarios for every business rule. Gherkin bridges the gap between
business analysts who define rules and QA engineers who validate them.

```gherkin
@domain:billing
Feature: Billing Domain Business Rules

  Business rules extracted from the Magellan knowledge graph.
  Source: .magellan/domains/billing/deliverables/business_rules.md

  @classification:HARD
  @confidence:0.85
  @rule:BR-FIN-001
  Scenario: Invoice above threshold requires manager approval
    Given an invoice with amount 20000
    When the invoice is submitted for processing
    Then manager approval should be required

  @classification:HARD
  @confidence:0.85
  @rule:BR-FIN-001
  Scenario: Invoice below threshold is auto-approved
    Given an invoice with amount 10000
    When the invoice is submitted for processing
    Then the invoice should be auto-approved

  @classification:HARD
  @confidence:0.85
  @rule:BR-FIN-001
  Scenario Outline: Invoice approval threshold boundary testing
    Given an invoice with amount <amount>
    When the invoice is submitted for processing
    Then the result should be <outcome>

    Examples:
      | amount | outcome            |
      | 14999  | auto-approved      |
      | 15000  | auto-approved      |
      | 15001  | requires-approval  |
```

Gherkin generation rules:

- **Confidence score visible**: tagged on every scenario (`@confidence:0.85`).
  Teams can filter to only test high-confidence rules first.
- **Classification as tag**: `@classification:HARD` allows running only HARD rules.
- **Source traceability**: feature description cites the source document and entity.
- **Boundary tests**: numeric threshold rules auto-generate Scenario Outlines with
  boundary values (below, at, above the threshold).
- **Decision table rules**: generate Scenario Outlines with Examples tables matching
  the decision table rows.
- **QUESTIONABLE rules**: tag scenarios with `@needs-review` so QA knows to validate
  the rule itself, not just its behavior.
- **Condition/action mapping**: Given = set up the condition, When = trigger the
  evaluation, Then = assert the action.

## Critical: Use Built-in Tools for Reading

- ALL KG data reads MUST use Claude's built-in tools:
  - **Discover domains**: Glob on `.magellan/domains/*/`
  - **Discover entities**: Glob on `.magellan/domains/<domain>/entities/*.json`
  - **Read entity details**: Read tool on `.magellan/domains/<domain>/entities/<entity_id>.json`
  - **Read domain summaries**: Read tool on `.magellan/domains/<domain>/summary.json`
- Read `business_rules.md` from the deliverables directory using the Read tool
  (it's a generated artifact, not KG data).
- Write export files using the Write tool (same pattern as other generated
  artifacts in deliverables/).

## What You Do NOT Do

- Do not invent rules. Only export rules that exist in the KG.
- Do not guess at conditions or actions. If a rule's condition can't be extracted
  as a structured expression, use the natural language description and note it.
- Do not generate invalid XML. Escape all special characters in DMN output.
- Do not skip QUESTIONABLE rules. Export all rules with their classification —
  consumers decide what to use.
- Do not omit source traceability. Every exported rule must reference its KG
  entity and source document.
- Do not combine domains. Generate separate export files per domain.
