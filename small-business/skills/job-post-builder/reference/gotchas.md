# Gotchas

## 1. DocuSign login state

✗ **Bad:** Claude navigates to `https://app.docusign.com` and immediately tries
to upload the offer letter without checking whether the user is logged in.

✓ **Good:** Immediately after navigating to DocuSign, check for a login screen.
If a login prompt appears, pause and ask the user to log in, then wait for
confirmation before continuing.

**Why it matters:** DocuSign redirects unauthenticated sessions silently. If the
login check is skipped, the automation tries to click UI elements that don't exist
and fails mid-flow with no clear error.

---

## 2. Missing candidate details before entering the browser

✗ **Bad:** Claude reaches Phase 6, opens DocuSign in Chrome, and then asks mid-flow:
"What's the candidate's email address?"

✓ **Good:** If the user chose DocuSign delivery in Phase 1, collect the candidate's
full name and email address before Phase 6 begins — either in Phase 1 or at the
end of Phase 5. Never enter the browser flow without both fields.

**Why it matters:** Interrupting an open browser session to collect missing data
disrupts the automation state and confuses the user.

---

## 3. Re-asking for context the user already provided

✗ **Bad:** The user says "we need to hire a senior PM, fully remote, $160–180k"
and Phase 1 asks for role title, location, and compensation anyway.

✓ **Good:** Extract role title, location, and compensation from the message, confirm
them in a single sentence, and ask only for the fields that are genuinely missing.

**Why it matters:** The skill explicitly requires "one focused clarifying question
rather than a long form." Redundant questions break trust and slow the workflow.

---

## 4. Silently expanding the user's existing format

✗ **Bad:** The user has a 3-section job post on file. Claude produces a 7-section
post based on `references/job-post-structure.md` without asking.

✓ **Good:** Map the user's existing format against the reference, identify missing
sections, and ask one question: "Your existing JD has X and Y — want me to add Z,
or keep your current format?"

**Why it matters:** The user's format is the source of truth. Overriding it silently
may conflict with internal HR or legal standards the user hasn't mentioned.

---

## 5. Inventing compensation figures

✗ **Bad:** No salary range was provided, so Claude writes "$120,000–$150,000 DOE"
in the job post or offer letter.

✓ **Good:** If compensation isn't provided, omit the range from the job post entirely.
In the offer letter, use `[ANNUAL SALARY — confirm with HR]` as a bracketed placeholder.

**Why it matters:** Inventing compensation figures creates legal and HR liability.
The skill's instructions are explicit: "Don't invent a range."
