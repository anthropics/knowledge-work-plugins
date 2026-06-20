---
name: Student Assessment
stability: stable
description: Create rubrics, quizzes, exams, and formative assessments aligned to learning objectives. Generate answer keys, grading guides, and detailed feedback templates.
triggers:
  - "create a rubric for"
  - "design a quiz on"
  - "build an assessment for"
  - "write exam questions"
  - "create a grading guide"
---

# Student Assessment

Design assessments that actually measure what students learned — not just what they can memorize. From quick formative checks to comprehensive summative exams.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│ STUDENT ASSESSMENT                                              │
├─────────────────────────────────────────────────────────────────┤
│ ALWAYS (works standalone)                                       │
│ ✓ You tell me: topic, objectives, student level, format       │
│ ✓ Build: questions, rubrics, answer keys, feedback stems      │
│ ✓ Align: to Bloom's taxonomy levels                          │
│ ✓ Output: complete assessment ready to use                    │
├─────────────────────────────────────────────────────────────────┤
│ SUPERCHARGED (when you connect your tools)                      │
│ + LMS: publish quizzes directly to Canvas / Google Classroom  │
│ + Gradebook: auto-generate grading criteria matching rubric   │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

Tell me what you need:
- "Create a rubric for a persuasive essay, 9th grade, 4-point scale"
- "Write 20 multiple-choice questions on photosynthesis for 7th graders"
- "Design a project-based assessment for a Python basics unit"
- "Build a formative check-in quiz on the Bill of Rights"

**Required:**
- Topic or learning objectives to assess
- Student level (grade, age, experience)
- Assessment format (quiz, rubric, project, presentation, etc.)

## Assessment Types

### Multiple Choice Quiz
- Specify: number of questions, difficulty distribution, distractors quality
- Output: questions + answer key + rationale for each answer

### Rubric
- Specify: task type, number of criteria, scale (4-point, percentage, etc.)
- Output: criteria descriptors for each performance level

### Essay / Open-Response
- Specify: prompt type, length expectations, key concepts to cover
- Output: prompt + exemplar response + scoring guide

### Project / Performance Assessment
- Specify: deliverables, process vs. product weighting
- Output: project brief + rubric + self-assessment checklist

## Output Format (Rubric Example)

```markdown
# Rubric: [Assignment Title]

**Task:** [Brief description]
**Total Points:** [X]

| Criteria | 4 - Exceeds | 3 - Meets | 2 - Approaching | 1 - Beginning |
|----------|-------------|-----------|-----------------|---------------|
| [Criterion 1] | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] |
| [Criterion 2] | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] |

**Feedback Stems:**
- Strong performance: "[Sentence starter]"
- Needs improvement: "[Sentence starter]"
- Next steps: "[Sentence starter]"
```

## Related Skills
- **curriculum-design** — Build the full course before designing assessments
- **learning-path** — Create personalized remediation based on assessment results
