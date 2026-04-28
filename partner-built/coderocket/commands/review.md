---
description: View AI-powered code reviews for your pull requests
---

You are helping the user view their CodeRocket code reviews. Follow this workflow:

## Step 1 — List Reviews

Call `list_reviews` to get recent code reviews. If the user mentioned a specific repository, pass the `repository_id` parameter.

Present reviews as a list showing:
- PR title and number
- Repository name
- Status (pending/processing/completed/failed)
- Approval recommendation (if completed)
- Number of comments
- Date

## Step 2 — Show Review Details

If the user wants to see a specific review, call `get_review` with the review ID.

Organize the review output by severity:

**Critical** issues first (security vulnerabilities, bugs):
- Show file path, line number, and the comment

**Warnings** next (performance issues, potential bugs):
- Show file path, line number, and the comment

**Suggestions** (style, maintainability):
- Show file path, line number, and the comment

**Praise** last (good patterns noticed):
- Briefly mention these

## Summary

At the top of the review, show:
- Overall recommendation (approve/request changes/comment)
- Summary from the AI reviewer
- Files reviewed count
- Total comments by severity

## Notes

- Reviews are created automatically when PRs are opened (if auto-review is enabled)
- Users can configure review settings at `/repos/{id}/review-config`
- If no reviews exist, suggest the user enable auto-review on their repositories
