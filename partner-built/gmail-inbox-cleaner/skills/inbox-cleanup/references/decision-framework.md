# Decision Framework

Heuristics for classifying senders during the audit and review loop. These are Claude's starting positions — the user overrides everything.

The framework applies at two levels: sender-level (is this whole sender relationship noise or signal?) and email-level (within a sender, are some emails different in character?).

---

## The Carrier vs. Cargo Test

Before applying any heuristic, ask: **Is this email a carrier or cargo?**

- **Carrier** — the sender wants something from the user: attention, clicks, re-engagement, a purchase. The email exists to serve the sender's interests. → Candidate for trash/unsubscribe.
- **Cargo** — the email is delivering something the user requested or agreed to receive: a statement, receipt, alert, notice, confirmation. The email serves the user's interests. → Keep or label.

The same sender can be both. A bank that sends monthly statements (cargo) may also send promotional credit card offers (carrier). Distinguish by reading the actual subjects — never assume based on domain alone.

---

## Strong Bulk-Delete Signals

These signal the entire sender relationship is noise. Present as candidates for bulk delete without individual review.

**Sender local-part patterns** (the part before @):
```
noreply, no-reply, no_reply, donotreply, do-not-reply,
newsletter, newsletters, digest, weekly, daily, monthly,
marketing, promo, promotions, offers, deals,
notifications, notification, notify, alerts, alert,
updates, bounce, mailer, mailer-daemon,
automated, auto, robot, bot, system
```

**Sender domain infrastructure patterns** (bulk email providers with no personal relationship):
```
*.sendgrid.net
*.mailchimp.com / *.list-manage.com
*.constantcontact.com
*.klaviyo.com
*.exacttarget.com
*.marketo.com
*.hubspot.com (marketing emails — different from transactional HubSpot)
*.greenhouse.io (job application systems)
*.lever.co (recruiting platforms)
*.breezy.hr
*.smartrecruiters.com
```

**Subject line patterns** (if ALL subjects from a sender match these, it's noise):
```
% off / save X% / up to X% off
sale ends / limited time / ends tonight
exclusive offer / special offer / just for you
deal of the day / flash sale
promo code / discount code
weekly digest / monthly roundup / weekly picks
X new jobs matching / Y properties matching
someone liked / X people viewed / you have X new followers
we miss you / come back / it's been a while
```

**Category of senders that are almost always bulk-deletable:**
- Job board alerts (matching jobs, new postings from sites the user hasn't actively used)
- Real estate listing alerts (new listings, price drops from sites with no active search)
- Social notification digests (platform engagement summaries, "you have new followers")
- Inactive app re-engagement ("we haven't seen you in a while")
- Event recommendation emails (suggested events, things happening near you)
- Rewards program newsletters (points balance reminders, earning opportunities)

---

## Always-Keep Signals

Never auto-trash. Always show to user with a keep recommendation.

**Domain categories:**
- Government domains (`.gov`, `.gc.ca`, `.gov.in`, `.nic.in`, etc.)
- Financial regulators and statutory bodies
- Legal correspondence (law firms, courts)
- Healthcare providers
- Educational institutions (personal correspondence, not newsletters)
- Immigration authorities

**Sender relationship signals:**
- Any sender the user has replied to at any point (check sent mail for matching threads)
- Any sender the email address is a named individual at a company (e.g., `john.smith@company.com`)
- Any sender where subjects include personal names in the body/subject

**Subject keywords that override any other signal:**
```
invoice, receipt, confirmation, booking, itinerary,
contract, agreement, statement, notice, form,
deadline, renewal, expiry, action required,
tax, return, refund, payment due, outstanding balance,
password reset, security alert, login attempt,
visa, permit, application, approval, rejection
```

---

## Label-and-Archive Candidates

Emails worth keeping but that should live outside the main inbox. Claude should suggest label categories based on what it finds in the review — do not impose specific label names. These are patterns, not prescriptions.

**Common label categories that emerge across most inboxes:**

| Pattern | Suggested label concept | Stay in inbox? |
|---------|------------------------|---------------|
| Order/delivery confirmations from regular services | Purchases or Receipts | Usually no |
| Bank statements, brokerage reports, fund notices | Financial | Usually no |
| Building/property management, landlord notices | Housing or Property | Depends — if actionable (maintenance, fees) → yes |
| Employer, HR, payroll correspondence | Work | Usually yes — may need action |
| Government, tax authorities | Government | Usually yes — needs attention |
| Publications/newsletters the user reads actively | Reading or Newsletters | No — they choose when to read |
| Healthcare, medical providers | Health | Usually yes |

**Key question to ask the user for each proposed label:**
1. Should new emails from these senders skip your inbox, or stay visible?
2. Should they arrive unread (default) or be marked read on arrival?

Never assume mark-as-read. Some users want labeled emails to remain unread as a reminder. Always ask.

---

## Ambiguous Sender Types — Read Bodies, Not Just Subjects

These warrant round 2 (reading actual email bodies) before recommending an action:

**Financial services senders** — distinguish between:
- Statements and transaction alerts (cargo → keep)
- Promotional offers, cashback emails, credit card pitches (carrier → trash/unsub)

**SaaS product senders** — distinguish between:
- Account activity, billing receipts, security notifications (cargo → keep)
- Product updates, feature announcements, newsletters (carrier → depends on user preference)
- Re-engagement campaigns (carrier → trash/unsub)

**E-commerce platforms** — distinguish between:
- Receipts and order confirmations (cargo → label Purchases)
- Marketing ("items in your cart", "you might like") (carrier → trash/unsub)
- Shipping/delivery notifications (cargo → label Purchases or keep)

**Social platforms** — distinguish between:
- Security alerts, login notifications, account changes (cargo → keep)
- Engagement summaries, notification digests (carrier → trash/unsub)
- Messages from other users forwarded by email (cargo → depends)

---

## Mixed-Sender Handling

When a single sender has some cargo and some carrier emails, do not treat them as one block. Propose split treatment to the user:

> "This sender has 34 emails — 8 are transaction receipts from 2022-2024, 26 are promotional newsletters. I recommend keeping the receipts and trashing the newsletters. Want me to split them?"

Split by: subject keyword match, date range, or specific subject patterns. Execute each batch separately.

---

## Regulatory Senders — Cannot Unsubscribe

Some senders are legally required to contact the user and have no unsubscribe mechanism. Attempting to unsubscribe will fail. Do not include them in the unsubscribe sweep:

- Financial regulatory bodies (securities commissions, investment regulators)
- Fund registrars sending statutory investor notices
- Government tax authorities
- Immigration authorities
- Any sender whose emails reference a legal obligation or regulatory requirement

Recommend keeping these. They cannot be filtered out. Best practice: label them and let them stay visible.
