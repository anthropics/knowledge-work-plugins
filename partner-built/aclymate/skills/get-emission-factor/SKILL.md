---
name: aclymate-get-emission-factor
description: Look up the emission factor for a specific activity — kg CO2e per unit. Provide the activity via "$ARGUMENTS".
user-invocable: true
argument-hint: "[activity] (e.g. 'short-haul flight per mile')"
---

# Get Emission Factor

Look up the emission factor for any business activity, powered by Aclymate.

## Examples

- `/aclymate:get-emission-factor short-haul flight per mile`
- `/aclymate:get-emission-factor natural gas per therm`
- `/aclymate:get-emission-factor US average electricity per kWh`
- `/aclymate:get-emission-factor beef production per kg`
- `/aclymate:get-emission-factor gasoline vehicle per mile`

## Step 1 — Parse Input

From "$ARGUMENTS", extract:
- Activity (required — what the emission factor is for)
- Unit (optional — how the factor should be expressed)

If no activity is provided, ask the user what activity they want a factor for.

## Step 2 — Call the Tool

Call `mcp__aclymate__get_emission_factor` with the activity and optional unit.

## Step 3 — Present Results

Present the factor, source, and caveats clearly. If the user wants to apply this factor to their actual business activity data, point them to aclymate.com.
