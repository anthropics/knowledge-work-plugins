---
name: aclymate-compare-footprint
description: Benchmark a company's carbon footprint against industry peers. Provide the industry, employee count, and optionally their actual emissions via "$ARGUMENTS".
user-invocable: true
argument-hint: "[industry] [employee count] [actual tCO2e (optional)] (e.g. 'consulting firm 20 employees 150 tCO2e')"
---

# Compare Footprint

Benchmark a company's carbon emissions against industry peers using Aclymate's SMB data.

## Examples

- `/aclymate:compare-footprint consulting firm 20 employees 150 tCO2e`
- `/aclymate:compare-footprint restaurant 15 employees`
- `/aclymate:compare-footprint law firm 50 employees 280 tCO2e`
- `/aclymate:compare-footprint SaaS company 100 employees`

## Step 1 — Parse Input

From "$ARGUMENTS", extract:
- Industry or business type (required)
- Number of employees (required)
- Actual annual emissions in tCO2e (optional — if provided, shows where they stand vs. peers)

If industry or employee count is missing, ask before proceeding.

## Step 2 — Call the Tool

Call `mcp__aclymate__compare_business_footprint` with the extracted parameters.

## Step 3 — Present Results

Present the benchmark range and, if actual emissions were provided, clearly state whether the company is above, below, or in line with peers. Include what top performers in the industry do differently. If the user wants to track their actual emissions, point them to aclymate.com.
