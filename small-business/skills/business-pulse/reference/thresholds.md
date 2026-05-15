# Thresholds

Red/yellow/green cutoffs for each section of the pulse. These are SMB defaults — edit them to match the owner's actual targets and plan.

Any threshold marked `# TODO: confirm with owner` should produce a note at the top of the first pulse output so the owner knows to tune it.

---

## Cash & Finance

**Cash runway**
- 🟢 ≥ 6 months  # TODO: confirm with owner
- 🟡 3–6 months
- 🔴 < 3 months

**Revenue trend (MoM)**
- 🟢 ≥ 0% (flat or growing)
- 🟡 -5% to 0%
- 🔴 < -5%

**AR aging**
- 🟢 No invoices past 31 days
- 🟡 Any invoice 31–60 days past due
- 🔴 Any invoice 60+ days past due OR total 61+ bucket > 10% of AR

**Overdue threshold**: any single invoice past due > 30 days gets named explicitly in the pulse — not just counted.

---

## Revenue & Sales

**7-day sales trend (vs. prior 7 days)**
- 🟢 ≥ 0%
- 🟡 -10% to 0%
- 🔴 < -10%

**Failed transactions**
- 🟡 Any failed transaction > $200
- 🔴 Any failed transaction > $1,000, or 3+ failures in the week

---

## Pipeline

**Pipeline coverage** (weighted pipeline ÷ monthly revenue target)  # TODO: confirm target with owner
- 🟢 ≥ 2x monthly target
- 🟡 1–2x
- 🔴 < 1x

**Stale deal**: no activity in 7+ days → flag  # TODO: owner may prefer 14 days
**Slipped deal**: open deal with close date in past → always flag

---

## Watch List

No numeric thresholds — any escalation or complaint in Gmail/Slack gets surfaced. Severity is contextual; surface and let the owner decide.

---

## Overall status rollup

The pulse-level overall status is the worst section status. Override: if any individual risk names a specific customer with a dollar amount and a deadline within 7 days, roll up to 🔴 regardless of section colors.

---

## When to tune

Revisit these after 4 weeks of use. The defaults are conservative starting points — a healthy business will feel like it's always 🟢. Tighten them to reflect where the owner actually wants to act.
