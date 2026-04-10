# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2026-02-17

### Fixed
- Eliminated multi-stage builder and venv from Dockerfile, now installing directly to system python using uv, removing the broken symlink workaround from #206
- Eliminated bundled pip/setuptools/wheel and their vendored dependencies which carried 2 HIGH vulnerabilities:
  - jaraco.context 5.3.0 (CVE-2026-23949)
  - wheel 0.45.1 (CVE-2026-24049)

### Security
- Trivy scan: 0 HIGH/CRITICAL vulnerabilities on the resulting Docker image
- The pyatlan base image already provides pyatlan, pydantic, httpx, cryptography, authlib, h11, anyio, and other common packages at the system level
- Only MCP-specific packages (fastmcp, uvicorn, and their transitive deps) are now installed on top

## [0.3.2] - 2026-02-13

### Fixed
- Dockerfile builder using Python 3.12 while pyatlan runtime image uses 3.11, causing ABI incompatibility for compiled C extensions
- Broken venv python symlink after multi-stage COPY — builder path `/usr/local/bin/python` does not exist in pyatlan runtime, causing `ModuleNotFoundError` at container startup

### Changed
- Upgraded `fastmcp` from 2.13.2 to >=2.14.0 (resolved to 2.14.5)
- Removed deprecated `dependencies` constructor argument from `FastMCP()` init, added `fastmcp.json` for dependency metadata
- Constrained transitive dependencies to remediate HIGH/CRITICAL vulnerabilities:
  - `authlib>=1.6.6`, `cryptography>=46.0.5`, `h11>=0.16.0`
  - `python-multipart>=0.0.22`, `starlette>=0.49.1`, `urllib3>=2.6.3`

## [0.3.1] - 2025-12-17

### Added
- Data quality rule management tools:
  - `update_dq_rules`
  - `schedule_dq_rules`
  - `delete_dq_rules`
- Extended asset support for `create_dq_rules` to View, MaterialisedView, and SnowflakeDynamicTable
- DockerHub as an additional container registry alongside GHCR

### Changed
- Upgraded FastMCP dependency from 2.13.0.2 to 2.13.2

## [0.3.0] - 2025-12-03
- Added new tools:
  - `create_data_domain_assets`
  - `create_data_product_assets`
  - `create_dq_rules`

## [0.2.12] - 2025-11-14

### Changed
- Added explicit uvicorn>=0.35.0 dependency to ensure compatibility with FastMCP 2.13.0.2

## [0.2.11] - 2025-11-07

### Changed
- Upgraded FastMCP dependency from 2.11.0 to 2.13.0.2

## [0.2.10] - 2025-10-13

### Fixed
- Fixed a bug in `update_assets_tool` where glossary terms and categories could not be updated because the glossary GUID parameter was not being sent - now properly includes the glossary GUID as a required parameter for these asset types

## [0.2.9] - 2025-09-22

### Fixed
- Transport configuration not working when installed via PyPI and executed using `uvx atlan-mcp-server` - server would ignore environment variables and command-line arguments, always defaulting to stdio mode

## [0.2.8] - 2025-09-15

### Added
- Term linking functionality for improved glossary term relationships (#138)
- Enhanced search tool with popularity attributes context and examples (#132)
- Comprehensive MCP transport mode documentation (#124)

### Changed
- Implemented client singleton pattern for improved connection pool reuse and performance (#131)
- Enhanced Docker configuration with improved .dockerignore settings (#127)

## [0.2.7] - 2025-09-02

### Added
- Configurable tool access control via `RESTRICTED_TOOLS` environment variable
- Organizations can now restrict any combination of tools for MCP clients


## [0.2.6] - 2025-08-19

### Added
- Glossary management tools to streamline glossary creation and management:
  - `create_glossaries`: Create top-level glossaries with metadata (name, `user_description`, optional `certificate_status`)
  - `create_glossary_terms`: Add individual terms to an existing glossary; supports `user_description`, optional `certificate_status`, and `category_guids`
  - `create_glossary_categories`: Add categories (and nested subcategories) anchored to a glossary or parent category; supports `user_description` and optional `certificate_status`
- Bulk creation support across glossaries, terms, and categories to enable scalable glossary builds
- Foundation for automated, structured glossary generation from unstructured content


## [0.2.5] - 2025-08-05

### Changed
- Enhanced `search_assets_tool` documentation and usage examples for `connection_qualified_name` parameter
- Added `connection_qualified_name` parameter to example function calls for missing descriptions and multiple asset types searches

## [0.2.4] - 2025-07-24

### Added
- Enhanced lineage traversal tool with configurable attribute inclusion support
- `include_attributes` parameter in `traverse_lineage_tool` allowing users to specify additional attributes beyond defaults
- Default attributes are now always included: name, display_name, description, qualified_name, user_description, certificate_status, owner_users, owner_groups, connector_name, has_lineage, source_created_at, source_updated_at, readme, asset_tags

### Changed
- Improved lineage tool return format to standardized dictionary structure with `assets` and `error` keys
- Enhanced lineage processing using Pydantic serialization with `dict(by_alias=True, exclude_unset=True)` for consistent API responses
- Updated `immediate_neighbors` default value from `True` to `False` to align with underlying FluentLineage behavior
- Better error handling and logging throughout lineage traversal operations

### Fixed
- Lineage tool now returns richer attribute information instead of just default minimal attributes
- Resolved issue where lineage results only contained basic metadata without requested additional attributes

## [0.2.3] - 2025-07-16

### Added
- Expanded docstring attributes for LLM context in `server.py` for improved clarity and developer experience

### Changed
- Major documentation and README refactoring for easier setup and integration with Claude Desktop and Cursor, including clearer configuration examples and troubleshooting guidance

### Fixed
- Made `ATLAN_MCP_USER_AGENT` dynamic in `settings.py` to always reflect the current MCP server version in API requests

## [0.2.2] - 2025-06-23

### Added
- Multi-architecture build support for Docker images (ARM64 and AMD64)
- README support for asset updates - allows updating asset documentation/readme using markdown content
- Enhanced parameter parsing utilities for better Claude Desktop integration

### Fixed
- Search and Update Assets Tool compatibility issues with Claude Desktop
- String input parsing from Claude Desktop for better tool interaction
- Parameter validation and error handling improvements

### Changed
- Upgraded FastMCP dependency version for improved performance and stability
- Enhanced tool parameter processing with better error handling
- Improved asset update functionality with support for README content management

## [0.2.1] - 2025-05-24

### Added
- Advanced search operators support in `search_assets` including `contains`, `between`, and case-insensitive comparisons
- Default attributes for search results via `DEFAULT_SEARCH_ATTRIBUTES` constant with dynamic user-specified attribute support
- Enhanced "some conditions" handling with support for advanced operators and case-insensitive logic
- New search examples demonstrating OR logic for multiple type names and glossary term searches by specific attributes

### Changed
- Integrated `SearchUtils` for centralized and consistent search result processing
- Improved search API flexibility and precision with advanced query capabilities

### Fixed
- Release workflow changelog generation issues that previously caused empty release notes
- Improved commit range calculation and error handling in GitHub Actions workflow

## [0.2.0] - 2025-05-17

### Added
- Support for new transport modes: streamable HTTP and SSE
- MCP server executable script (`atlan-mcp-server`)
- Improved Docker image with non-root user and security enhancements

### Changed
- Made MCP server an installable package
- Updated dependencies and bumped versions
- Improved build process for faster Docker builds
- Restructured release workflow for better isolation and PR-based releases

### Fixed
- Various minor bugs and stability issues

### Documentation
- Updated setup and usage instructions
- Added more comprehensive examples


## [0.1.0] - 2024-05-05

### Added
- Initial release of Atlan MCP Server
- Basic functionality for integrating with Atlan
