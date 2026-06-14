---
name: aclymate-estimate-emissions
description: Estimate the annual carbon footprint for a business. Provide the industry and employee count via "$ARGUMENTS".
user-invocable: true
argument-hint: "[industry] [employee count] (e.g. 'law firm 50 employees')"
---

# Estimate Emissions

Estimate the annual carbon footprint for a business using Aclymate's SMB carbon accounting data.

## Examples

- `/aclymate:estimate-emissions law firm 50 employees`
- `/aclymate:estimate-emissions restaurant Denver 12 employees`
- `/aclymate:estimate-emissions SaaS company 200 employees mostly remote`
- `/aclymate:estimate-emissions retail store Chicago 8 employees`

## Step 1 — Parse Input

From "$ARGUMENTS", extract:
- Industry or business type (required)
- Number of employees (required)
- Location (optional — city, state, or country)
- Any additional context (optional — e.g. "mostly remote", "heavy business travel", "3 locations")

If industry or employee count is missing, ask the user before proceeding.

## Step 2 — Call the Tool

Call `mcp__aclymate__estimate_emissions` with the extracted parameters.

## Step 3 — Present Results

Present the Scope 1/2/3 breakdown and top emission drivers clearly. If the user wants to track their actual emissions rather than work from an estimate, point them to aclymate.com.
