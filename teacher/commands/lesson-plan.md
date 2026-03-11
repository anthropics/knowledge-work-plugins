---
description: Create a comprehensive lesson plan for a class
argument-hint: "<topic> <grade/level> <duration>"
---

# Lesson Plan

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Create a comprehensive, standards-aligned lesson plan with objectives, activities, assessments, and differentiation strategies.

## Usage

```
/lesson-plan <topic> <grade/level> <duration>
```

Examples:
- `/lesson-plan photosynthesis 7th-grade 45-minutes`
- `/lesson-plan quadratic equations high-school 60-minutes`
- `/lesson-plan persuasive writing 5th-grade 90-minutes`

## Workflow

### 1. Gather Information

Extract from the input:
- **Topic**: The subject matter to teach
- **Grade/Level**: Student level (consider developmental appropriateness)
- **Duration**: Class period length
- **Additional context**: Standards, student needs, available resources

### 2. Create Lesson Structure

Use the **lesson-template** skill as a foundation and build:

#### Header Information
- **Topic**: [Topic Name]
- **Grade Level**: [Grade/Level]
- **Duration**: [Time]
- **Date**: [Proposed date]

#### Learning Objectives
- **CCSS/Standard**: [Relevant standard code]
- **I Can Statement**: [Student-friendly objective]
- **Success Criteria**: [How students show mastery]

#### Materials
- [List physical and digital resources]
- [Technology requirements]

#### Lesson Procedure

**Launch (5-10 min)**
- Hook/Engage students
- Connect to prior knowledge
- Share objectives

**Explore/Develop (20-30 min)**
- Active learning activity
- Guided practice
- Think-pair-share or collaborative work

**Synthesize/Close (10-15 min)**
- Summary discussion
- Exit ticket/check for understanding
- Preview next lesson

#### Assessment
- **Formative**: [During lesson checks]
- **Summative**: [End of lesson assessment]
- **Differentiation**: [Support for all learners]

#### Homework/Extension
- [Optional practice or pre-work for next class]

### 3. Review and Refine

- Check alignment between objectives and activities
- Ensure accessibility for all learners
- Verify timing is realistic

### 4. Output Format

Present the lesson plan in clean markdown with clear section headers. Include:
- Time allocations for each phase
- Teacher questions to ask
- Expected student responses
- Common misconceptions to address

### 5. Offer Next Steps

- "Want me to create the slide deck for this lesson?"
- "Should I generate a worksheet for the activity?"
- "Need an assessment with answer key?"
- "Shall I add this to your [Google Classroom/Canvas]?"

## Notes

- Adjust complexity based on grade level
- Include multiple entry points for diverse learners
- Build in formative assessment throughout
- Consider culturally responsive teaching practices