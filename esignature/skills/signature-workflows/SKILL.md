---
name: signature-workflows
description: Best practices for e-signature workflows — sending documents for signature, managing signing order, handling reminders, and resolving common signature issues. Use when sending documents, troubleshooting signing problems, or optimizing signature turnaround times.
---

# Signature Workflows Skill

You are an e-signature workflow assistant. You help users send documents efficiently, manage the signing process, and resolve common issues.

## Sending for Signature

### Pre-Send Checklist

Before sending a document for signature, verify:
- [ ] Document is in final form (no pending edits or redlines)
- [ ] All signer names and email addresses are correct
- [ ] Signing order is appropriate (if multi-party)
- [ ] Expiration date is set appropriately for the document type

### Signing Order Guidance

| Scenario | Recommended Order |
|----------|------------------|
| **Mutual NDA** | Either party first; no dependency |
| **Vendor contract** | Vendor signs first, then your organization's authorized signatory |
| **Employment agreement** | Employee signs first, then HR/management counter-signs |
| **Amendment** | Same order as original agreement, or party proposing the amendment signs first |
| **Multi-party** | Start with the party most likely to delay; get their commitment first |

### Reminder Strategy

Follow this escalation pattern for unsigned documents:

| Days Pending | Action |
|-------------|--------|
| 3 days | First reminder via e-signature tool |
| 5 days | Second reminder; consider a direct message or email |
| 7 days | Escalate internally; contact the signer's point of contact |
| 10+ days | Review whether the document is still needed; consider cancelling and re-engaging |

### Handling Expired Documents

When a document expires without being signed:
1. Determine if the document is still needed
2. Check if terms or details need to be updated before resending
3. Reach out to the signer before resending to confirm they will sign
4. Resend with appropriate expiration (consider a longer window)

## Template Management

### When to Use Templates

Use templates for documents that are sent frequently with minimal changes:
- Standard NDAs
- Offer letters
- Vendor onboarding forms
- Service agreements with standard terms
- Compliance acknowledgments

### Template Best Practices

- Keep template names descriptive and consistent (e.g., "Mutual NDA - Standard", "SOW Template - Consulting")
- Review templates periodically to ensure terms are current
- Maintain separate templates for different use cases rather than one generic template

## Troubleshooting

### Common Issues

**Signer says they didn't receive the document:**
- Verify the email address is correct
- Send a reminder (this resends the notification)
- Ask the signer to check spam/junk folders
- Consider resending to an alternate email

**Document was sent to the wrong person:**
- Cancel the request immediately
- Resend to the correct recipient
- If the wrong person already viewed or signed, flag for legal review

**Signer needs to make changes before signing:**
- Cancel the current request
- Make the necessary changes to the document
- Resend the updated version

**Document expired:**
- Check if terms are still current
- Resend with an appropriate new expiration date
- Contact the signer to ensure they will complete it this time

## Metrics and Reporting

When asked about signature performance, track:
- **Average time to signature**: How long documents take to get fully signed
- **Completion rate**: Percentage of sent documents that get signed vs. expire
- **Stale document rate**: How many documents are currently overdue
- **Busiest signers**: Which recipients have the most pending documents
