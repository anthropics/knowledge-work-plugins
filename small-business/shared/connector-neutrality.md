# Connector neutrality — plugin-wide rule

Scope: **every skill, command, reference file, and onboarding flow.** This is
Anthropic's positioning for the plugin, not a house preference: the owner's
tool set decides what gets called. The plugin never decides which vendor an
owner should have.

---

## The rule

**Connectors in the same category are peers.** A ledger is a ledger. A CRM is
a CRM. A mailbox is a mailbox. No skill names one of them as the default, the
primary, the one that takes precedence, the fallback vendor, the alternate,
or the lesser path. Name what is connected, and run on that.

Categories this applies to, and the connectors in each today (alphabetical,
which is the order every list in the plugin uses when more than one is named):

| Category | Connectors |
|---|---|
| Accounting ledger | MYOB, NetSuite, QuickBooks, Xero, Zoho Books |
| CRM | HubSpot, Monday.com, Salesforce, Zoho CRM |
| Lead data and enrichment | Apollo, Clay |
| Mail | Gmail, Microsoft 365 |
| Calendar | Google Calendar |
| Payroll | Gusto, QuickBooks Payroll |
| Payments | PayPal, Square, Stripe |
| Storefront and point of sale (holds orders and stock) | Shopify, Square |
| Files | Google Drive, Microsoft 365 |
| Support | Zoho Desk |

Salesforce is reached as a custom connector the owner adds (its Headless 360 server has a per-org address and OAuth client), not through the plugin manifest; once added it is a peer like the rest. A connector that is not on this table is reached through `build-connector`,
which checks the connector directory first and connects through Zapier
otherwise. Once connected, it joins its category as a peer.

---

## What "peers" means in practice

**Gating is by category, never by vendor.** A skill that needs a ledger says
"a ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books)," and any one of
them opens the gate. The router's connector map is written the same way.

**Two connected in one category: read both, total from one.** Each connector
supplies what it uniquely holds. Any figure that must come from a single
place — a cash balance, a revenue total, an AR figure — comes from the one
the owner names as the source of record for that run, and the output says
which. Never sum the same figure across two connectors: that double-counts.
The router's Step 5 multiple-choice is how the owner names it; the answer
sticks for the session and can be stored in the business context.

**Capability limits are stated as capabilities, not as judgments.** "This
connector has no bill-write path, so the entries are exported for keying in"
is a capability. "Xero is read-only here, better if QuickBooks is
mid-migration" is a ranking. Write the first kind. Where a connector genuinely
cannot do part of a skill (MYOB holds no cash balance; a read-only ledger
cannot post a journal; Zoho Books holds no bill object, no bank feed, and no
report endpoints), say what it cannot do and what the skill does instead, in
one line, without comparing it to another vendor.

**Metered connectors say the price before spending.** A lead-data connector
charges credits per enriched row. A skill that uses one names the row count
and asks once per run before enriching. That is an approval gate, not a
ranking.

**Vendor-specific technical notes are fine.** A file like
`shared/quickbooks-report-traps.md` documents real behaviour of one
connector. That is not a preference; it is a gotcha. Keep those, label them
as connector-specific, and add sibling files for other connectors as their
traps are found.

**Worked examples may name a vendor.** An example has to run on something.
Naming QuickBooks in a transcript is fine; saying "let's connect QuickBooks
first" as advice is not. Examples show the owner's tool being used, never
being chosen for them.

---

## One connector, two registrations

The plugin's manifest (`.mcp.json`) declares every connector in the router
map so Cowork's plugin page can list them. Cowork registers each declared
server under the plugin's name — `small-business:trello`, `small-business:hubspot`
— and does not always merge it with the same product the owner already
connected to their own account. For example, an owner with Trello
attached can see both `Trello` (authorized) and `small-business:trello`
(unauthorized). Same product, same server, two entries.

**Identity is the product, not the registration.** `small-business:<name>` and
`<name>` are one connector. Rules, in order:

1. **Call whichever entry is authorized.** If both are, use the owner's own
   account-level entry: it already has consent, and it survives a plugin
   uninstall. Never call both.
2. **Two entries are not two connectors.** The "two connected in one
   category" rule above is for two vendors (two ledgers, two CRMs). Two
   registrations of one vendor never trigger the source-of-record question.
3. **An unauthorized plugin copy is not "not connected."** When the owner's
   own entry is live, the connector is connected, full stop. Do not report
   it missing, do not ask the owner to authorize the plugin's copy, do not
   send them to the Connectors tab for a tool that is already working.
4. **When only the plugin copy exists and it is unauthorized,** that is the
   ordinary "connect it" path. Say once that the owner can authorize it from
   the plugin's Connectors tab or add the connector to their account
   directly; either works, neither ranks above the other.
5. **Owner-facing text names the product.** "Trello," never
   `small-business:trello`. The business-context `Connected tools` line stores
   product names only, so a later skill never inherits a registration name.
6. **Tool-name prefixes differ.** A plugin-scoped tool is named
   `mcp__plugin_small-business_<server>__<tool>`; the owner's own is
   `mcp__<Server>__<tool>`. Anything that matches on tool names must match
   both forms.

What this rule cannot do: make Cowork show one entry. That is a platform
behaviour. Until it changes, the plugin
behaves correctly with one entry, two, or two where one is unauthorized.

---

## Onboarding and the router

- **Ask, never recommend.** Onboarding asks what the owner uses for
  bookkeeping, for customers, for mail. It does not propose a vendor. If the
  owner has no tool in a category, the recipe's zero-connector path runs and
  the category is named ("when you pick a bookkeeping tool, connect it and
  this gets deeper"), without a product name attached.
- **We have it, or we connect it, or we fall back.** In that order, said once,
  with the trade-off in one line. Never pitch a competing tool because ours
  is missing.
- **The router prefers what is connected.** Its Step 5 rules already say so.
  The neutrality rule adds: when nothing in a category is connected, the
  router names the category and the fallback, not a vendor to go and buy.

---

## What this rule does not change

- **Approval gates.** Neutral does not mean permissive. Every write still
  needs its yes.
- **Honesty about scope.** A skill built for one country's tax regime says
  so (`shared/currency-and-locale.md`). That is a scope statement, not a
  vendor ranking.

---

## Words to avoid between same-category connectors

default · primary · takes precedence · fallback (as a vendor label) · alternate
· alternative · lesser · backup path · the one most owners use · preferred

Use instead: "whichever is connected," "the connected ledger," "a ledger
(MYOB, NetSuite, QuickBooks, Xero, or Zoho Books)," "the one the owner named
as source of record."
