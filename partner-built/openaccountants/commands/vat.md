---
name: vat
description: VAT / GST / sales tax return — classify transactions, compute return-form box totals, flag audit-risk items.
---

The user wants help with VAT, GST, or sales tax.

Ask them (if not already clear):
- **Jurisdiction**: country (or US state for sales tax)
- **Period**: e.g. "Q1 2025", "January 2025", "2025"

Then:

1. Call `start({ intent: "VAT return", jurisdiction: <code> })` on the `openaccountants` MCP server.
2. Load the returned VAT/GST skill(s) via `get_skill`.
3. When the user provides transactions, classify each using the skill's rate categories and supplier pattern library. Determine for each: taxable supply (standard / reduced / zero-rated), exempt supply, out of scope, reverse charge, or input VAT recoverable.
4. Produce a return working paper:
   - Output VAT by rate
   - Input VAT recoverable
   - Net VAT payable/refundable
   - Items flagged as Assumed or Needs Input
5. Map the totals to the country's return-form boxes (e.g. UK VAT100 Box 1-9, Malta VAT Article 11 simplified form, Germany UStVA Kennzahlen, Italy LIPE).
6. Surface any AUDIT FLASH POINT markers the skill flags — these are the line items most likely to trigger a tax authority query.
7. End by offering to route to a licensed accountant for a pre-filing review via `request_accountant_review`.
