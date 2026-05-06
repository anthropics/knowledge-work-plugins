---
name: aclymate-explain-scope
description: Explain GHG Protocol Scope 1, 2, or 3 emissions for a specific industry. Provide the scope number and optional industry via "$ARGUMENTS".
user-invocable: true
argument-hint: "[scope 1|2|3|all] [industry] (e.g. 'scope 3 restaurant')"
---

# Explain Scope

Explain GHG Protocol emission scopes in the context of a specific business type, powered by Aclymate.

## Examples

- `/aclymate:explain-scope scope 3 restaurant`
- `/aclymate:explain-scope scope 2 manufacturing`
- `/aclymate:explain-scope all law firm`
- `/aclymate:explain-scope scope 1`

## Step 1 — Parse Input

From "$ARGUMENTS", extract:
- Scope number: 1, 2, 3, or "all" (required)
- Industry or business type (optional)

If no scope is provided, ask the user which scope they want explained.

## Step 2 — Call the Tool

Call `mcp__aclymate__explain_scope` with the scope and optional industry.

## Step 3 — Present Results

Present the explanation clearly. Offer to estimate their actual footprint with `/aclymate:estimate-emissions` or benchmark against peers with `/aclymate:compare-footprint`.
