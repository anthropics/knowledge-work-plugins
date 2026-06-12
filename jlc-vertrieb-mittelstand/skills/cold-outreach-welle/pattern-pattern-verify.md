# Pattern: Email-Address Verify Before Send

A bounce kills the touch. Worse: a bounce on a generic `info@` to a group domain reveals to the recipient (if they ever see the bounced version) that the sender used a guessed address. Verify before send.

## The bounce trap pattern

| Symptom | Why it happens | Fix |
|---|---|---|
| `info@parent-group.com` bounces with "mailbox unavailable" | Group/holding domains often have no active inbox; mail is routed to subsidiaries | Find the subsidiary domain via the company imprint, send to `info@subsidiary-domain.de` |
| `info@brand.com` rejects "Recipient address rejected" | The `.com` version of a brand may not exist (only `.de`) | Check imprint for the active TLD |
| `info@subsidiary.com` returns "Unroutable address" | Domain exists, mail routing is disabled (showroom-only domain) | Find the operations-active subsidiary, e.g. `service@brand.com` |
| `info@company.de` returns "Domain does not exist" | The company has no web presence — typically a sub-50-FTE artisan operation | Drop from the wave; mark as phone-only contact |

## The 60-second verify routine

1. Open the company's **imprint / Impressum page** — by German law it lists a working contact address. Use exactly the address printed there.
2. Cross-check the **domain in the imprint** against the domain on the LinkedIn page. If they differ, the imprint wins.
3. Spot-check one MX record if there's any doubt: `dig +short MX [domain]` should return a real mail server, not `null`.
4. If the imprint lists a named role-address (`vertrieb@`, `kontakt@`), prefer that over `info@`.

## When the verified address is a named individual

If you can find the decision-maker's direct address (verified via imprint, signature on a press release, or a Sales Navigator export):

- Send to the named address **only** if you have at least one prior soft touch (LinkedIn connection, mutual contact, prior signal). A first cold mail to a personal direct address can read as overreach.
- Otherwise, send to the role-address (`vertrieb@`, `info@`) and **mention the named individual in the body** ("Herr Schmidt"). The receptionist or assistant who routes mail will forward it, which is fine and often better than the cold-direct path.

## Group-screen check (HG-4 from the wave gates)

Before sending to `subsidiary-domain.de`, verify the subsidiary is **not** a procurement-centralized arm of a >500-FTE parent. Quick check:

- Open the parent-group imprint → "About / Group structure"
- Or check the public registry / Bonität entry for the parent UID

If the parent group is large (>500 FTE / >250m revenue), the subsidiary's purchasing flows through the parent and a small consulting engagement won't survive the procurement gate. Drop from the wave; log as "group-screened".

## Anti-patterns

1. **Sending to `info@` without imprint verification** — the most common cause of bounces in Mittelstand outreach
2. **Sending to a personal address without prior touch** — reads as overreach
3. **Re-sending to the same address after a bounce** without finding the corrected one — the bounce will repeat
4. **Skipping the group screen** because the subsidiary looks small — half the bounces in our test waves came from accounts that turned out to be subsidiaries of >2000-FTE groups

## Recovery from a bounced send

If a draft is sent and bounces:

1. Find the corrected address per the routine above
2. Re-send within 24 hours from the same thread, with a one-line transparency note at the top: "Versuch Nr. 2 — Adressheilung über das Impressum"
3. Log the bounce + heal in the wave audit
4. Note the pattern in the next wave's gate-check so the same trap doesn't reappear
