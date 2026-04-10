---
name: review
description: Review code for Sanity best practices and common issues.
---

# Sanity Code Review

I'll review your Sanity code for best practices. Here's what I check:

## Schema Review

1. **Definition Syntax**
   - Using `defineType`, `defineField`, `defineArrayMember`
   - Icons assigned from `@sanity/icons`
   - Proper validation rules

2. **Data Modeling**
   - "Data > Presentation" philosophy (no `bigHero`, `redButton`)
   - Correct use of references vs nested objects
   - Proper deprecation pattern for removed fields

3. **Organization**
   - File naming conventions (kebab-case)
   - Schema directory structure

## Query Review

1. **TypeGen Compatibility**
   - Queries wrapped in `defineQuery`
   - SCREAMING_SNAKE_CASE naming
   - Proper field projections (not `*`)

2. **Performance**
   - No unnecessary deep expansions
   - Using query parameters (not string interpolation)

## Frontend Review

1. **Visual Editing**
   - Using `_key` for array item keys (not index)
   - `stegaClean` for logic-critical values
   - No stega in `<head>` tags

2. **Type Safety**
   - Using generated types from `sanity.types.ts`
   - No manual typing of query results

## Usage

Just ask me to review specific files or your whole Sanity setup:
> "Review my post schema"
> "Check my GROQ queries for issues"
> "Review my Sanity frontend integration"

