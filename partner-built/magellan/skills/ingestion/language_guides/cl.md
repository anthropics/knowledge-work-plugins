# IBM CL (Control Language) Reference Guide

## Overview

CL (Control Language) is IBM's command language for the AS/400 (IBM i). CL programs orchestrate job-level operations: submitting batch jobs, overriding DB files, handling parameters, and executing RPG/COBOL programs.

CL programs compile into executable objects (`.PGM`, `.clle` for ILE, `.clp` for legacy). **Key insight**: CL programs rarely contain complex business logic. They control WHEN things run (job scheduling), HOW they run (environment routing), and AGAINST WHAT (file overrides). Business rules live in the called RPG/COBOL programs.

## Key Constructs

### Program Structure

```
PGM PARM(&PARAM1 &PARAM2)
  DCL VAR(&PARAM1) TYPE(*CHAR) LEN(10)
  /* body */
ENDPGM
```

- Variables prefix with `&`. Types include `*CHAR`, `*DEC`, `*LGL` (boolean).

### Commands (The Action Layer)

- **Execution**: `CALL PGM(lib/pgm)` (dynamic), `CALLPRC` (bound procedure).
- **Batch**: `SBMJOB CMD(...) JOB(name)` submits work asynchronously.
- **File Overrides**: `OVRDBF FILE(logical) TOFILE(physical)` dynamically points a program's file reference to a different database file. `OVRPRTF` overrides print formats.
- **Library List**: `ADDLIBLE`, `RMVLIBLE`. Alters the search path for finding databases and programs (environment routing).
- **Data Areas / Queues**: `RTVDTAARA` (Retrieve Data Area for global settings), `CHGDTAARA`. `SNDDTAQ` / `RCVDTAQ` (Send/Receive Data Queue) for async IPC.

### Control Flow

- `IF COND(...) THEN(...) ELSE(...)`
- Operators: `*EQ`, `*NE`, `*GT`, `*AND`, `*OR`.
- `SELECT / WHEN / OTHERWISE` for multi-branching.

### Error Handling — MONMSG

```
CALL PGM(MYPGM)
MONMSG MSGID(CPF0000) EXEC(DO)
  /* Handle failure */
ENDDO
```

- `MONMSG` acts as a structured try/catch. Placed directly after a command, it catches errors just for that command. Placed at the top level, it catches them globally.

## Common Patterns

### Environment File Routing

```
IF COND(&ENV *EQ 'PROD') THEN(DO)
  OVRDBF FILE(MAST) TOFILE(PRODDTA/MAST)
ENDDO
ELSE CMD(DO)
  OVRDBF FILE(MAST) TOFILE(TESTDTA/MAST)
ENDDO
CALL PGM(PROCESS)
```

The CL determines which dataset the RPG program mutates.

### Batch Orchestration via Job Queues

```
SBMJOB CMD(CALL PGM(RPTGEN) PARM(&DATE)) JOB(NIGHTRPT) JOBQ(QBATCH)
```

Passes runtime parameters to an async background job.

### Async Coordination via Data Queues

```
RCVDTAQ DTAQ(ORDQ) WAIT(-1) DATA(&ORDDATA)
CALL PGM(PROCESSORD) PARM(&ORDDATA)
```

Wait infinitely for a message on a queue, then process it. Common pattern for decoupling online input from background processing.

## What Carries Business Logic

**Extract facts from these:**

- `CALL` / `CALLPRC` — maps program dependencies.
- `OVRDBF` / `OVRPRTF` — maps dynamic data relationships. If `OVRDBF` occurs conditionally, it dictates distinct business scenarios.
- `SBMJOB` — reveals batch integration points and chronologies.
- `IF / SELECT` statements on parameters (`&PARAM`) — represents business branching.
- `SNDDTAQ` / `RCVDTAQ` — reveals asynchronous, event-driven business architectures.
- `RTVDTAARA` / `*LDA` (Local Data Area) — extracts system configuration limits or cross-program communication variables.

**Skip these (boilerplate):**

- Global `MONMSG MSGID(CPF0000)` without an `EXEC` block.
- `DLTOVR` file override cleanup.
- String slicing and padding variables for command execution.

## Common Misinterpretations

1. **Parameter Length mismatch is fatal.** CL handles parameters by reference. If a CL passes a 10-byte variable `&PARAM` but the RPG program expects 50 bytes, memory corruption occurs. Implicit sizes matter heavily.
2. **OVRDBF modifies the architecture, not the filesystem.** The RPG program compiled against `MYFILE`. CL intercepts references to `MYFILE` at runtime and redirects to `HISFILE`. It is dependency injection for files.
3. **MONMSG is not a console log.** It prevents the job from crashing and throwing a hard halt. It is strictly exception trapping.
4. **SBMJOB does not halt the calling program.** The command dispatches to a queue. The CL immediately proceeds to the next line.
5. **LDA (Local Data Area) is implicitly passed.** `*LDA` is a special 1024-byte memory space bound to the job. RPG and CL can communicate via it without explicitly declaring parameters.
6. **Library Lists dictate data access.** `ADDLIBLE` isn't just a PATH variable; it completely changes the target of an unqualified file reference.

## File Naming Conventions

- Extns: `.clle` (ILE CL, modern), `.clp` (Original Program Model CL).
- Often prefixed with `CL` or `CLP` (e.g., `CLORDPROC`).
- Programs are stored in source physical files, commonly `QCLSRC`.
