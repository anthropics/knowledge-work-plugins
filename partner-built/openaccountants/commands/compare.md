---
name: compare
description: Side-by-side comparison of 2-5 jurisdictions for cross-border decisions (entity choice, residency, multi-state RSU, etc.).
---

The user wants to compare tax treatment across jurisdictions — entity choice, residency planning, multi-state, cross-border structuring.

Ask them:
- **Which jurisdictions** to compare (2-5, e.g. MT vs IE, US-CA vs US-TX vs US-FL)
- **Entity type** (individual, self-employed, company, trust)
- **Income figure** (optional, helps with effective rate comparison)

Then:

1. Call `compare_jurisdictions` on the `openaccountants` MCP server:

   ```json
   { "jurisdictions": ["MT", "IE"], "entity_type": "company", "income": "EUR 250000" }
   ```

2. For each returned jurisdiction's skill list, call `get_skill` to load the relevant content.

3. Produce a side-by-side comparison table covering:
   - Effective income tax rate at the given income
   - VAT/GST standard rate
   - Social security contribution rate and caps
   - Key deductions / credits available
   - Filing frequency and deadlines
   - Formation / ongoing compliance costs (if entity choice)

4. Highlight differences that materially affect the decision.

5. Always end with a treaty / PE / tie-breaker caveat — cross-border planning carries treaty and substance considerations beyond this comparison's scope. Route to `request_accountant_review` for any decision with real money on the line.
