# piia-engram

**Persistent personal memory across tools and chats.** Profile, preferences, lessons, and decisions live as local JSON — every AI tool and every new conversation reads the same memory. AI proposes; you approve what becomes permanent. Local-first, no cloud, no account.

For knowledge workers: stop re-explaining who you are every time you open a new chat or switch between Claude Cowork, Claude Code, and other MCP clients. piia-engram keeps your role, working style, communication preferences, and accumulated lessons in one place, accessible to every AI tool you use.

## What it does

- **Cross-tool**: same identity & knowledge accessed from Claude Cowork, Claude Code, Cursor, Codex, Windsurf, or any MCP client.
- **Cross-chat**: every new conversation auto-loads your resume brief (identity card + recent decisions + today's daily log) via a SessionStart hook.
- **User-approved**: AI-proposed knowledge lands in a `staging` tier and only becomes `verified` when you explicitly approve it — no silent hallucination drift.
- **Local-first**: all data lives in `~/.engram/` as human-readable JSON. No cloud, no account, no lock-in.

## Install

The MCP server runs via `uvx`, so no separate install step is required after the plugin loads. If you prefer to install ahead of time:

```bash
pip install piia-engram
engram setup
```

After install, every supported AI tool (Claude Cowork, Claude Code, etc.) automatically picks up the same memory store at `~/.engram/`.

## Links

- Main repository: https://github.com/Patdolitse/piia-engram
- PyPI: https://pypi.org/project/piia-engram/
- Documentation: https://github.com/Patdolitse/piia-engram#readme
- Privacy: https://github.com/Patdolitse/piia-engram/blob/main/PRIVACY.md
- Security: https://github.com/Patdolitse/piia-engram/blob/main/SECURITY.md

## License

Apache-2.0
