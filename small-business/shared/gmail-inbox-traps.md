# Gmail inbox traps

Three things that will make a mail-reading skill report confidently wrong — or
leak something it should not.

---

## Trap 1 — a label query by ID silently returns nothing

The Gmail connector's own documentation says label search takes label **IDs**,
not display names, and points at `list_labels` to fetch them. Following that
instruction returns an empty result.

Same inbox, same moment:

| Query | Threads returned |
|---|---|
| `label:Label_2` (the ID for "Leads") | **0** |
| `label:Leads` (the display name) | **201** |

`list_labels` reports the label holds 219 messages, so the label is real and
populated. The ID form just matches nothing, and it fails the worst possible
way: no error, no warning, an empty list that reads exactly like an empty label.
A skill doing the documented thing concludes there are no leads and says so.

**The rule.** Query labels by **display name** — `label:Leads`, `label:AP`,
`label:Support`. Use `list_labels` to confirm the label exists and how many
messages it holds, then search by its name. Multi-word names take quotes:
`label:"Client work"`.

**Always cross-check an empty result.** If a label search returns nothing but
`list_labels` says the label has messages, the query is wrong, not the inbox.
Never report "no messages" on the strength of a single empty label search.

## Trap 2 — the inbox is mostly machines, in two layers

Excluding the obvious storefront sender is not enough. In one inbox, of
201 inbound threads in fourteen days:

- **layer one** — storefront and processor mail: order placed, payment
  received, payout sent, refund issued
- **layer two** — everything left after filtering layer one was *still* noise:
  SaaS onboarding drips, product newsletters, ad-credit promotions, sign-in
  notifications, one-time password mail

Human correspondence was zero in that window. The real inquiries were all sitting
under the `Leads` label, not loose in the inbox.

**The rule.** Filter both layers before counting anything as inbound human mail:
storefront and processor senders, then bulk and transactional senders —
`no-reply`, `noreply`, `notifications@`, `store+`, `learn@`, `ads-`, and the
like. If nothing survives, the honest answer is zero, reported plainly. Never
present a raw thread count as inquiry volume.

## Trap 3 — never reproduce an authentication code

A live inbox contains authentication material. For example:

> *"Use the following one-time password (OTP) to sign in to your Zoho account.
> This OTP will be valid for 15 minutes… 0000000"*

Digests, morning briefs and triage summaries quote subjects and snippets. Any of
them would carry that code out of the inbox — into a chat transcript, a saved
file, or a Slack channel other people can read. A one-time code in a shared
channel is an account takeover waiting for someone to notice.

**The rule.** Authentication material never leaves the inbox. This covers
one-time passwords, verification and security codes, password-reset links,
magic sign-in links, API keys and tokens, and multi-factor prompts.

Classify these as handled and count them. Never quote the subject, never quote
the snippet, never include the body, never follow or reproduce the link. If one
must be named at all, name it by category alone:

```
Handled (14) — 6 newsletters, 5 platform notices, 3 sign-in and security codes
```

**This hardens as the output travels.** A code in the chat is bad; a code in a
Slack post or a saved document is worse, because it outlives the conversation
and reaches people who were never in it. Outward writes get the strictest
reading of this rule.

Related: the same instinct applies to a payment-detail change email, which is
the wire-fraud case handled separately in `inbox-manager` — surface that one
loudly, undrafted, rather than suppressing it. The difference is that a
fraudulent wire request is something the owner must *see*; an OTP is something
nobody but the owner should see. Loud versus silent, both deliberate.
