# Salesforce objects, fields, and activity types

The Salesforce objects and fields the `crm-autopilot` skill reads and writes,
and how it reaches them. Only the fields listed here are in scope; everything
else in the org is left alone.

**Source of these names.** Standard-object API names, plus the Headless 360
tool contract Salesforce published. Any operation name `discover` returns is
the truth over this file.

---

## How the connector works

Salesforce is reached through the Headless 360 server, which the owner adds
as a custom connector (it has a per-org address and its own OAuth client, so
it is not in the plugin manifest). It exposes four tools, and every step in
this skill is the same three-beat flow:

1. `discover` — say what you need in plain words ("find a contact by email",
   "open opportunities with no recent activity", "log a completed call").
   It returns ranked operations.
2. `describe` — the one you pick. Read its parameters and any ordered steps
   before calling. Never skip this: parameter names are the operation's,
   not this file's.
3. `dispatch_readonly` for any read; `dispatch` only for the one write the
   owner approved. `dispatch` runs as the signed-in user with that user's
   access, and there is no delete operation, which matches this skill's
   first gate.

Shape notes are in `../../../shared/connector-call-shapes.md`.

---

## Contacts — write (`Contact`)

| Field | Usage |
|---|---|
| `Email` | Primary identifier for lookup and dedupe. Always set on creation. |
| `FirstName` | From the email signature or calendar invite if available. |
| `LastName` | Required by Salesforce. From the signature or invite; if unknown, ask before creating — do not invent one. |
| `AccountId` | Set only when the company is unambiguous (an existing Account matching the email domain). Otherwise leave blank and say so. |

Do not write any other contact field. `OwnerId`, `LeadSource`, and any custom
field are user-managed.

## Contacts — read (for lookup)

| Field | Usage |
|---|---|
| `Email` | Search key. Salesforce email matching is case-insensitive. |
| `FirstName` · `LastName` · `Account.Name` | Shown to the owner during ambiguity resolution. |
| `Id` | The `WhoId` on any activity logged against this person. |

A person may exist as a `Lead` rather than a `Contact` (unconverted). Search
both by email, with `IsConverted = false` on the Lead side — a converted lead's
row persists and would otherwise match beside the Contact it became. A match
on an unconverted `Lead` is reported as a lead, and the activity is
logged with `WhoId` = the lead's `Id` **and no `WhatId`** — Salesforce
rejects an activity that names a Lead and an Opportunity together. Say the
deal is unset and that it attaches once the lead is converted.

## Opportunities — read (all cleanup and resolution paths)

| Field | Usage |
|---|---|
| `Name` | Shown to the owner; fuzzy-matched against the email subject or meeting title |
| `StageName` | Read-only during cleanup — flag discrepancies, never change |
| `Amount` | Read during cleanup; flag if a recent email or meeting implies a change |
| `CloseDate` | Read during cleanup; flag if in the past on an open opportunity |
| `NextStep` | Read, and propose updates during cleanup |
| `OwnerId` → `Owner.Name` | Shown to the owner; never changed |
| `IsClosed` | Open-pipeline filter |
| `LastActivityDate` | Stale-deal detection. Set by completed Tasks and Events; **null on a record with no logged activity ever** — treat null as the quietest deal, not as "no data" |
| `OpportunityContactRoles` (subquery) | Whether the email or meeting participants are on the opportunity. A child object, not a column: `SELECT Id, (SELECT ContactId, Role FROM OpportunityContactRoles) FROM Opportunity WHERE Id = ...` |

## Opportunities — write (cleanup path only, with approval)

| Field | Rule |
|---|---|
| `NextStep` | Proposed from the extracted next step; written only on approval |
| `CloseDate` | Proposed when the evidence names a date; written only on approval |
| `StageName`, `Amount` | **Never written by this skill.** Flag and defer; stage drives the forecast the owner reports to other people |

Never create an Opportunity unprompted. Never close one.

## Activities — write

| Activity | Object | Fields |
|---|---|---|
| Call | `Task` | `Subject`, `Description` (the summary, never the transcript), `ActivityDate` (the real date), `Status` = Completed, `TaskSubtype` = Call, `WhoId` (contact or lead), `WhatId` (opportunity) |
| Email | `Task` | Same, `TaskSubtype` = Email |
| Meeting | `Event` | `Subject`, `Description`, `StartDateTime` and `EndDateTime` (the real times), `WhoId`, `WhatId` |

`WhoId` takes a Contact or Lead `Id`; `WhatId` takes an Opportunity or Account
`Id`. Either may stand alone: a deal-only activity (`WhatId` set, no `WhoId`) is
valid, and so is a contact-only one. The single constraint is that a Lead
`WhoId` requires an empty `WhatId`. An activity with neither is orphaned and
invisible from the deal; if the deal cannot be resolved, log against the
contact and say the deal is unset.

## Association rules

- A contact joins an opportunity through `OpportunityContactRole`; propose
  adding a participant who is on the email or meeting but not on the
  opportunity, never add silently.
- A contact's company is `AccountId`. If the email domain matches exactly one
  Account, propose it; if it matches none or several, leave it blank and say
  so.

---

## What the Salesforce path cannot do here

- **Delete.** No operation exists; the skill never wanted one.
- **Arbitrary joins in one read.** SOQL covers parent lookups (contact →
  account, opportunity → account) and one level of child subquery (an
  opportunity's contact roles); anything wider is two reads, and the report
  says so.
- **Bypass the user's own access.** `dispatch` runs as the signed-in owner.
  A field they cannot edit in Salesforce cannot be edited from here either,
  and the error is reported as that, not as a plugin failure.
