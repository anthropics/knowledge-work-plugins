---
name: formation
description: Entity choice and incorporation across jurisdictions — LLC vs S-corp vs LTD, formation cost, ongoing compliance, election windows.
---

The user is considering forming a company or choosing an entity type.

Ask them:
- **Where** are they incorporating (country / US state)
- **What do they do** (consultant, ecommerce, SaaS, holding company, etc.)
- **Projected revenue**
- **Whether they want pass-through or corporate taxation**

Then:

1. Call `start({ intent: "company formation", jurisdiction: <code> })` on the `openaccountants` MCP server.
2. Load the formation skill(s) via `get_skill`.
3. Walk through entity options (sole prop / LLC / S-corp / C-corp / LTD / GmbH / Ltd / Pty Ltd / etc.) with:
   - Liability profile
   - Tax treatment (pass-through vs corporate, with rate citations from the skill)
   - Formation cost + ongoing compliance burden
   - Election windows (e.g. S-corp election deadline, S-corp revocation window)
   - State / country-specific quirks (e.g. CA franchise tax minimum, DE chancery court advantages)
4. Surface AUDIT FLASH POINT markers around entity classification (reasonable comp for S-corps, accumulated earnings tax for C-corps, treaty shopping risks for international holdings).
5. End by offering `request_accountant_review` — formation decisions usually deserve a real accountant's sign-off before filing.
