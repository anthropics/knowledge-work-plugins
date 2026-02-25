## Plugin submission checklist

### Type of change
<!-- Check all that apply -->
- [ ] New plugin
- [ ] New command or skill added to existing plugin
- [ ] Bug fix or correction
- [ ] Documentation update
- [ ] Other (describe below)

---

### Plugin metadata (`plugin.json`)

- [ ] `name` matches the directory name exactly
- [ ] `version` follows semver (`1.0.0` for new plugins)
- [ ] `description` is one sentence, ≤160 characters, actionable (starts with a verb)
- [ ] `author.name` is set

---

### Required files

Every plugin directory must contain:

- [ ] `.claude-plugin/plugin.json`
- [ ] `.mcp.json`
- [ ] `README.md` — includes: purpose, target persona, commands table, skills table, example workflows, MCP integration section, file structure diagram
- [ ] `CONNECTORS.md` — documents `~~category` placeholders and lists supported MCP servers per category
- [ ] `LICENSE` — copied from an existing plugin (MIT)

---

### Commands (`commands/*.md`)

Each command file must have:

- [ ] A YAML frontmatter block with at least `name` and `description`
- [ ] Clear instructions on what inputs it accepts (file, URL, pasted text, etc.)
- [ ] Graceful degradation behaviour documented when MCP tools are unavailable
- [ ] No hardcoded organization names, credentials, or personal data

---

### Skills (`skills/*/SKILL.md`)

Each skill file must have:

- [ ] YAML frontmatter with `name` and `description`
- [ ] Clear scope: what the skill does and what it explicitly does NOT do
- [ ] Escalation triggers — situations where the skill should not generate output and must instead alert the user
- [ ] No hardcoded sensitive data

---

### Quality bar

- [ ] Tested end-to-end with at least one representative input (paste test output or describe scenario below)
- [ ] `~~category` placeholders used for all tool references — no hardcoded product names in logic
- [ ] Plugin degrades gracefully when no MCP tools are connected
- [ ] Sample files added to `samples/` if the plugin handles structured documents (contracts, reports, tickets, etc.)

---

### For jurisdiction- or regulation-specific plugins (legal, finance, compliance, HR)

- [ ] Statutory or regulatory citations are accurate and versioned (e.g. "nDSG Art. 25 (in force 1 Sep 2023)", "GDPR Art. 33")
- [ ] Mandatory escalation triggers are present for situations requiring licensed professionals
- [ ] A disclaimer is included in `README.md` stating the plugin does not provide legal/financial/medical advice
- [ ] Language coverage documented if the jurisdiction is multilingual

---

### Summary
<!-- One paragraph: what does this plugin do, who is it for, and what problem does it solve? -->

### Test scenario
<!-- Describe or paste the input you tested with and the output you got -->

### Screenshots or sample output
<!-- Optional but encouraged for new plugins -->
