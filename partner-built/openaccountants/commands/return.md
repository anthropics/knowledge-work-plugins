---
name: return
description: Walk through a full tax return for any jurisdiction — intake, transaction classification, working paper, reviewer handoff.
---

The user wants help preparing a tax return.

Ask them (if not already clear):
- **Jurisdiction**: country, US state, or province
- **Tax year**: e.g. 2025
- **Entity type**: sole proprietor, self-employed, single-member LLC, S-corp, C-corp, partnership, individual (W-2 only), or other

Then:

1. Call `start({ intent: "tax return", jurisdiction: <code> })` on the `openaccountants` MCP server.
2. For each skill in the returned plan, call `get_skill({ slug })`.
3. Run the intake from the loaded intake skill — ask the user only the questions the documents don't answer.
4. When the user provides bank statements, invoices, or transaction lists, classify every transaction using the rules in the loaded skills. Use the three-outcome system: **Classified** (clear), **Assumed** (conservative default, flag for reviewer), **Needs Input** (ask the user).
5. Produce a working paper:
   - Classified transactions grouped by tax category
   - Computed totals for each return-line item
   - All assumptions disclosed
   - Items flagged for accountant review
   - Filing deadlines and payment dates
6. End by asking the user if they want a licensed accountant to review before filing. If yes, call `request_accountant_review` with the working paper attached.

**Conservative defaults**: when uncertain, assume **more** tax, never less. Never compute amounts from your training data — use only the rates and thresholds from the loaded skills.
