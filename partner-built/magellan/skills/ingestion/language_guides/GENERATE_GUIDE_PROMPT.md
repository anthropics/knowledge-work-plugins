# Language Guide Generation Prompt

Use this prompt with any LLM to generate a Magellan-compatible language guide.
Replace `{LANGUAGE}` with the target language (e.g., "NATURAL/ADABAS", "PL/I",
"REXX", "JCL", "CICS COBOL", "Assembler/370", "Easytrieve", "IDMS", "Fortran",
"PowerBuilder", "Progress 4GL", "MUMPS/M", "Pick BASIC", "ABAP").

Run the same prompt through multiple models and merge the best outputs.

---

## The Prompt

```
I need you to demonstrate deep knowledge of {LANGUAGE} by completing two tasks.

## Task 1: Verification (prove you know the language)

Answer these 10 questions about {LANGUAGE}. Be specific — cite exact syntax,
keywords, or conventions. If you don't know an answer with confidence, say
"uncertain" rather than guessing.

1. What platform(s) does {LANGUAGE} primarily run on?
2. Show the minimal "hello world" or equivalent program structure.
3. What is the primary mechanism for database/file access? Show the exact syntax.
4. How does the language handle control flow (conditionals, loops)? Show syntax.
5. How does one program call another? Show the exact call mechanism.
6. What is the variable/data declaration syntax?
7. How are errors or exceptions handled?
8. What is the compilation/execution model? (compiled, interpreted, both?)
9. Name 3 constructs that a developer unfamiliar with this language would
   likely misinterpret, and explain what they actually mean.
10. What is the most common anti-pattern or "code smell" in legacy {LANGUAGE}
    codebases, and what does it usually indicate about the business logic?

## Task 2: Generate the Guide

Using your verified knowledge, produce a reference guide in exactly this format.
This guide will be read by an AI system that is extracting business rules and
facts from legacy source code. The guide must help the AI understand what it's
reading — not teach a developer how to write new code.

Write the guide using this exact structure:

---

# {LANGUAGE} Reference Guide

## Overview

[2-3 paragraphs: What is this language? What platform does it run on? What era
is it from? What are its primary file formats / extensions? Are there multiple
dialects or versions the AI might encounter?]

## Key Constructs

### Program Structure
[How is a program organized? What are the major sections/divisions? What do the
first few lines tell you about what the program does?]

### Data Access (Database / File I/O)
[This is the MOST IMPORTANT section. How does the program read, write, update,
and delete data? What are the exact operation names/keywords? What do they
translate to in SQL terms?]

### Control Flow
[Conditionals, loops, branching. Focus on patterns that encode business rules
(e.g., "IF ACCOUNT-STATUS = 'D'" means a business decision is happening).]

### Program-to-Program Communication
[How does one program call another? What are the call mechanisms (static, dynamic,
message-based)? How are parameters passed?]

### Error Handling
[How does the program detect and handle errors? What are the standard patterns?]

## Common Patterns

[Show 3-5 code examples of the most frequent patterns found in production
codebases. Each example should be real-world (not textbook), 5-15 lines,
with a one-line explanation of what the pattern does. Focus on patterns that
carry business logic.]

## What Carries Business Logic

**Extract facts from these:**
[Bulleted list of constructs, operations, and patterns that encode business
rules, thresholds, calculations, and decisions. These are what the AI should
focus on during fact extraction.]

**Skip these (boilerplate):**
[Bulleted list of constructs that are infrastructure, plumbing, or standard
setup. These rarely contain business logic and the AI should not spend time
on them.]

## Common Misinterpretations

[Numbered list of 5-10 things that an AI (or a developer unfamiliar with this
language) would likely get wrong. Each entry should explain:
- What the construct LOOKS like to an outsider
- What it ACTUALLY means
- Why this matters for understanding business logic

These are the most valuable part of the guide. Be specific.]

## File Naming Conventions

[What file extensions and naming patterns does this language use? How can you
identify the type of program (batch, online, subroutine, copybook) from the
filename or member name?]

---

IMPORTANT RULES:
- Do NOT pad with generic information. Every sentence should help an AI
  understand legacy source code it's reading for the first time.
- Do NOT include installation, IDE setup, or "getting started" content.
- DO include misinterpretations even if they seem obvious to an expert.
  The reader is an AI that has broad but shallow knowledge.
- DO use exact syntax in examples, not pseudocode.
- DO mention platform-specific behavior (e.g., EBCDIC vs ASCII, packed
  decimal, fixed-length records) that affects how data is interpreted.
- Keep the guide under 200 lines. Conciseness is critical — this will be
  loaded into a context window alongside source code.
```

---

## Languages to Generate Guides For

Priority 1 — Common legacy languages in enterprise knowledge discovery:
- [ ] NATURAL / ADABAS
- [ ] PL/I
- [ ] JCL (Job Control Language)
- [ ] REXX
- [ ] CICS (COBOL with CICS commands)
- [ ] Assembler/370 (BAL)
- [ ] Easytrieve
- [ ] IDMS

Priority 2 — Other legacy platforms:
- [ ] MUMPS / M (healthcare systems)
- [ ] Pick BASIC / UniVerse BASIC
- [ ] PowerBuilder (PowerScript)
- [ ] Progress 4GL / OpenEdge ABL
- [ ] ABAP (SAP)
- [ ] Fortran (scientific/engineering legacy)
- [ ] Informix 4GL
- [ ] Clipper / dBASE / FoxPro
- [ ] Uniface
- [ ] CA Gen / Cool:Gen (generated COBOL)
- [ ] Synon / 2E (AS400 code generator)
- [ ] RM COBOL / Micro Focus COBOL (PC COBOL variants)

Priority 3 — Niche but encountered:
- [ ] Mapper (Unisys)
- [ ] LINC / Unisys
- [ ] Datapoint DATABUS
- [ ] Tandem TAL / pTAL
- [ ] ADS/Online (IDMS)
- [ ] Telon (generated COBOL)
- [ ] CSP (IBM Cross System Product)

## Merging Outputs from Multiple Models

After running the prompt through N models:
1. Compare Task 1 answers — discard outputs from models that answered
   "uncertain" on more than 3 questions (they don't know the language well).
2. For each section, pick the most specific and accurate version.
3. Merge "Common Misinterpretations" from all models — different models
   catch different blind spots.
4. Have a domain expert (or a high-capability model) do a final review pass.
5. Save the merged guide as `{language}.md` in this directory.
