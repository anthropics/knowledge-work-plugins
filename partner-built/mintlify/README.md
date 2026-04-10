# Mintlify Claude plugin

A Claude Code plugin that gives Claude a comprehensive reference for building [Mintlify](https://mintlify.com) sites.

## What it does

Installs a `mintlify` skill that Claude can invoke when working on Mintlify-powered sites.

The skill covers:

- **Components** — Full syntax and props for all Mintlify components (callouts, cards, steps, tabs, accordions, code groups, fields, frames, and more)
- **Configuration** — Complete `docs.json` settings reference including theme, colors, logo, fonts, navbar, footer, redirects, integrations, and custom CSS/JS
- **Navigation** — All navigation patterns: groups, tabs, anchors, dropdowns, products, versions, and languages
- **API docs** — OpenAPI and AsyncAPI setup, endpoint pages, API playground configuration

## Installation

To install the skills in this repo:

```
npx skills add mintlify/mintlify-claude-plugin
```

To install as a Claude Code plugin:

```
/plugin marketplace add mintlify/mintlify-claude-plugin
/plugin install mintlify@mintlify-marketplace
```

## Skills included

### `mintlify`

Invoke with `/mintlify:mintlify` or let Claude use it automatically when working on Mintlify projects.

The skill loads a concise core reference and routes to detailed reference files only when the task requires them:

| Reference file | Contents |
|----------------|----------|
| `reference/components.md` | All component syntax, props, and examples |
| `reference/configuration.md` | Full `docs.json` schema and frontmatter fields |
| `reference/navigation.md` | Navigation patterns and when to use each |
| `reference/api-docs.md` | API documentation setup and playground config |

## License

MIT
