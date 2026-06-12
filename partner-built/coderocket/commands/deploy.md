---
description: Generate a CI/CD workflow for your project and create a GitHub PR
---

You are helping the user deploy their project using CodeRocket Deploy. Follow this workflow:

## Step 1 — Check Connectivity

Call the `health_check` tool to verify the CodeRocket API is reachable and the API key is configured.

If the health check fails due to a missing API key, tell the user:
> To use CodeRocket Deploy, you need an API key:
> 1. Sign up at https://deploy.coderocket.com
> 2. Install the GitHub App on your repositories
> 3. Go to Settings > API Keys and create a key
> 4. Set it in your environment: `export CODEROCKET_API_KEY=crk_...`

## Step 2 — List Repositories

Call `list_repos` to show the user their connected repositories. Present them as a numbered list showing:
- Repository name
- Analysis status
- Primary language/framework (if analyzed)

Ask the user which repository they want to deploy.

## Step 3 — Generate Workflow

Call `deploy_repo` with the selected repository ID and any deploy target preference. This will:
- Analyze the repository (if not already analyzed)
- Generate a CI/CD workflow using AI
- Return the YAML and an explanation

Show the user:
1. A brief summary of what was detected (language, framework, deploy target)
2. The generated workflow YAML in a code block
3. The AI's explanation of what the workflow does

## Step 4 — Confirm and Create PR

Ask the user if they want to create a PR with this workflow. If yes, call `create_pr` with the generation ID.

Show the PR URL so they can review and merge it.

## Step 5 — Collect Feedback

After the user has had a chance to try the workflow, ask how it went and call `generation_feedback` with their response (worked/partial/failed).

## Notes

- If the user specifies a deploy target (e.g., "deploy to AWS", "deploy to Vercel"), pass it as the `deploy_target` parameter
- If analysis is already complete, the `deploy_repo` tool will skip re-analysis
- The full flow typically takes 30-60 seconds
