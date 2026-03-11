---
name: teacher-plugin-customizer
description: >
  Guide users through customizing the teacher plugin for their school or district.
  Use when users want to adapt this plugin to their specific curriculum, policies, or tools.
---

# Teacher Plugin Customizer

This skill helps you customize the Teacher Plugin for your specific school, district, or teaching context.

## Customization Areas

### 1. Curriculum Alignment

**What to customize:**
- Your state or national standards
- District-approved curriculum
- Scope and sequence documents
- pacing guides

**How to add:**
```
# In your lesson-plan command or skill

## [Your District] Standards
- [Standard code]: [Standard description]
- [Standard code]: [Standard description]
```

### 2. Rubrics and Grading

**What to customize:**
- School-wide rubric templates
- Weighting for grade categories
- Letter grade cutoffs
- Feedback language preferences

**How to add:**
```
# Create skills/[rubric-name]/SKILL.md

## [Your School] Rubric

| Criteria | Advanced | Proficient | Developing | Beginning |
|----------|----------|------------|------------|-----------|
| [Criterion 1] | [Your descriptor] | [Your descriptor] | [Your descriptor] | [Your descriptor] |
```

### 3. Classroom Management

**What to customize:**
- School-wide behavior system
- Reward/privilege structures
- Consequence progression
- Communication protocols

**How to add:**
```
# In classroom-management skill

## [School Name] Behavior System

**Levels:**
1. [Level 1] - [Description] - [Response]
2. [Level 2] - [Description] - [Response]
3. [Level 3] - [Description] - [Response]
```

### 4. Template Customization

**What to customize:**
- Lesson plan template structure
- Assessment format
- Feedback template
- Parent communication tone

**How to add:**
```
# Create skills/[template-name]/SKILL.md

## [Your Template Name]

### Structure
[Your preferred structure]

### Tone
[Your preferred tone]

### Required Elements
- [Element 1]
- [Element 2]
```

## Connector Customization

### Adding Your LMS

Edit `.mcp.json` to add your specific tools:

```json
{
  "mcpServers": {
    "your-lms": {
      "type": "http",
      "url": "https://your-lms.mcp.claude.com/mcp"
    }
  }
}
```

### Removing Unused Connectors

Remove connectors you won't use from `.mcp.json`:

```json
{
  "mcpServers": {
    // Keep only what you need
  }
}
```

## School-Specific Workflows

### IEP/504 Accommodations

Create a skill for your accommodation tracking:

```
# skills/iep-accommodations/SKILL.md

## [School Name] IEP Accommodations

**Categories:**
- Timing: [Your accommodation codes]
- Setting: [Your accommodation codes]
- Materials: [Your accommodation codes]
- Response: [Your accommodation codes]
```

### Professional Learning Communities

```
# skills/plc-process/SKILL.md

## [School Name] PLC Process

**Cycle:**
1. [Step 1] - [Description]
2. [Step 2] - [Description]
3. [Step 3] - [Description]
```

## Best Practices for Customization

1. **Start with what matters most** - Don't try to customize everything at once
2. **Keep it simple** - Simple customizations are more likely to be used
3. **Test with real work** - Try your customizations with actual lessons
4. **Iterate** - Refine based on what works in practice
5. **Share with colleagues** - Collaborate on school-wide customizations

## File Organization

```
teacher/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── commands/
│   └── [your commands]
├── skills/
│   ├── teacher-plugin-overview/
│   ├── teacher-plugin-customizer/
│   ├── [your custom skills]/
│   └── references/
├── CONNECTORS.md
└── README.md
```