# Personal data — what never leaves the source system

**Shared across the plugin.** Connected payroll, HR, tax, ledger, payments,
and support systems return more about a person than any deliverable needs.
The rule is the same in every skill: use a field to do the work, never
reproduce it.

---

## Never reproduced, in any output

Not in chat, not in an HTML artifact, not in a Notion or Canva page, not in a
spreadsheet, not in a CRM note, not in a draft email, not in a log line:

- Social Security numbers, individual tax IDs, and national ID numbers. A
  business EIN on a 1099 is the one designed exception.
- Dates of birth.
- Home addresses of employees and contractors. A work location is fine.
- Full card numbers, CVVs, and expiry dates. The last four digits identify a
  card; nothing more is ever needed.
- Full bank account and routing numbers, for the business or for anyone it
  pays. The last four digits or the bank name is the limit.
- Government ID and passport images or numbers, and anything from an I-9.

When a tool result carries one of these (Gusto and QuickBooks Payroll
employee payloads carry DOB, SSN flags, and home addresses; a vendor or card record carries the full
number), it is read for the step that needs it and dropped. It is not copied
into working notes, not echoed back to confirm, and not left in a rendered
page.

---

## Kept to the output that needs it

- **Per-person pay** (rate, hours, gross, net, deductions) appears only in
  payroll and tax outputs — `payroll-prep`, `plan-payroll`,
  `tax-season-organizer`, and the journal lines in `month-end-prep` — never
  in a brief, a pulse, a hiring output, or a customer-facing draft.
- **Medical, disability, leave-reason, and protected-class details** seen in
  a resume, a time-off request, or a ticket are not carried into any score,
  note, or output. `hiring-screener`'s fair-screening rules apply.
- **Customer contact details** go only where the skill's step sends them:
  the CRM of record, or the draft addressed to that customer. Never into a
  shared channel post or an artifact meant for a wider audience.

---

## When the owner asks for it anyway

Say the field is not reproduced by this plugin and point them to the source
system, where it sits under its own access controls. One line, no lecture.

---

## Skills this governs first

`payroll-prep`, `plan-payroll`, `hiring-screener`, `tax-season-organizer`,
`ap-processor`, `ticket-deflector`, and `month-end-prep`. Every
other skill applies it the moment a connector returns one of the fields
above.
