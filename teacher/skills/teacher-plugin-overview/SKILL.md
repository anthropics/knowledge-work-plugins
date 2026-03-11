---
name: teacher-plugin-overview
description: >
  Guide users through the teacher plugin features, commands, and best practices.
  Use when users ask about what the teacher plugin can do, how to use commands, or need help with teaching workflows.
---

# Teacher Plugin Overview

Welcome to the Teacher Plugin! This skill provides a quick tour of what this plugin offers and how to get the most out of it.

## What This Plugin Does

This plugin helps educators:

- **Plan lessons** - Create comprehensive, standards-aligned lesson plans
- **Create assessments** - Generate quizzes, tests, and assignments with answer keys
- **Provide feedback** - Give specific, actionable feedback on student work
- **Manage classroom** - Develop norms, routines, and behavior plans
- **Communicate with families** - Draft professional messages to parents and guardians

## Available Commands

| Command | What It Does |
|---------|-------------|
| `/lesson-plan` | Create a lesson plan with objectives, activities, and assessments |
| `/assessment` | Create quizzes, tests, or assignments with answer keys |
| `/feedback` | Provide detailed feedback on student work |
| `/classroom-management` | Create classroom norms and behavior intervention plans |
| `/parent-communication` | Draft messages to families |

## How to Use Commands

Each command accepts arguments to customize the output:

```
/lesson-plan <topic> <grade/level> <duration>
/assessment <topic> <type> <number>
/feedback <student work or description>
/classroom-management <grade level> <context>
/parent-communication <type> <audience> <details>
```

Examples:
- `/lesson-plan photosynthesis 7th-grade 45-minutes`
- `/assessment fractions multiple-choice 10`
- `/feedback [paste essay]`
- `/classroom-management middle-school online`
- `/parent-communication celebration elementary "Student excelled in science project"`

## Getting Started

1. **Try a command** - Start with `/lesson-plan` to create your first lesson
2. **Connect tools** - Set up Google Classroom, Canvas, or other LMS in `.mcp.json`
3. **Customize** - Add your school's rubrics, templates, and policies
4. **Save work** - Copy outputs to your preferred location

## Best Practices

- **Be specific** - The more detail you provide, the better the output
- **Request revisions** - Ask for different difficulty levels or formats
- **Save templates** - Keep frequently used plans for reuse
- **Connect tools** - Integrate with your LMS for one-click distribution

## What Each Skill Contains

| Skill | Purpose |
|-------|---------|
| `lesson-template` | Comprehensive lesson planning framework |
| `assessment-design` | Quiz and test creation guidelines |
| `feedback-framework` | Research-based feedback strategies |
| `standardized-test-prep` | Test preparation strategies |

## Need Help?

- Check `CONNECTORS.md` for tool setup instructions
- Review individual skill files for detailed guidance
- Ask for specific examples or variations