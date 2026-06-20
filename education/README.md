# Education Plugin

An AI-powered instructional design specialist for educators, trainers, and learning & development professionals. Built for [Claude Cowork](https://claude.ai) but also compatible with Claude Code.

## What It Does

The Education plugin helps you design, build, and deliver better learning experiences faster.

| Skill | How it helps |
|-------|-------------|
| **Curriculum Design** | Design comprehensive curricula with scope & sequence, unit plans, and assessments aligned to standards |
| **Student Assessment** | Create rubrics, quizzes, exams, and formative checks aligned to learning objectives |
| **Learning Path** | Build personalized learning progressions for individual students or cohorts |

## Connectors

| Connector | What it adds |
|-----------|-------------|
| Slack | Team communication and parent/student announcements |
| Notion | Course content repository and knowledge base |
| Google Classroom | Course management, assignment publishing, and submission collection |
| Canvas | LMS course delivery, gradebook, and student data |

## Quick Start

### Claude Cowork
Install from [claude.com/plugins](https://claude.com/plugins).

### Claude Code
```bash
# Add the marketplace first
claude plugin marketplace add anthropics/knowledge-work-plugins

# Then install the education plugin
claude plugin install education@knowledge-work-plugins
```

## Example Prompts

- "Design a 6-week unit on climate change for 8th graders"
- "Create a rubric for a research paper, 10th grade, 100 points"
- "Build a 12-week Python programming course for adult learners, project-based"
- "Write 20 quiz questions on the American Civil War, 5th grade level"
- "Create a differentiated learning path for students who struggled with fractions"

## Making It Yours

This plugin is a starting point. Customize it for your context:

**Swap connectors** — Edit `.mcp.json` to connect your actual LMS and tools.

**Add institutional context** — Tell Claude about your school's pedagogy, standards, and student population in the skill files.

**Adjust for your level** — Modify skill files to reflect the specific grade bands, subject areas, or training domains you work in.

**Extend with new skills** — Add skills for parent communication, IEP support, substitute lesson plans, or professional development.

## Contributing

Skills are just Markdown files. Fork the repo, make changes, and submit a pull request.
