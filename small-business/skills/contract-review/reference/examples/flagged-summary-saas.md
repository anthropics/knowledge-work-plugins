# Example: SaaS vendor agreement flagged summary

A worked example of contract-review output. Contract: a SaaS subscription agreement from a mid-size software vendor.

---

## Input

> "Review this SaaS agreement before I sign. We're a 12-person consulting firm."

Contract: 18-page SaaS Subscription Agreement, vendor template, governing law: California.

---

## Output

### 📋 Contract summary

12-month SaaS subscription, auto-renewing annually. Vendor provides project management software. You pay $2,400/year billed monthly. Vendor hosts data; you own your data but grant vendor a broad license to use it for "product improvement." You can terminate with 30 days notice but owe fees through end of the contract term.

---

### 🔴 Red flags (push back before signing)

**1. Uncapped liability**

> *"IN NO EVENT SHALL VENDOR'S LIABILITY EXCEED THE AMOUNTS ACTUALLY PAID BY CUSTOMER IN THE THREE (3) MONTHS PRECEDING THE CLAIM."*

**Problem:** Three months of fees = $600. If a vendor data breach exposes your client data, your recovery is capped at $600 — regardless of actual damages. For a consulting firm handling client information, this is inadequate.

**Ask for:** Cap at 12 months of fees paid ($2,400), or at a fixed floor of $50,000 for data security incidents. Suggested language:

> *"Vendor's total liability shall not exceed the greater of (a) fees paid in the twelve (12) months preceding the claim or (b) $50,000 for claims arising from data security incidents."*

---

**2. Auto-renewal with 60-day opt-out window**

> *"This Agreement shall automatically renew for successive one-year terms unless either party provides written notice of non-renewal no less than sixty (60) days prior to the end of the then-current term."*

**Problem:** You have a 60-day window to opt out. Miss it and you're committed to another year. With a $2,400/year contract, that's easy to overlook.

**Ask for:** Reduce to 30-day opt-out, or add a reminder obligation from vendor. Alternatively, calendar the opt-out deadline now (2027-04-01 if signing May 1, 2026).

---

### 🟡 Yellow flags (negotiate if possible)

**3. Broad data license**

> *"Customer grants Vendor a non-exclusive, worldwide license to use, process, and analyze Customer Data to improve Vendor's products and services."*

**Concern:** Vendor can use your data — including client project data — to train their product. This may conflict with your client confidentiality obligations.

**Ask for:** Restrict to aggregated, anonymized usage only. Suggested language:

> *"...limited to aggregated, de-identified data and expressly excluding any Customer Data that identifies Customer's clients or projects."*

---

**4. No termination for cause cure period**

> *"Vendor may terminate this Agreement immediately upon Customer's material breach."*

**Concern:** Vendor can cut off access immediately for any "material breach" with no chance to fix it. No definition of "material." You could lose access to your data mid-project.

**Ask for:** 15-day cure period. Suggested: *"...upon written notice and Customer's failure to cure such breach within fifteen (15) days."*

---

### 🟢 Key terms to note

- **Payment:** Monthly, auto-charged. Keep credit card current or service suspends immediately.
- **Data portability:** You can export your data at any time and for 30 days post-termination. Plan export before cancellation.
- **Governing law:** California. Any disputes go to Santa Clara County courts.
- **Uptime SLA:** 99.5% monthly. Credits issued as account credits, not cash.

---

### 💡 Negotiation playbook

| Flag | Ask | Framing |
|------|-----|---------|
| Liability cap | Raise to 12 months ($2,400) or $50K for security incidents | "We handle client data — we need the liability cap to reflect actual risk" |
| Auto-renewal window | Reduce to 30 days | "60 days is tight for a small team — 30 is more typical" |
| Data license | Restrict to anonymized/aggregated | "Our client agreements restrict how we share their project data" |
| Termination cure | Add 15-day cure period | "We need a chance to fix issues before access is cut off" |

---

*This is not legal advice. For binding decisions, consult an attorney.*

---

## Redline DOCX

A redlined DOCX with these suggested changes marked in tracked-changes format was exported to: `contract-review-redline-2026-05-01.docx`
