---
description: Find the cheapest business class flights between any two cities using creative routing and exhaustive search
argument-hint: "<origin> to <destination> in <month/dates>"
---

# Find Cheap Business Class Flights

Search for the cheapest possible business class flights using 8 creative pricing strategies.

## Trigger

User runs `/find-flights` or asks to find cheap business class flights, affordable premium cabin tickets, or business class deals.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Origin city** — city name or airport code. Confirm whether nearby airports are acceptable (default: yes).

2. **Destination city** — city name or airport code. Confirm whether nearby airports are acceptable (default: yes).

3. **Travel dates** — specific dates or a flexible range (e.g., "anytime in October", "first two weeks of March"). Ask how flexible if not specified.

4. **Number of passengers** — default is 1. Ask if not stated.

5. **Additional context** (optional):
   - Airline or alliance preferences/exclusions
   - Loyalty program memberships (e.g., Star Alliance Gold, OneWorld Sapphire)
   - Transferable points balances (Chase UR, Amex MR, Citi TY)
   - Budget ceiling per person

## Workflow

Read and follow the full skill at `skills/cheap-business-class-finder/SKILL.md`. The skill defines a 4-phase workflow:

1. **Phase 1 — Route Analysis**: Understand the geography, airlines, hubs, alliances, and seasonality.
2. **Phase 2 — Search Matrix**: Execute all 8 strategies (direct baseline, nearby airports, ex-EU/Asia hubs, multi-city, fifth-freedom, mistake fares, points/miles, date flexibility).
3. **Phase 3 — Deep Dive**: Verify top leads, check aircraft/product, calculate total costs including positioning.
4. **Phase 4 — Compile Results**: Deliver a ranked chat summary AND a professional .xlsx spreadsheet.

## Output

Deliver two things:

1. **Chat summary** — Top 5–8 options ranked by total cost, with savings percentages, route details, strategy used, tradeoffs, and booking instructions.

2. **Excel spreadsheet** — Detailed comparison with columns for rank, price, strategy, full itinerary, airlines, aircraft, seat product, travel time, stops, savings, booking source, fare class, and change/cancel policy. Use conditional formatting and filters.

Always end with important caveats: prices are snapshots, book quickly, separate tickets carry risk, check visa/transit requirements.
