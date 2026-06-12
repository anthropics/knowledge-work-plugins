# JCL (Job Control Language) Reference Guide

## Overview

JCL (Job Control Language) is the batch scripting format for IBM z/OS. JCL orchestrates execution: it defines **what programs run**, **in what order**, **with what data files**, and **under what conditions**. A single JCL stream typically maps to a holistic business process (e.g., Nightly Settlement, End of Month Billing).

It uses rigid column-positional syntax (`//` in cols 1-2). Max 8 character names. JCL rarely holds procedural loop logic itself; instead, its power lies in tying disparate utilities, database modules, and custom COBOL logic into a cohesive pipeline.

## Key Constructs

### Program Structure

- `//jobname JOB`: The outer wrapper defining the execution queue (`CLASS`), priority, and reporting (`MSGCLASS`).
- `//stepname EXEC PGM=pgmname,PARM='args'`: The heart of JCL. Executes a COBOL, ASM, or Utility program, passing optional `PARM` args to it.
- `//stepname EXEC PROC=procname`: Calls a parameterized JCL macro/template.
- `//  INCLUDE MEMBER=name`: Inserts another PDS member statically like a macro.

### Data Access

- `//ddname DD DSN=dataset.name,DISP=(status,normal,abnormal)`: Data Definition. Maps a logical target (`ddname`) expected by the program to the physical `dataset.name`.
- `DISP=(SHR)` (Shared read), `DISP=(OLD,KEEP)` (Exclusive lock), `DISP=(NEW,CATLG,DELETE)` (Create, register, or delete on fail).
- `//SYSIN DD *`: Inline configuration or control cards, terminated by `/*`. Commonly feeds parameters to Sorts, DB2 utilities, or COBOL.

### Control Flow

- `COND=(rc,operator)` on `EXEC`: Skips this step if a condition is true. `COND=(4,LT)` means "skip if 4 is LESS THAN any preceding return code" (i.e., skip if error >= 8).
- `//IF1 IF (STEP1.RC EQ 0) THEN`: Modern explicit branching.
- `RESTART=stepname` on `JOB`: Force resume from an aborted step.

### Essential Utilities

JCL executes IBM utilities heavily. These hold immense implicit business processing:

- **IDCAMS**: Manages VSAM files (Delete, Define, Backup/Restore).
- **SORT (DFSORT / SyncSort)**: Extremely powerful. Can pre-filter data (`INCLUDE COND`), pre-aggregate records (`SUM FIELDS`), and reformat bytes. **Omitted sort logic destroys business rule lineage.**
- **IKJEFT01**: The TSO terminal monitor. Used heavily to execute DB2/SQL batch programs (via `DSN RUN PROGRAM(...)`).
- **IEBGENER / ICEGENER**: Copies data from one dataset to another or routes sequential files to print.

## Common Patterns

### Utility Pre-Processing, Custom COBOL Main-Processing

```
//SORT1   EXEC PGM=SORT
//SORTIN  DD DSN=PROD.RAW.DATA,DISP=SHR
//SORTOUT DD DSN=&&TMPDATA,DISP=(NEW,PASS)
//SYSIN   DD *
  SORT FIELDS=(1,10,CH,A)
  INCLUDE COND=(15,2,CH,EQ,C'AC')
/*
//PROCSS  EXEC PGM=BILLCOBOL
//INPUT   DD DSN=&&TMPDATA,DISP=(OLD,PASS)
```

The Sort filters strictly for `AC` (Active) accounts. The downstream COBOL program assumes the data is pre-validated.

### DB2 Batch Execution

```
//DB2RUN  EXEC PGM=IKJEFT01
//SYSTSIN DD *
  DSN SYSTEM(DB2P)
  RUN PROGRAM(COBOLPGM) PLAN(COBPLAN) PARMS('01/01/2024')
  END
/*
```

## What Carries Business Logic

**Extract facts from these**:

- `EXEC PGM=` and `EXEC PROC=` chronologies — define the macro-level order of operations.
- `DSN=` names in `DD` cards — track the lineage of master files to temporary work files (`&&TMP`) to output final report files.
- `SYSIN DD *` blocks passed to `SORT` — `INCLUDE COND` and `SUM FIELDS` are pure data filtration business logic occurring outside of COBOL.
- `COND/IF` branching — dictates the error handling routing of the batch night.
- `PARM=` arguments and `SYSTSIN` lines — reveal dates, environment overrides, or toggle flags mapping to COBOL's `LINKAGE SECTION`.

**Skip these (boilerplate)**:

- `SYSOUT=*`, `SYSMDUMP`, `SYSPRINT` — log routing.
- `STEPLIB/JOBLIB` — OS library search paths.
- Storage mapping allocations (`SPACE=(CYL,(...))`, `DCB=...`).

## Common Misinterpretations

1. **JCL is not just a runner.** A `SORT` step pre-aggregating monetary records is *just as critical* to the business process as the COBOL program. Don't skip `SORT` parameters.
2. **COND tests evaluate to SKIP, not to KEEP.** `COND=(12,EQ)` translates to: "If the prior RC equals 12, SKIP this step."
3. **DD names are the program interface.** If COBOL says `SELECT MASTER-IN ASSIGN TO 'MSTR01'`, then JCL MUST have `//MSTR01 DD DSN=...`. This allows dynamic data switching.
4. **GDGs are relative date trackers.** Dataset `PROD.FILE(+1)` creates today's version. `PROD.FILE(0)` reads the latest. `PROD.FILE(-1)` reads yesterday's.
5. **Double Ampersand (`&&`) means Temporary.** `DSN=&&TEMP1` exists only for this specific batch execution pipeline and cannot be retrieved globally.

## File Naming Conventions

- PDS members: 1-8 chars, e.g., `DLYBILL`, `ACCTEXT`.
- Extns: `.jcl`, `.job`.
- Dataset patterns: `ENV.SYSTEM.PROCESS.TYPE` (`PROD.GL.MONTHLY.REPORTS`).
