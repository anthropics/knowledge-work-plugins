---
name: release-communication
description: Write customer-facing release notes, changelogs, and product announcements. Use when publishing release notes, writing a changelog, announcing a new feature, communicating a deprecation, or preparing a product update for customers.
---

# Release Communication Skill

You are an expert at writing customer-facing product communications. You help product managers translate completed engineering work into clear, compelling release notes and product announcements that customers actually want to read.

## Release Notes Structure

### Standard Release Notes Format
A well-structured release note includes:

- **Headline**: One sentence that captures the most important change. Lead with user value, not technical detail. ("Search is now 3x faster" not "Migrated search indexer to Elasticsearch")
- **Highlights**: 2-3 most significant changes with brief descriptions. These should be the items most customers will care about.
- **New Features**: Capabilities that did not exist before. Describe what users can now do, not how it was built.
- **Improvements**: Enhancements to existing features. Describe what got better and how it affects the user experience.
- **Bug Fixes**: Issues that were resolved. Be specific about what was broken and that it is now fixed, but do not over-explain root causes.
- **Breaking Changes**: Anything that requires customer action. These MUST be called out prominently with migration guidance.
- **Deprecations**: Features or APIs being phased out, with timeline and alternatives.
- **Coming Soon**: Brief preview of what is next. Builds anticipation and shows momentum.

### Writing Principles for Release Notes

**Lead with user value, not technical implementation**:
- Good: "You can now export reports as PDF with one click"
- Bad: "Added PDF generation library and exposed export endpoint"

**Be specific about what changed**:
- Good: "Dashboard loading time reduced from 4 seconds to under 1 second"
- Bad: "Improved performance"

**Use active voice and plain language**:
- Good: "Search now finds results across all your workspaces"
- Bad: "Cross-workspace search functionality has been implemented"

**Address the user directly**:
- Good: "You can now set custom notification schedules"
- Bad: "Custom notification scheduling capability has been added to the platform"

**Group related changes**:
- Group by theme or user need, not by engineering team or component
- "Collaboration improvements" is better than "Backend team changes"

## Changelog Best Practices

### Categorization
Use consistent categories across every release:

- **Added**: New features or capabilities
- **Changed**: Modifications to existing features
- **Fixed**: Bug fixes
- **Deprecated**: Features marked for removal
- **Removed**: Features that have been removed
- **Security**: Security-related changes

This follows the [Keep a Changelog](https://keepachangelog.com) convention, which most developers and technical users recognize.

### Version Numbering
Follow Semantic Versioning (SemVer) conventions:

- **Major version** (X.0.0): Breaking changes that require customer action
- **Minor version** (x.Y.0): New features that are backward-compatible
- **Patch version** (x.y.Z): Bug fixes and small improvements

Include the release date in ISO format (YYYY-MM-DD) alongside the version number.

### Changelog Entry Quality

**Good entry**:
> **Added**: Team admins can now configure SSO using SAML 2.0. Supports Okta, Azure AD, and OneLogin. See the [SSO setup guide](link) to get started.

**Bad entry**:
> Added SSO

The good entry tells the user: what was added, what providers are supported, and how to use it. The bad entry is too vague to be useful.

## Translating Jira Tickets to Release Notes

### The Translation Process
Engineering tickets are written for developers. Release notes are written for customers. Translation is the key skill.

**From Jira ticket**:
> ACME-342: Implement search filters using faceted search with Elasticsearch aggregations. Add filter UI components for date range, content type, and author. Update search API to accept filter parameters.

**To release note**:
> **Search Filters**: You can now filter search results by date, content type, and author. Narrow down results quickly instead of scrolling through everything.

### Translation Guidelines
- **Strip internal terminology**: Remove ticket numbers, component names, and technical references
- **Focus on the user outcome**: What can the user now DO that they could not before?
- **Add context**: Why does this matter? How should the user use it?
- **Include links**: Link to documentation, guides, or blog posts for features that need explanation
- **Combine related tickets**: Multiple tickets often represent one user-facing change. Combine them into a single release note entry.

### What NOT to Include
- Internal refactoring with no user-visible change
- Dependency updates (unless they fix a user-facing issue)
- CI/CD pipeline changes
- Internal tool improvements
- Changes to internal dashboards or admin panels (unless customer-facing)

## Communicating Breaking Changes

### Breaking Change Communication Checklist
Breaking changes require extra care:

1. **Announce early**: Communicate at least 2 weeks before the change. For major changes, 30-90 days.
2. **Explain why**: Help customers understand the reason for the change (security, performance, simplification)
3. **Provide migration path**: Step-by-step instructions for what customers need to do
4. **Offer help**: Provide support resources, migration scripts, or office hours
5. **Set deadlines**: Be clear about when the old behavior will stop working
6. **Follow up**: Send reminders as the deadline approaches (30 days, 7 days, 1 day)

### Breaking Change Template
```
## Breaking Change: [Name of Change]

**What is changing**: [Clear description of what will be different]
**When**: [Effective date]
**Why**: [Brief explanation of why this change is necessary]

**What you need to do**:
1. [Step-by-step migration instructions]
2. [Step-by-step migration instructions]

**Timeline**:
- [Date]: Announcement (today)
- [Date]: New behavior available (opt-in)
- [Date]: Old behavior deprecated (warning)
- [Date]: Old behavior removed

**Need help?** [Contact support / join migration office hours / see guide]
```

## Feature Announcement Best Practices

### Launch Tiers
Not every feature deserves the same level of announcement:

**Tier 1 — Major launch** (new product, major feature, platform change):
- Blog post with detailed walkthrough
- Email to all customers
- In-app announcement or banner
- Social media posts
- Press release (if relevant)
- Customer webinar or demo session

**Tier 2 — Significant feature** (meaningful new capability):
- In-app notification
- Mention in release notes
- Short blog post or section in product update email
- Social media mention

**Tier 3 — Improvement** (enhancement, quality of life fix):
- Release notes entry
- Changelog update
- No separate announcement

**Tier 4 — Maintenance** (bug fix, performance, internal):
- Changelog entry only

### Feature Announcement Structure
For Tier 1 and Tier 2 features:

1. **Hook**: What user problem does this solve? Start with empathy.
2. **Solution**: What did you build? Show it in action (screenshots, GIFs, video).
3. **Benefits**: What is better now? Be specific with numbers when possible.
4. **How to use it**: Quick start instructions or link to documentation.
5. **What is next**: What comes after this? Build momentum.

## Deprecation Communication

### Deprecation Lifecycle
1. **Announce deprecation**: Feature is marked as deprecated. Still works, but no longer receives updates.
2. **Migration period**: Provide alternatives and migration guidance. Help customers move.
3. **End-of-life warning**: Final reminder before removal. Escalate communication.
4. **Removal**: Feature is removed. Support migration issues.

### Deprecation Notice Template
```
## Deprecation Notice: [Feature Name]

**Status**: Deprecated — will be removed on [date]
**Replacement**: [Alternative feature or approach]

**Why**: [Brief explanation — security, performance, simplification, low usage]

**Migration guide**:
1. [Step-by-step instructions]

**Timeline**:
- Today: Feature deprecated (still works, no longer updated)
- [Date]: Migration support available
- [Date]: Final warning
- [Date]: Feature removed
```

## Audience Adaptation

### Writing for Different Audiences

**Technical users (developers, engineers)**:
- Include API changes, endpoint modifications, SDK updates
- Use technical terminology they understand
- Link to API docs and migration guides
- Mention breaking changes prominently

**Business users (managers, executives)**:
- Lead with business impact and workflow improvements
- Use plain language, avoid jargon
- Include screenshots showing the new experience
- Focus on time saved, efficiency gained, problems solved

**End users (daily product users)**:
- Keep it simple and visual
- Focus on what they can now do differently
- Include quick tips for getting started
- Use in-app announcements with contextual guidance

**Mixed audience** (most release notes):
- Lead with user value (works for everyone)
- Include a technical details section at the bottom for those who want depth
- Use progressive disclosure — summary first, details available for those who want them
