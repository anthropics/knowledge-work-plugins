# Intake and Extraction

How bills get in, and how the fields come out.

---

## Where bills come from

**Ranked by how clean the data arrives.**

| Source | What you get | Watch for |
|---|---|---|
| Mail AP label or folder (Gmail or Microsoft 365), or `bills@` alias | PDF attachment plus sender context | Vendors who put the invoice in the message body with no attachment |
| Vendor portal notification email | A link, not a document | The email alone is not a bill. Ask the owner to download it or forward the PDF |
| Uploaded PDF | Clean text extraction | Scanned PDFs are images — treat as photos |
| Phone photo of paper | Whatever the light allowed | Glare, crop, and skew. Low-confidence fields are the norm here, not the exception |
| Ramp / Expensify feed | Card charge with merchant and amount | Not a bill. It is already paid. Never stage it into a payment run |
| Vendor statement | A list of open invoices | A statement is a reconciliation tool, not a bill. Use it to find missing invoices, never to create entries |

**Set up the inbox once.** If the owner has no AP label, offer to create one and give them a forwarding address to use with vendors. That single change removes most of the manual work permanently.

---

## Extraction fields

Pull every one of these for each bill. Empty is a valid value; invented is not.

- Vendor name, as printed, plus the matched vendor record in the ledger
- Invoice number
- Invoice date
- Due date, or terms if only terms are printed
- Subtotal, tax, freight or delivery, total
- PO number
- Line items: description, quantity, unit price, extended amount
- Remit-to details, when they differ from the vendor on file. A difference is a flag for the owner to verify by phone on the number already on file, never a reason to update the vendor record from the bill (`../../../shared/untrusted-content.md`)

### Confidence

Tag every field high, medium, or low.

- **High** — machine-readable text, or a number that foots against the lines
- **Medium** — read from an image but internally consistent
- **Low** — glare, cropping, handwriting, or a total that does not foot

Low-confidence money fields are surfaced by vendor and invoice number and are never used to build a payment run until the owner confirms them.

### Footing check

Lines plus tax plus freight should equal the total. When it doesn't, say so with both figures. That mismatch usually means a line was cropped out of a photo, which is exactly the case where a plausible-looking guess does the most damage.

---

## Dedupe

Run before coding. A bill is a likely duplicate when **any** of these hold:

1. Same vendor and same invoice number. This is a duplicate, full stop.
2. Same vendor, same total, invoice dates within 5 days, no invoice number on one copy.
3. Same vendor and total already staged or paid in the ledger in the last 90 days.

Present suspected duplicates as pairs with both sources named ("emailed 3/2 as PDF, also on the March statement"). The owner decides. Some vendors legitimately bill identical amounts monthly, so the check surfaces, it does not delete.

---

## Vendor matching

Match the printed vendor name to the ledger record before coding. Handle the common noise: `ACME SUPPLY CO`, `Acme Supply`, and `ACME SUPPLY #4412` are usually one vendor.

When no ledger record exists, propose creating one with the remit-to details from the bill and ask. Bank or remit-to details on a first bill are confirmed by phone on a number the owner sources themselves, not from the bill, before the record is created (`../../../shared/untrusted-content.md`). A vendor created by mistake is a cleanup job for the bookkeeper later.

---

## Worked example

Okonkwo Mechanical's AP label held 23 messages over two weeks. After intake:

- 19 bills extracted, 2 vendor-portal links with no document, 2 statements
- 1 duplicate found: Ferguson invoice 88231 arrived as a PDF and again on the monthly statement
- 3 low-confidence totals, all photos taken in the truck
- 1 bill with no due date printed, terms line read "Net 30"

Reported to Ray as: 19 bills, USD 41,208 readable, 3 totals need his eyes, 2 portal invoices he has to download, 1 likely duplicate to confirm.
