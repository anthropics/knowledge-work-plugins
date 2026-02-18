---
description: Generate customer-facing release notes from completed engineering work
argument-hint: "<version number or list of completed items>"
---

# Release Notes

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate customer-facing release notes from completed work.

## Workflow

### 1. Understand the Release

Ask the user:
- What version or release is this for?
- What product or product area?
- What is the release date?
- Is there a specific audience? (All customers, enterprise only, beta users)
- Any previous release notes to match the format of?

### 2. Pull Context from Connected Tools

If **~~project tracker** is connected:
- Pull all tickets completed since the last release
- Group by epic or theme for logical organization
- Identify bug fixes, new features, and improvements
- Flag any breaking changes or deprecations
- Pull ticket descriptions for context on each change

If **~~knowledge base** is connected:
- Search for related PRDs or spec documents
- Pull documentation updates that correspond to the release
- Find any migration guides or upgrade instructions

If these tools are not connected, ask the user to paste:
- List of completed Jira tickets, Linear issues, or GitHub PRs
- Brief descriptions of each change
- Any breaking changes or deprecations to flag
- Epic or theme summaries if available

### 3. Generate Release Notes

Produce customer-facing release notes. See the **release-communication** skill for detailed guidance on writing principles, changelog categorization, and audience adaptation.

- **Headline**: One compelling sentence about the most impactful change in this release
- **Highlights**: 2-3 most significant changes — the items most customers will care about
- **New Features**: New capabilities, each described in terms of what the user can now do
- **Improvements**: Enhancements to existing features — what got better and how
- **Bug Fixes**: Issues resolved, described specifically enough for affected users to recognize
- **Breaking Changes**: Anything requiring customer action, with migration guidance (if applicable)
- **Deprecations**: Features being phased out, with timeline and alternatives (if applicable)
- **Coming Soon**: Brief preview of what is next — builds anticipation and shows momentum

### 4. Follow Up

After generating the release notes:
- Offer to create a shorter version for email or social media
- Offer to create a TL;DR version for Slack
- Offer to draft a detailed blog post for major features
- Offer to adjust the tone for a different audience (technical, business, end-user)

## Output Format

Use markdown with clear headers. Lead with user value, not technical implementation details. Write in active voice and address the user directly ("You can now..." not "The ability to... has been added").

## Tips

- Translate engineering language to customer language. "Migrated to Elasticsearch" becomes "Search is now 3x faster."
- Combine related tickets into single entries. Five tickets about search improvements become one "Search Improvements" section.
- Skip internal changes with no user-visible impact (refactoring, dependency updates, CI changes).
- Breaking changes must be called out prominently — do not bury them in the middle of a list.
- Include links to documentation, guides, or help articles where relevant.
- The "Coming Soon" section is optional but powerful. It builds excitement and shows the product is actively improving.
