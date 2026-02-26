# Development Workflow

## Branch Strategy

- `main` - Production-ready plugins
- Feature branches for new work

## Development Process

### 1. Plugin Development
1. Create/modify plugin files
2. Test locally with Claude Code
3. Update documentation
4. Submit PR

### 2. Quality Checks
- Verify plugin.json schema
- Test all commands
- Validate skill instructions
- Check markdown formatting
- Run Conductor track validator: `python conductor/scripts/validate_tracks.py`

### 3. Review Process
- Peer review for content accuracy
- Verify connector configurations
- Test installation flow

## Testing

### Local Testing
```bash
claude plugin install ./path/to/plugin
python conductor/scripts/validate_tracks.py
```

### Pre-commit Setup
```bash
pip install pre-commit
pre-commit install
```

### Command Testing
Run commands in Claude Code session to verify behavior.

## Release

1. Merge to main
2. Tag release version
3. Update marketplace

## Contribution Guidelines

- Fork repo
- Make changes
- Submit PR with description of changes
- Address review feedback
