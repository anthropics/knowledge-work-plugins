---
description: Create quizzes, tests, or assignments with answer keys
argument-hint: "<topic> <type> <number of questions>"
---

# Assessment

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Create quizzes, tests, exit tickets, or assignments aligned with learning objectives, complete with answer keys and scoring guidance.

## Usage

```
/assessment <topic> <type> <number of questions>
```

Examples:
- `/assessment fractions multiple-choice 10`
- `/assessment essay writing 1`
- `/assessment photosynthesis mixed 15`
- `/assessment quadratic equations short-answer 5`

## Assessment Types

| Type | Description |
|------|-------------|
| `multiple-choice` | Standard MCQs with distractors |
| `short-answer` | Brief responses required |
| `essay` | Extended written responses |
| `true-false` | Concept checks |
| `mixed` | Combination of types |
| `performance` | Task-based assessment |

## Workflow

### 1. Determine Assessment Parameters

- **Topic**: What is being assessed?
- **Cognitive Level**: Recall, application, analysis, creation?
- **Format**: Multiple-choice, short-answer, essay, etc.
- **Number of Items**: Quantity of questions/tasks
- **Difficulty**: Appropriate for student level

### 2. Create Assessment Items

For each question:

**Multiple-Choice**
- Clear stem/question
- One correct answer
- Three plausible distractors
- Distractors based on common misconceptions

**Short-Answer**
- Direct question
- Clear expected response
- Scoring rubric

**Essay/Performance**
- Clear task description
- Rubric with criteria
- Performance levels (Excellent, Proficient, Developing, Emerging)

### 3. Create Answer Key and Scoring Guide

- Correct answers
- Partial credit guidance
- Exemplar responses for essays
- Common errors to watch for

### 4. Organize Output

```
# [Topic] Assessment

## Multiple Choice (X points each)
1. Question...
   A) Option
   B) Option
   C) Option
   D) Option

## Short Answer
1. Question...
   [Space for response]

## Answer Key

### Section 1: Multiple Choice
1. B — [Explanation]
2. D — [Explanation]

### Section 2: Short Answer
1. [Correct response]
   Scoring: [Points available]
   [Rubric criteria]

## Rubric (for essays/performance)
| Criteria | Excellent (4) | Proficient (3) | Developing (2) | Emerging (1) |
|----------|---------------|----------------|----------------|--------------|
| [Criterion] | [Description] | [Description] | [Description] | [Description] |
```

### 5. Offer Next Steps

- "Want me to generate a Google Forms version?"
- "Should I create an editable Word/PDF version?"
- "Need a version with scaffolding for struggling students?"
- "Shall I upload this to [Google Classroom/Canvas]?"

## Notes

- Balance question types for comprehensive assessment
- Include at least one higher-order thinking question
- Ensure accessibility in formatting
- Consider timing constraints