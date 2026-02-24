---
name: real-estate/shadow-workflow
description: This skill enables independent contractors to maintain a high-leverage "Shadow Workflow" outside of corporate oversight. It provides logic for parsing Vault RE webhooks, synthesizing forwarded emails using Gemini Pro, sanitizing private drafts, and mirroring corporate tasks into private admin logs. Invoke when users mention webhooks, forwarded emails, private Workspace, or avoiding oversight.
version: 1.0.0
---

# Shadow Workflow (The Contractor's Edge)

A strategic framework for independent real estate agents to maintain data sovereignty and operational efficiency through a private tech stack. This skill enables the "Shadow Brain" that operates parallel to corporate CRM systems, ensuring the agent owns their intelligence and personal brand.

**Important**: This skill is designed for agents who control their own private Google Workspace Admin account. It focuses on the separation of personal IP from corporate data while maintaining synchronization.

## When to Use This Skill

Invoke this skill when:
- Receiving or auditing **Vault RE** webhook JSON payloads.
- Synthesizing forwarded email threads from a corporate account into a private admin account.
- Drafting client communications that need to be scrubbed of "Corporate Oversight" markers (Privacy Sanitizer).
- Mirroring CRM milestones (e.g., "Contract Signed via Secure Sign") into private Google Sheets or Tasks.
- Using **Gemini Pro** to analyze complex, multi-source client histories.
- Drafting "Shadow Marketing" content for **OpenClaw** that lives on personal profiles.

## Operational Context

| Workflow Element | Corporate Mode | Shadow Mode (Next) | Advantage |
|------------------|----------------|-------------------|-----------|
| **CRM** | Vault RE (Shared) | Private Sheet Mirror | Data Ownership |
| **Email** | RW Corporate | Private Gmail (Forwarded) | Gemini Pro Analysis |
| **Signing** | DocuSign (Audit trail) | Private Secure Sign Log | Milestone Control |
| **Marketing** | Agency Brand | **OpenClaw** Personal Brand | IP Preservation |

## Quick Reference

1. **Parse Webhook**: Analyze Vault RE JSON for property/contact updates.
2. **Synthesize Threads**: Use Gemini Pro to distill forwarded email context.
3. **Mirror Tasks**: Sync corporate milestones to your private task list.
4. **Sanitize Drafts**: Remove internal corporate jargon and tracking pixels.
5. **Brand Pulse**: Schedule personal posts via OpenClaw based on deal milestones.

## Detailed Guidance

### 1. Vault RE Webhook Parser

Process incoming JSON payloads:
- **`contact.added`**: Extract name, source, and notes. Auto-tag in private "Golden Database."
- **`property.updated`**: Detect status changes (e.g., "Appraisal" -> "Listing"). Trigger private marketing prep.
- **`user.update`**: Monitor for corporate configuration changes that might impact the shadow flow.

### 2. Email Forwarding Synthesis (Gemini Pro)

Independent agents often forward emails to a private admin account to leverage advanced AI:
- **Task**: Summarize long threads including attachments (multi-modal).
- **Cross-Reference**: Match email names against Vault RE contact IDs found in webhooks.
- **Action**: Draft replies in the private account, then copy-paste to the corporate sender.

### 3. The Privacy Sanitizer

Ensure outgoing communications don't reveal the "Shadow" setup:
- **Logic**: Strip hidden tracking pixels often added by corporate CRM mailers.
- **Tone**: Adjust language from "The Team at [Agency]" to "I" (Personal Brand focus).
- **Metadata**: Verify that PDF properties or document headers don't show "Private Admin" origins.

### 4. Task Mirroring

Maintain an invisible log of activity:
- **Trigger**: Webhook signals "Offer Received."
- **Action**: Update private Google Sheet "Deal Tracker" and create a high-priority Google Task.
- **Why**: Ensures if you lose access to the corporate CRM, your deal pipeline and client Intel remain with you.

## Documentation Requirements

- [ ] **Webhook Log**: Record of parsed JSON events.
- [ ] **Situation Report**: Gemini Pro synthesis of forwarded emails + CRM data.
- [ ] **Private Task List**: Mirrored milestones from corporate systems.
- [ ] **Sanitized Draft**: Final communication ready for delivery.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Direct API write to Vault** | High audit risk; reveals shadow tool usage | Use the "Mirror" pattern: read from Vault, act in Private. |
| **Leaving corporate sig in private mail** | Looks unprofessional/confusing | Use separate, personal-brand signatures in the admin account. |
| **Storing PII in insecure Sheets** | Regulatory risk (Privacy Act) | Use encrypted fields or private Google Cloud storage. |
| **Ignoring Webhook latency** | Data becomes stale | Manually trigger `/shadow-sync` if real-time webhooks fail. |

## When to Escalate

Escalate to your private Tech Advisor or Solicitor when:
- Corporate IT signals a crackdown on email forwarding or third-party webhooks.
- A "Conflict of Interest" arises between personal brand IP and agency contracts.
- There is a breach of your private admin account credentials.

## Privacy Considerations

- **Data Sovereignty**: The agent is the owner of the "Shadow Brain."
- **Minimized Footprint**: Do not push private data back into the corporate CRM without explicit intent.
- **Regulatory**: Ensure your shadow workflow complies with the REA Act and Privacy Act 2020.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard `contact.added` JSON payload | High | Auto-populate private log and suggest follow-up. |
| Fragmented email thread forwarded from 3 sources | Medium | Use Gemini Pro for "Deep Synthesis" and flag gaps. |
| Outgoing draft contains corporate tracking links | High | Flag for Sanitizer and propose clean version. |

## Tool Requirements

- `~~webhook listener` - Essential for real-time Vault RE integration.
- `~~cloud storage` - Private Google Workspace account.
- `~~social media` - OpenClaw for personal brand posts.

## Success Indicators

You've applied this skill well when:
- [ ] You have a complete, private mirror of your deal pipeline.
- [ ] You respond to client emails 50% faster thanks to Gemini Pro synthesis.
- [ ] Your personal brand (LinkedIn/IG) is active and deal-driven without corporate approval delays.
- [ ] Corporate management is unaware of your high-leverage private tech stack.

## Related Skills

- `~~real-estate/marketing-suite` - For personal brand content templates.
- `~~real-estate/lead-management` - For the "Hot Lead" ranking within the shadow database.
- `~~real-estate/compliance-closer` - For REA checks on private drafts.
