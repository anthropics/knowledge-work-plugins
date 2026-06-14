# OpenAccountants Plugin for Claude Code and Cowork

Give Claude **verified tax & accounting skills for 190+ jurisdictions** — every answer linked to a **named licensed accountant**. Powered by the [OpenAccountants MCP Server](https://www.openaccountants.com/api/mcp) with **one-click integration**.

---

## 🔌 One-Click MCP Server Integration

This plugin **automatically configures the OpenAccountants MCP server** when installed. No API keys, no setup, no config files — just install and start asking real tax questions for any country, US state, or industry.

---

## ✅ What you get

**882 verified skills** across **190+ jurisdictions** (every country + US state + Canadian province). **11 MCP tools.** Country-verified sign-offs from named licensed accountants — Michael Cutajar CPA (Malta), Werner Britz CA(SA) (South Africa), and a growing global network.

The skill content is kept current with annual rate refreshes, post-legislative updates, and IRS Revenue Procedure releases — so Claude isn't relying on training-data tax rates that drifted two years ago.

---

## 🧰 Slash commands

| Command | What it does |
|---|---|
| `/openaccountants:start` | Front door — give Claude an intent ("VAT return", "tax filing", "formation") and a jurisdiction, get a scoped plan with the right skills loaded |
| `/openaccountants:return` | Walk through a full tax return for any jurisdiction — intake → classification → working paper → reviewer handoff |
| `/openaccountants:vat` | VAT / GST / sales tax return — classifies transactions, computes return-form box totals, flags audit-risk items |
| `/openaccountants:formation` | Entity choice + incorporation across jurisdictions — LLC vs S-corp vs LTD, ongoing compliance, tax election windows |
| `/openaccountants:compare` | Side-by-side compare 2-5 jurisdictions — entity choice, effective rates, residency planning, cross-border decisions |
| `/openaccountants:rates` | Current-year US federal indexed rates — brackets, 401(k) limits, SS wage base, FEIE, gift/estate, mileage, 1099-K |
| `/openaccountants:review` | **The handoff.** Routes the user to the named lead verifier for their jurisdiction with their working paper attached and a Calendly booking link |

### The differentiator: `/openaccountants:review`

Every honest AI tax workflow ends with *"have a professional review before filing"*. This command turns that closing line into an actual booking.

When you call `/openaccountants:review`, Claude captures your working paper (classified transactions, computations, draft return lines), routes it to the named lead verifier for your jurisdiction, logs the scenario server-side so the accountant sees real context, and returns their Calendly URL. No client-accountant relationship until both sides sign an engagement letter — the first call is just a review conversation.

---

## 🧠 How it works (the 11 MCP tools)

**Discovery**
- `start` — scopes intent + jurisdiction, returns a ready plan
- `list_jurisdictions` — every country/state covered with skill counts + lead verifier
- `list_skills` — full catalogue, filterable by jurisdiction
- `list_verifiers` — every named accountant in the network

**Skill access**
- `get_skill` — fetch the verified markdown for a skill (rates, rules, audit flash points, citations)
- `get_skill_sections` — parsed sections for step-by-step rule application
- `search_skills` — keyword search ("home office deduction", "reverse charge", "§1202 QSBS")

**Tax intelligence**
- `get_rates` — machine-readable US federal annual rates for 2025/2026
- `compare_jurisdictions` — load 2-5 jurisdictions side-by-side

**Handoff & feedback**
- `request_accountant_review` — the AI-to-verified-human handoff
- `submit_feedback` — pre-filled GitHub Issue when you spot an error or outdated rate

---

## 🌍 Per-jurisdiction & per-topic plugins

Want a plugin pre-scoped to one country or one topic? OpenAccountants publishes a **separate marketplace** with **83 specialised plugins**:

```bash
claude plugin marketplace add openaccountants/marketplace
```

Then install any of:

- **Per country**: `openaccountants-mt` (Malta, verified by Michael Cutajar CPA) · `openaccountants-za` (South Africa, Werner Britz CA(SA)) · `openaccountants-us-ca` · `openaccountants-gb` · `openaccountants-de` · `openaccountants-jp` · `openaccountants-in` · `openaccountants-br` · *…60 more*
- **Per topic**: `openaccountants-crypto-tax` · `openaccountants-transfer-pricing` · `openaccountants-company-formation` · `openaccountants-payroll` · `openaccountants-vat-gst` · `openaccountants-tax-optimization` · `openaccountants-bookkeeping` · `openaccountants-cross-border`
- **Per vertical**: `openaccountants-vertical-saas-digital-products` · `openaccountants-vertical-ecommerce-seller` · `openaccountants-vertical-freelance-developer` · `openaccountants-vertical-property-investor` · *…10 more*

All 83 route to the same hosted MCP backend — install only what you need.

---

## 🏛️ Trust model

- **Open source.** All 882 skills are public markdown at [github.com/openaccountants/openaccountants](https://github.com/openaccountants/openaccountants).
- **Country-verified.** Each jurisdiction is signed off by a named licensed accountant whose credential and Calendly link are published. Tier 1 = signed; Tier 2 = research-verified (flagged honestly to the user).
- **Cite-able.** Every skill output includes a provenance footer with the named verifier, the skill slug, and a working-paper attribution line.
- **Working papers, not advice.** Outputs always carry the *not-tax-advice* disclaimer. The handoff to a real accountant is built into the tool surface.

---

## 📚 Resources

- **Website**: [openaccountants.com](https://openaccountants.com)
- **Install (any AI client)**: [openaccountants.com/connect](https://openaccountants.com/connect)
- **Source code**: [github.com/openaccountants/openaccountants](https://github.com/openaccountants/openaccountants)
- **Plugin marketplace**: [github.com/openaccountants/marketplace](https://github.com/openaccountants/marketplace)
- **Talk to a verifier**: [calendly.com/openaccountants-info/30min](https://calendly.com/openaccountants-info/30min)

---

## ⚠️ Disclaimer

Outputs are **working papers, not filed returns**. No client-accountant relationship is created until both parties sign an engagement letter. Use `/openaccountants:review` to route to a credentialed accountant before acting on anything.
