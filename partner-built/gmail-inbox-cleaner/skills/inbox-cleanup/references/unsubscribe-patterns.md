# Unsubscribe Patterns

Platform-by-platform methods for firing unsubscribes. Always try List-Unsubscribe header first — it's the most reliable and doesn't require HTML parsing or browser automation.

---

## Source Priority

1. **`List-Unsubscribe` header** — standard RFC 2369 header present in most bulk-sent marketing email. Parse for HTTP URLs (`<https://...>`). A GET to this URL is sufficient for most senders.

2. **`List-Unsubscribe-Post` header** — indicates one-click POST is supported (RFC 8058). POST to the List-Unsubscribe URL with body `List-Unsubscribe=One-Click`.

3. **HTML body hrefs** — when no List-Unsubscribe header exists, decode the raw HTML body (base64) and extract all `href` attributes. The unsubscribe link is typically:
   - Located near the bottom of the email
   - The last unique URL without tracking parameters (no `ext=`, `utm_`, `trk=`)
   - Often contains the words `unsubscribe`, `optout`, `opt-out`, or `manage` in the path

---

## Execution Methods

### Direct GET (Most Senders)

A simple HTTP GET to the URL is sufficient. Use `WebFetch` or Python `requests`:

```python
import requests
response = requests.get(unsubscribe_url, timeout=15, allow_redirects=True)
# Check response.text for confirmation message
```

Confirm by checking the response page text for words like "unsubscribed", "removed", "opted out".

### Button-Click Required (Loops and Similar)

**Symptom**: Navigating to the unsubscribe URL loads a page showing individual lists as "unsubscribed," but a global opt-out button is still toggled off. The GET alone does not complete the opt-out.

**Detection**: URLs matching `app.loops.so/unsubscribe`, `loops.so`, or similar. Page shows subscription status but no auto-redirect.

**Fix**: Use Claude in Chrome to navigate to the URL and click the opt-out button (e.g., "Unsubscribe from all future email"). A real browser click is required — synthetic JS events are rejected (`isTrusted: false`).

**Verification**: The button text changes to confirm opt-out (e.g., "Resubscribe" appears, indicating the opt-out is active).

### Form-Based Unsubscribes

**Symptom**: URL loads a form with a reason dropdown and a submit button. No auto-opt-out on page load.

**Fix**: Use Claude in Chrome to navigate, select a reason from the dropdown, and click Submit. The page typically navigates away after a successful submission.

**Common reason options** (select any valid one — the specific reason doesn't affect the opt-out):
- "I no longer want to receive these emails"
- "I didn't subscribe to this list"
- "Too many emails"

### One-Click POST

If `List-Unsubscribe-Post` header is present:

```python
import requests
response = requests.post(
    unsubscribe_url,
    data="List-Unsubscribe=One-Click",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=15
)
```

---

## Bulk Email Platforms — Known Patterns

| Platform | Detection | Method |
|----------|-----------|--------|
| Loops | `loops.so` in URL | Chrome button click |
| HubSpot | `hubspot.com`, `hs-email-open.hubspotemail.net` in URL | Direct GET |
| MoEngage | `moengage.com` in URL or response body | Direct GET |
| Wix | `wix.com/consent` or similar in URL | Direct GET |
| SendGrid | `sendgrid.net`, `em.` subdomain patterns | Direct GET or One-Click POST |
| Mailchimp | `list-manage.com`, `mailchi.mp` in URL | Direct GET |
| Klaviyo | `klaviyo.com` in URL | Direct GET |
| Constant Contact | `constantcontact.com` in URL | Direct GET |
| Custom forms | No matching pattern; URL loads form | Chrome form submit |

---

## What Not to Unsubscribe From

**Regulatory and legally mandated senders** — these notices are required by law and have no opt-out:
- Financial regulatory bodies and securities commissions
- Fund registrars sending statutory investor notices
- Government tax authorities
- Immigration authorities
- Any sender whose emails reference a legal obligation

**Transactional-only senders** — not marketing lists; unsubscribe links either don't exist or would disable important account alerts:
- Receipt and order confirmation senders
- Booking and reservation confirmation systems
- Bank and payment transaction alerts
- Security and account activity notifications

**Dead or erroring links** — if the URL returns 404, 5xx, or redirects to a maintenance page:
- Log as "retry later" with the URL
- Do not attempt workarounds (cache, alternative domains)

---

## Unsubscribe Log Template

Maintain a log file during the sweep:

```json
{
  "completed": [
    {"sender": "sender@domain.com", "platform": "HubSpot", "method": "GET", "status": "confirmed", "confirmation": "You have been unsubscribed"},
    {"sender": "news@service.com", "platform": "Loops", "method": "Chrome click", "status": "confirmed", "confirmation": "Button changed to Resubscribe"}
  ],
  "skipped": [
    {"sender": "notices@regulator.gov", "reason": "Regulatory — cannot opt out"},
    {"sender": "receipts@shop.com", "reason": "Transactional only — no marketing list"}
  ],
  "retry": [
    {"sender": "email@someservice.com", "reason": "URL returned 503 — site unavailable", "url": "https://..."}
  ]
}
```

Present the completed log to the user at the end of the sweep.
