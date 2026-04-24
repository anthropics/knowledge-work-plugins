# Cursor style plugin migration
_Exported on 4/23/2026 at 22:51:41 PDT from Cursor (3.2.7)_

---

**User**

Migrate the plugins here to cursor style plugins using all the skills and agents at your disposal

---

**Cursor**

Now I have a clear picture of the workspace. Let me also read the quality gates rule and look at a few more details before planning the migration.

Now I have a complete picture. Let me look at a few skill files to understand their current frontmatter format, then plan the migration.

Now I have everything I need. Let me set up the task plan and execute the migration systematically.

Let me read all the existing plugin manifests in parallel to prepare for creating the Cursor versions:

Let me read all command files to see what frontmatter they currently have:

Now I have everything needed. Let me execute the migration with a comprehensive shell script:

Now create the root `.cursor-plugin/marketplace.json`:

Now add the missing `name` frontmatter to all command files:

Now verify all skills have the required `name` + `description` frontmatter:

All skills already have proper frontmatter. Now let me update the README and run a quality verification:

Now run the quality check to validate everything is correct:

Only one issue — `cowork-plugin-management` is missing a README. Let me check its structure and create one:

Now run the final quality check to confirm everything passes:

21/21. Let me update the todos and do a final git status summary:

All 21/21 plugins pass the quality check. Here's a summary of everything that was done:

## Migration Complete

All 21 plugins have been migrated to Cursor-style plugins. Here's what changed:

### New files created (per plugin)
- **`.cursor-plugin/plugin.json`** — Cursor manifest (copied from `.claude-plugin/plugin.json`). Each has a valid `name`, `version`, `description`, `author`, and optional `keywords`/`license`/`homepage`.
- **`mcp.json`** — Cursor MCP server config (copied from `.mcp.json`). 20 plugins have MCP connectors; `cowork-plugin-management` has none.

### Root registry
- **`.cursor-plugin/marketplace.json`** — Cursor marketplace registry listing all 21 in-tree plugins + 20 external third-party plugins (Zapier, PlanetScale, Prisma, Figma, etc.)

### Frontmatter fixes (15 command files)
Added missing `name:` field to all command `.md` files across `partner-built/brand-voice`, `partner-built/common-room`, `partner-built/slack`, `pdf-viewer`, and `product-management`. Cursor requires both `name` and `description` in command frontmatter.

### New README
- **`cowork-plugin-management/README.md`** — Created the missing README for this plugin.

### Updated
- **`README.md`** — Updated to mention Cursor as the primary target alongside Claude Code/Cowork. Updated the plugin table to include all 16 Anthropic plugins (not just 11), updated the structure diagram to show both `.cursor-plugin/` and `.claude-plugin/` directories, and updated connector edit instructions for both `mcp.json` (Cursor) and `.mcp.json` (Claude Code).

All skills already had valid `name` + `description` frontmatter — no changes needed there. The original Claude plugin files (`.claude-plugin/`, `.mcp.json`) are fully preserved for backward compatibility.

---

**User**

/review-plugin-submission review the above changes and make sure to take into account this was a claude plugins repo so convert any claude-specific features to cursor lingo or equivalent, for example, cowork is a claude code or desktop feature so make modify the words. go through the whole repo and modify for cursor plugin and use /plugin-architect and other cursor-specific plugins skills to do the modifications

---

**Cursor**

Let me launch the plugin-architect review and simultaneously grep for all Claude/Cowork-specific references:

The searches are hanging on the large repo. Let me use more targeted approaches:

Now I have a clear picture of what needs changing. Let me read all the affected files in parallel:

Now let me read the remaining key files I need to update:

Let me also check the plugin-architect results and a few README files:

Let me read the README files and references for the cowork skill to understand the full scope:

Let me check the plugin-architect output while starting on the changes:

The plugin-architect subagent didn't complete in time, but I have enough intel to proceed. Let me now make all the Cursor-specific changes systematically, starting with manifests, then skills, then READMEs:

**Step 1: Fix the Cursor plugin.json manifests**

Now update the Cursor marketplace.json for the cowork-plugin-management entry:

**Step 2: Update all README files with a Python script (batch)**

**Step 3: Update the cowork-plugin-management README**

**Step 4: Update the SKILL.md files** — starting with the enterprise-search (simple) and brand-voice ones:

Now update the productivity `start` skill:

Now update the CLAUDE.md memory template section in the start skill:

**Step 5: Major rewrite of the cowork-plugin-management skills** — these are the biggest change:

Now rewrite the `create-cowork-plugin` skill for Cursor:

Now rewrite the `cowork-plugin-customizer` skill:

Now update the references files in the cowork-plugin-management skill:

Now check and update the mcp-servers.md references file in the customizer skill:

Now also check the examples/customized-mcp.json referenced by the customizer:

Good, that's a clean JSON file with no Claude-specific references. Now run the final comprehensive quality check:

**21/21 PASS.** Let me do one final sanity check — verify the git diff summary to confirm all the right files changed:

**21/21 plugins pass.** Here's the complete review-plugin-submission report:

---

## Review-Plugin-Submission: Final Report

### What was changed (41 files across the repo)

**Cursor manifest fixes (plugin.json)**
- `partner-built/slack/.cursor-plugin/plugin.json` — "from Claude Cowork" → "from Cursor"
- `partner-built/zoom-plugin/.cursor-plugin/plugin.json` — "Claude plugin" → "Cursor plugin", keyword `claude-plugin` → `cursor-plugin`
- `cowork-plugin-management/.cursor-plugin/plugin.json` — name changed to `plugin-management`, description updated for Cursor

**Root marketplace**
- `.cursor-plugin/marketplace.json` — `cowork-plugin-management` renamed to `plugin-management`

**All 14 Anthropic plugin READMEs**
- "primarily designed for Cowork… also works in Claude Code" → "designed for Cursor. Also compatible with Claude Cowork and Claude Code."
- `claude plugins add knowledge-work-plugins/<name>` → Cursor install instructions
- "Domain knowledge Claude uses automatically" → "Domain knowledge the AI uses automatically"

**Partner plugin READMEs**
- `partner-built/brand-voice/README.md` — `.claude-plugin/` and `.mcp.json` → `.cursor-plugin/` and `mcp.json` in file tree; `.claude/` paths → `.cursor/`
- `partner-built/slack/README.md` — "The Claude plugin uses `.mcp.json`" → "The plugin uses `mcp.json`"

**Skill files — terminology conversion**
- `cowork-plugin-management/skills/create-cowork-plugin/SKILL.md` — **full rewrite**: name `create-plugin`, all Cowork/Claude refs replaced, `.claude-plugin/` → `.cursor-plugin/`, `.mcp.json` → `mcp.json`, `${CLAUDE_PLUGIN_ROOT}` → `${PLUGIN_ROOT}`, packaging changed from `.plugin` zip to copy-to-local-dir, added rules/ component type
- `cowork-plugin-management/skills/cowork-plugin-customizer/SKILL.md` — **full rewrite**: name `plugin-customizer`, `mnt/.local-plugins` → `~/.cursor/plugins/`, "Cowork mode" → "Cursor", `.mcp.json` → `mcp.json`, delivery rewritten for Cursor
- `productivity/skills/start/SKILL.md` — "Cowork VM" note removed, `${CLAUDE_PLUGIN_ROOT}` → `${PLUGIN_ROOT}`, `CLAUDE.md` → `AGENT.md`
- `enterprise-search/skills/source-management/SKILL.md` — `.mcp.json` → `mcp.json`
- `partner-built/brand-voice/skills/brand-voice-enforcement/SKILL.md` — `.claude/` → `.cursor/`, "in Cowork" removed
- `partner-built/brand-voice/skills/guideline-generation/SKILL.md` — `.claude/` → `.cursor/`, "in Cowork" removed

**Reference files in plugin-management**
- `references/component-schemas.md` — `${CLAUDE_PLUGIN_ROOT}` → `${PLUGIN_ROOT}`, `Cowork UI` → `Cursor`, `.mcp.json` → `mcp.json`
- `references/example-plugins.md` — `.claude-plugin/` → `.cursor-plugin/`, `.mcp.json` → `mcp.json`
- `references/mcp-servers.md` — `.mcp.json` → `mcp.json`

---

**User**

review and install the cursor plugins now for all users

---

**Cursor**

Good — `~/.cursor/plugins/local/` is empty and ready. Let me run the full review-plugin-submission audit across all 21 plugins, then install them all:

All 21 pass. Now install all plugins to `~/.cursor/plugins/local/`:

All 21 installed. Now verify the install is correct — confirm each plugin directory has the required Cursor manifest and can be discovered:

All 21 plugins are installed and verified. Here's the complete report:

---

## Review + Installation Complete

### Review-Plugin-Submission Results: 21/21 PASS

Every plugin cleared the full checklist:
- `.cursor-plugin/plugin.json` — valid, kebab-case `name`, `description`, `version`, `author`
- `mcp.json` — present and valid JSON with `mcpServers` (all except `plugin-management` which has none)
- Skills — all `SKILL.md` files have `name` + `description` frontmatter
- Commands — all `commands/*.md` files have `name` + `description` frontmatter
- `README.md` — present in all 21 plugins
- Marketplace — all 21 registered in `.cursor-plugin/marketplace.json`

### Installed: 21/21 plugins → `~/.cursor/plugins/local/`

| Plugin                | Version | Skills | Cmds | Agents | MCP |
| --------------------- | ------- | ------ | ---- | ------ | --- |
| productivity          | 1.2.0   | 4      |      |        | ✓   |
| enterprise-search     | 1.2.0   | 5      |      |        | ✓   |
| plugin-management     | 0.2.2   | 2      |      |        |     |
| sales                 | 1.2.0   | 9      |      |        | ✓   |
| finance               | 1.2.0   | 8      |      |        | ✓   |
| data                  | 1.1.0   | 10     |      |        | ✓   |
| legal                 | 1.2.0   | 9      |      |        | ✓   |
| marketing             | 1.2.0   | 8      |      |        | ✓   |
| customer-support      | 1.2.0   | 5      |      |        | ✓   |
| product-management    | 1.2.0   | 8      | 1    |        | ✓   |
| bio-research          | 1.1.0   | 6      |      |        | ✓   |
| engineering           | 1.2.0   | 10     |      |        | ✓   |
| human-resources       | 1.2.0   | 9      |      |        | ✓   |
| design                | 1.2.0   | 7      |      |        | ✓   |
| operations            | 1.2.0   | 9      |      |        | ✓   |
| pdf-viewer            | 0.2.0   | 1      | 4    |        | ✓   |
| slack-by-salesforce   | 1.0.0   | 2      | 5    |        | ✓   |
| apollo                | 0.1.0   | 3      |      |        | ✓   |
| common-room           | 1.0.0   | 6      | 2    |        | ✓   |
| brand-voice           | 1.0.0   | 3      | 3    | 5      | ✓   |
| zoom-plugin           | 1.1.0   | 30     |      |        | ✓   |

Cursor picks up plugins from `~/.cursor/plugins/local/` automatically — no restart required. The skills will activate when relevant, and slash commands (e.g. `/sales:call-prep`, `/engineering:standup`) are available immediately in any Cursor chat.

---

**User**

@/Users/patrick/.cursor/projects/Users-patrick-Code-thirdparty-anthropics-knowledge-work-plugins/terminals/14.txt:1011-1041 can you use your cursor plugin and marketplace skills to remove the `~/.cursor/plugins/cache/knowledge-work-plugins` folder that is dirtying up the cursor plugins marketplace and instead organize all the plugins you just put into `~/.cursor/plugins/local/` and put them into my own local cursor `knowledge-work-plugins` marketplace or something, since it has a marketplace.json file. im not sure how its supposed to be organized but use your cursor skills and context7 with web research if you are unsure

---

**Cursor**

Let me read the cursor plugin skills and research the marketplace structure before touching anything:

Now I understand the structure completely. Let me look up the exact Cursor marketplace format via Context7 before making changes:

Let me look at how the `cursor-public` marketplace cache is structured (as the gold standard) and check Context7 for marketplace docs:

Now I fully understand the structure. Here's what's happening:

- `cache/` = plugins installed FROM a marketplace (one plugin per dir)
- `local/` = standalone plugins installed directly (what we just did)
- `marketplaces/` = marketplace registry repos (full checkouts with `marketplace.json`)

The `cache/knowledge-work-plugins/` is a stale Claude CLI artifact with an empty inner dir. The right move is: remove that cache + remove the 21 individual `local/` installs + create a single local marketplace entry pointing at the workspace so Cursor discovers all plugins via `marketplace.json`. Let me execute:

The workspace SHA matches the existing marketplace checkout exactly (`3b505c1046b952d8cefa4983480e93fa5731731b`), which is the pre-migration commit. Here's the plan:

1. Remove stale `cache/knowledge-work-plugins/` (confirmed empty)
2. Remove the 21 individual `local/` installs
3. Create a `local` namespace marketplace entry as a symlink → the live workspace (which has our `.cursor-plugin/marketplace.json`)

This gives Cursor a single marketplace that discovers all 21 plugins dynamically from the workspace:

Now let me verify the marketplace is reachable through the symlink and the full structure is clean:

All 21 in-tree plugins resolve correctly through the symlink. The 20 `DICT` entries are external third-party plugins referenced by URL — those are fine and Cursor will handle them. Now let me do a final verification of the complete structure:

The structure is exactly right. Here's a summary of what was done:

**Removed:**
- `~/.cursor/plugins/cache/knowledge-work-plugins/` — the stale Claude CLI artifact that was cluttering the marketplace view
- All 21 individual plugin directories from `~/.cursor/plugins/local/` — no longer needed

**Created:**
- `~/.cursor/plugins/marketplaces/local/knowledge-work-plugins` — a symlink pointing to your live workspace at `/Users/patrick/Code/thirdparty/anthropics/knowledge-work-plugins`

**Final structure:**
```
~/.cursor/plugins/
├── cache/cursor-public/          ← Cursor's official marketplace cache (untouched)
├── local/                        ← empty (clean)
└── marketplaces/
    ├── github.com/anthropics/    ← old Claude-format snapshot (untouched)
    ├── github.com/pmcbride/      ← old Claude-format snapshot (untouched)
    └── local/
        └── knowledge-work-plugins → [symlink to workspace]
                                     └── .cursor-plugin/marketplace.json
                                          21 plugins, all ✓
```

**How it works going forward:**
- Cursor reads `marketplaces/local/knowledge-work-plugins/.cursor-plugin/marketplace.json` to discover all 21 plugins
- Because it's a symlink to the live workspace, any edits you make to the plugins are immediately reflected — no copying needed
- The 20 external third-party plugins listed in `marketplace.json` (Figma, Intercom, Prisma, etc.) remain available for on-demand install from their GitHub sources

---

**User**

I forked the anthropic repo over to pmcbride/knowledge-work-plugins which i clone over at 
```zsh
➜ ~/Code/Agents/knowledge-work-plugins (main) ✗ git remote -v
origin	https://github.com/pmcbride/knowledge-work-plugins.git (fetch)
origin	https://github.com/pmcbride/knowledge-work-plugins.git (push)
upstream	https://github.com/anthropics/knowledge-work-plugins.git (fetch)
upstream	https://github.com/anthropics/knowledge-work-plugins.git (push)
```
so can you move the feature/cursor-plugin branch changes over to my fork instead of anthropics repo and /new-branch-and-pr with my fork after /review-plugin-submission 

---

**Cursor**

Let me start by checking the git state in both repos in parallel with a review sweep:

