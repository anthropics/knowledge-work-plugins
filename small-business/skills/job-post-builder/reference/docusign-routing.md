# Routing the Offer Letter to DocuSign

Phase 6 only, and only when the user chose DocuSign in Phase 1.

Uses Claude in Chrome to drive the DocuSign UI, so the owner does not have to touch
DocuSign manually.

---

## The hard rule

**The envelope is saved as a draft and never sent.** Phase 6 does not advance past
"Save as draft" without the user explicitly confirming they have reviewed the envelope
and want it sent. An offer letter reaching a candidate before the owner has read it is
not recoverable.

---

## Why the browser and not the API

The DocuSign API will only accept a document from a template already in the account or
from a URL it can fetch without credentials. It does not accept file uploads. An offer
letter names a person and states their pay, so standing it up at a publicly reachable
address to satisfy the connector is not an option at any convenience.

The browser flow sidesteps this: the file is uploaded from the user's own logged-in
session, and nothing is ever published. That is why this phase is written as a UI flow.

---

## Browser flow

1. Navigate to `https://app.docusign.com`. The user should already be logged in. If a
   login screen appears, pause and ask them to log in, then continue.
2. Click **Start**, then **Send an Envelope**. Depending on the UI version this may be
   labelled **New** or **Use a Template**.
3. **Upload the offer letter.** Click "Upload Documents" and upload the
   `[Role]-Offer-Letter.docx` file created in Phase 5.
4. **Add the signer.** In Recipients, add the candidate as a signer with role "Signer".
   Ask for the candidate's name and email if not already provided.
5. **Add the sender as a CC recipient** if the user wants a copy. Ask if unsure.
6. **Set the subject line:** `Offer of Employment — [Role Title] at [Company Name]`
7. **Add a message.** A warm two-liner to the candidate by first name: pleased to extend
   the offer, review and sign when they can, questions welcome.
8. **Place signature fields.** On the document, place a Signature field and a Date Signed
   field on the candidate acceptance line at the bottom of the letter.
9. **Save as draft.** Do not send.

Then hand over the draft link and ask the user to review the signature placement and
confirm here when they are ready to send.

---

## Fallback

If DocuSign is unavailable or the browser flow fails at any step, draft an email via the
the connected mail connector (Gmail or Microsoft 365) with the offer letter attached and a note to upload it to DocuSign manually.

**Show the draft to the user before sending.** The fallback does not lower the approval
bar; it is the same gate reached a different way.

If neither path works, the `.docx` on disk is a complete outcome. Say the routing did not
happen and hand over the file.
