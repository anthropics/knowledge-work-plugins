# CodeRocket Deploy Plugin for Claude Code and Cowork

Generate production-ready CI/CD workflows, review code, and create deploy PRs with [CodeRocket Deploy](https://deploy.coderocket.com) — powered by the CodeRocket MCP Server.

---

## What It Does

CodeRocket analyzes your repository, detects your stack, and generates a GitHub Actions workflow tailored to your language, framework, and deploy target. One command to go from zero to production.

| Skill / Command | What it does |
|---|---|
| `/coderocket:deploy` | Analyze your repo, generate a CI/CD workflow, and create a PR |
| `/coderocket:review` | View AI-powered code reviews for your pull requests |
| `/coderocket:status` | Check account status, usage, and connected repositories |

---

## Supported Stacks

- **Languages:** JavaScript/TypeScript, Python, Go, Rust, Java, Ruby, PHP, C#/.NET
- **Frameworks:** React, Next.js, Vue, Angular, Django, Flask, FastAPI, Express, Rails, Laravel, Spring Boot
- **Deploy targets:** AWS (ECS, Lambda, S3+CloudFront), Google Cloud (Cloud Run, App Engine), Azure, Vercel, Netlify, Fly.io, Railway, Render, Docker/Kubernetes

---

## Installation

### Cowork

Click the link below to install in one step:

[Install in Cowork](https://claude.ai/desktop/customize/plugins/new?marketplace=mlgraham/coderocket-plugin&plugin=coderocket)

Then restart Cowork to ensure the MCP server starts correctly.

### Claude Code

#### 1. Add this plugin's marketplace

In Claude Code, run:

```
/plugin marketplace add mlgraham/coderocket-plugin
```

#### 2. Install the plugin

```
/plugin install coderocket@coderocket-marketplace
```

#### 3. Restart Claude Code

This ensures the MCP server starts correctly.

---

## Authentication

The CodeRocket MCP server uses API key authentication:

1. Sign up at [deploy.coderocket.com](https://deploy.coderocket.com) and sign in with GitHub
2. Install the [CodeRocket Deploy GitHub App](https://github.com/apps/coderocket-deploy) on your repositories
3. Go to **Settings > API Keys** and create a new key
4. Set your API key:

```bash
export CODEROCKET_API_KEY=crk_your_key_here
```

Or add it to your `.claude/settings.json`:

```json
{
  "env": {
    "CODEROCKET_API_KEY": "crk_your_key_here"
  }
}
```

---

## MCP Tools

The CodeRocket MCP server exposes 9 tools:

| Tool | Purpose |
|---|---|
| `health_check` | Verify API connectivity and API key |
| `list_repos` | List connected repositories |
| `deploy_repo` | Analyze repo and generate CI/CD workflow |
| `create_pr` | Create a PR with the generated workflow |
| `generation_feedback` | Submit feedback on generated workflows |
| `list_reviews` | List code reviews |
| `get_review` | Get detailed review with comments |
| `account_status` | Check account tier and usage |
| `repo_details` | Get full repo analysis and history |

---

## Pricing

| Plan | Generations/mo | Repos | Price |
|---|---|---|---|
| Free | 100 | 3 | $0 |
| Pro | 1,000 | 20 | $19/mo |
| Team | 5,000 | Unlimited | $49/mo |

Visit [coderocket.com/pricing](https://coderocket.com/pricing) for details.

---

## Support

- [Documentation](https://deploy.coderocket.com/docs)
- [GitHub Issues](https://github.com/mlgraham/coderocket-plugin/issues)
- Email: support@coderocket.com

---

## License

MIT — see [LICENSE](LICENSE) for details.
