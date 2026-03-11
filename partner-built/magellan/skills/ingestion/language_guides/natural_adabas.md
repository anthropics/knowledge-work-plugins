# Natural / ADABAS Reference Guide

## Overview

Natural is Software AG's 4GL (compiled or interpreted) designed for business platforms, natively coupled with ADABAS (an inverted-list, non-relational database).

Files have extensions `.NSP` (program), `.NSN` (subprogram), `.NSL`/`.NSG`/`.NSA` (Data Areas for Local/Global/Parameters), `.NSM` (screen Maps).
Code operates in **Structured Mode** (modern, explicit block bounds) or **Reporting Mode** (legacy, implicit looping).

## Key Constructs

### Program Structure

- variables reside in Data Areas. `DEFINE DATA LOCAL USING LDA-NAME`.
- **Views**: `1 EMPLOYEES-V VIEW OF EMPLOYEES` maps program logic to ADABAS file descriptors.
- `LOCAL`, `GLOBAL`, `PARAMETER` define variable scopes.

### Data Access (Non-Relational)

- `READ view BY descriptor`: Loops through a table sequentially using an index route.
- `FIND view WITH field = 'x'`: Extracts records using inverted list lookups. Triggers an implicit `FOR EACH` loop.
- `GET view ISN-VALUE`: Direct address grab by Internal Sequence Number (Physical ID).
- `HISTOGRAM`: Read index counts efficiently without opening full records.
- `UPDATE / DELETE`: Mutates locked instances.
- **Reporting Mode clauses**: `ACCEPT IF...`, `REJECT IF...` (Inline row-level DB filtration) and `AT BREAK OF field` (Aggregation triggers).

### Control Flow

- `DECIDE ON FIRST VALUE OF field` (Switch/Case statement).
- `FOR`, `REPEAT UNTIL`.
- `ESCAPE TOP`: Jump to next loop iteration. `ESCAPE BOTTOM`: Break out of loop. `ESCAPE ROUTINE`: Return from method.

### Program-to-Program Communication

- `CALLNAT 'NPGM' parm1`: Subprogram call (Push/Pop context).
- `FETCH 'NPGM'`: Permanent transfer of control. `FETCH RETURN` preserves it.
- `STACK COMMAND 'pgm'`: Places commands in a global queue to dictate subsequent UI workflows natively.

### Error Handling

- `ON ERROR ... END-ERROR`. Wraps block level exceptions.
- `BACKOUT TRANSACTION` rolls back uncommitted `UPDATE/STORE` operations; `END TRANSACTION` hard commits them.

## Common Patterns

### Implicit Loop via READ / FIND

```natural
FIND EMPLOYEES-V WITH DEPT = 'SALES' RETAIN AS 'HOLD'
  IF SALARY > 50000
    PERFORM APPLY-BONUS
    UPDATE
  END-IF
END-FIND
END TRANSACTION
```

Every line inside the `FIND` / `END-FIND` executes *per record*. `RETAIN AS` locks the records natively in ADABAS during the sweep.

### Periodic Groups (Multi-Value Arrays)

```natural
FIND EMP-V WITH ID = '123'
  FOR #I = 1 TO C*INCOME
    IF INCOME(#I) > 0 WRITE INCOME(#I)
  END-FOR
END-FIND
```

ADABAS natively stores arrays inside rows. `C*INCOME` is an automatically generated integer representing the total count of occurrences of the `INCOME` field in that specific row.

### External Parameter Binding

```natural
DEFINE DATA PARAMETER USING PDA-PROC
LOCAL USING LDA-VARS
GLOBAL USING GDA-SYST
END-DEFINE
```

Links external `.NSA`, `.NSL`, `.NSG` copybook layouts into local memory mapping.

## What Carries Business Logic

**Extract facts from these:**

- `FIND ... WITH` / `READ ... BY` — defines the business queries and indexed filter patterns.
- `ACCEPT` / `REJECT` — Reporting mode data filtration constraints.
- `AT BREAK OF` / `AT END OF DATA` — control breaks where monetary aggregation/reports execute.
- `END TRANSACTION` — denotes exactly where atomic business boundaries lie.
- `DECIDE ON` trees — explicit business process routing.
- `CALLNAT` parms — tracks API interactions between distinct microservice boundaries.
- Uses of `C*` variables indicate business logic iterating over nested relationships (Line-items inside Headers).

**Skip these (boilerplate):**

- Screen positioning `POSITION x y` / `DISPLAY` aesthetics.
- Standard variables initializations (`RESET #VAR`).
- `SET KEY` UI mapping without complex conditional handlers.

## Common Misinterpretations

1. **READ and FIND are loops.** A `FIND` statement is not a single database fetch. It inherently declares a `WHILE` loop containing the lines beneath it up to `END-FIND`.
2. **ADABAS is NOT Relational SQL.** It operates on ISNs (Internal addresses) and inverted lists. Do not document ADABAS paths as SQL `JOIN`s. They correlate through explicit nested `FIND` queries.
3. **Periodic groups (`#VAR(1:10)`) are native repeating datasets.** It's not memory instantiation; a DB row functionally contains 10 occurrences of that field natively.
4. **ESCAPE BOTTOM is NOT an error trap.** It performs a loop `break`.
5. **GDA (Global Data Areas) persist over the entire session.** State leakage between decoupled programs using heavily populated `.NSG` elements is standard architectural practice.
6. **Error 113 means Normal EOF/No Records.** This isn't a hard system failure; it handles generic "not found" conditional branching.

## File Naming Conventions

- Extns: `.NSP` (Program), `.NSN` (Subprogram), `.NSL` (Local DTA), `.NSG` (Global DTA), `.NSA` (Parm DTA), `.NSM` (Map).
- Code is typically 8-char abbreviated stored in FUSER physical volumes.
