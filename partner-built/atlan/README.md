# Atlan Agent Toolkit

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
[![PyPI - Version](https://img.shields.io/pypi/v/atlan-mcp-server.svg)](https://pypi.org/project/atlan-mcp-server)
[![License](https://img.shields.io/github/license/atlanhq/agent-toolkit.svg)](https://github.com/atlanhq/agent-toolkit/blob/main/LICENSE)


This repository contains a collection of tools and protocols for interacting with Atlan services for AI agents. Each component is designed to provide specific functionality and can be used independently or together.

## Components

### Model Context Protocol (MCP)

An MCP server that enables interaction with Atlan services through tool calling. Provides tools for asset search, and retrieval using [pyatlan](https://developer.atlan.com/sdks/python/).

You can find the documentation and setup instructions for the MCP server [here](modelcontextprotocol/README.md).

### Claude Code Plugin

The official Atlan plugin for Claude Code. Search, explore, govern, and manage your data assets through natural language, powered by the Atlan MCP server.

Connects to Atlan via OAuth at `mcp.atlan.com/mcp` - no API keys required.

**Features:**
- 15 MCP tools (12 enabled by default, 3 via feature flags)
- **Search**: AI-powered semantic search across data assets
- **Lineage**: Trace data flow upstream and downstream
- **Governance**: Manage glossaries, terms, certifications
- **Data Quality**: Create and schedule validation rules
- **Data Mesh**: Organize domains and data products

**Setup:**
```bash
# Install from marketplace (when available)
/plugin marketplace add atlanhq/agent-toolkit
/plugin install atlan@atlan-marketplace

# Or test locally
claude --plugin-dir ./claude-plugin
```

For detailed plugin documentation, see [claude-plugin/README.md](claude-plugin/README.md).


## 🔍 DeepWiki: Ask Questions About This Project

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/atlanhq/agent-toolkit)


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to the Atlan Agent Toolkit.


## License

The project is licensed under the [MIT License](LICENSE). Please see the [LICENSE](LICENSE) file for details.
