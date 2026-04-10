---
name: ai-firstify
description: "Analyze, re-engineer, or bootstrap projects to align with AI-first design principles. Use when asked to review, audit, improve, 'ai-firstify', or start a new project. Performs deep analysis across 7 dimensions, actively restructures existing projects, or guides new project setup through discovery questions. Based on the 9 design principles and 7 design patterns from the TechWolf AI-First Bootcamp."
---

# AI-Firstify

Analyze and re-engineer projects to align with AI-first design principles.

## Trigger

Use this skill when asked to:
- **Audit mode** (read-only): "review", "audit", "analyze", "check", "assess"
- **Re-Engineer mode** (active changes): "ai-firstify", "fix", "improve", "re-engineer", "transform"
- **Bootstrap mode** (new project): "start", "new project", "bootstrap", "set up", "build from scratch"

## Mode 1: Audit (Read-Only Analysis)

Perform a comprehensive read-only analysis across 7 dimensions. Output a scored report with recommendations. Do NOT modify any files.

Read **references/mode-audit.md** for the full audit procedure and dimension checklist.

## Mode 2: Re-Engineer (Active Transformation)

First, perform the full audit (Mode 1). Then actively fix issues in 7 phases: foundation, de-agentification, skill extraction, complexity reduction, context hygiene, safety hardening, workflow optimization.

Read **references/mode-reengineer.md** for the full re-engineering procedure.

## Mode 3: Bootstrap (New Project Setup)

Guide the user through setting up a new AI-first project from scratch. Interactive: ask discovery questions, recommend architecture, scaffold, and test.

Read **references/mode-bootstrap.md** for the full bootstrap procedure.

## Reference Files

Domain knowledge (load on demand per dimension):

- **references/principles.md**: All 9 AI-first design principles in depth
- **references/patterns.md**: All 7 design patterns with implementation guidance
- **references/anti-patterns.md**: Common mistakes with detection patterns and fixes
- **references/skill-architecture.md**: How to structure skills, sub-agents, and workflows
- **references/project-structure.md**: Ideal project layouts, CLAUDE.md templates, .gitignore
- **references/assessment-rubric.md**: Scoring criteria and report template

Load the relevant reference file for the dimension you are currently analyzing. Do not load all references at once. Use progressive disclosure.

## Tools

- **scripts/validate-report.sh**: Validates that a generated assessment report has all required sections, dimensions, and scores
