# CICS COBOL Reference Guide

## Overview

CICS (Customer Information Control System) is IBM's online transaction processing (OLTP) monitor for z/OS mainframes. CICS COBOL programs are standard COBOL programs augmented with `EXEC CICS ... END-EXEC` commands providing terminal I/O, file access, and transactional integrity.

CICS programs are **pseudo-conversational**: the program sends a screen to the user, terminates, and a new instance restarts when the user replies. State is preserved across invocations within the COMMAREA or modern Channels/Containers. Screen layouts are defined in BMS (Basic Mapping Support) mapsets.

## Key Constructs

### Program Structure

- **DFHCOMMAREA**: The communication area passed between invocations, preserving state (current screen, customer record, flags).
- **DFHEIBLK** (EIB): Execute Interface Block — system-provided struct containing metadata: `EIBCALEN` (COMMAREA length), `EIBAID` (last key pressed), `EIBTRNID`.
- **Channels and Containers**: Modern alternative to COMMAREA that removes the 32KB limit.

### Data Access (Database / File I/O)

CICS programs do NOT use standard COBOL `READ`/`WRITE`.

- `EXEC CICS READ FILE('name') INTO(ws-rec) RIDFLD(ws-key) END-EXEC`: Keyed VSAM read.
- `EXEC CICS READ ... UPDATE`: Locks the record for update. Followed by `REWRITE`.
- `EXEC CICS STARTBR` / `READNEXT` / `ENDBR`: Browse through a dataset sequentially.
- **Queues**: `EXEC CICS WRITEQ TS` (Temporary Storage Queue for scratchpad data) and `WRITEQ TD` (Transient Data Queue for triggering batch jobs or logging).

### Control Flow

- `EXEC CICS SEND MAP('MAP1') MAPSET('MAPSET1') ERASE`: Send a screen.
- `EXEC CICS RECEIVE MAP('MAP1')`: Receive user input into the symbolic map.
- `EXEC CICS RETURN TRANSID('TRN1') COMMAREA(WS-COMM)`: End invocation; restart `TRN1` when user responds.
- The `EIBAID` field (e.g., `DFHENTER`, `DFHPF3`) dictates workflow branching.

### Program-to-Program Communication

- `EXEC CICS LINK PROGRAM('SUBPGM') COMMAREA(WS-DATA)`: Synchronous call (returns control).
- `EXEC CICS XCTL PROGRAM('NEXTPGM') COMMAREA(WS-DATA)`: Transfer control (does NOT return). Used to chain screens.
- `EXEC CICS START TRANSID('TRN2')`: Asynchronously start another transaction.

### Error Handling

- `RESP` / `RESP2`: Inline response codes. `IF WS-RESP = DFHRESP(NOTFND)`.
- `EXEC CICS HANDLE CONDITION NOTFND(para-name)`: Legacy implicit asynchronous branch (GOTO). Traps errors gobally.

## Common Patterns

### Pseudo-Conversational Main Loop

```cobol
    IF EIBCALEN = 0
      PERFORM FIRST-TIME-SETUP
      EXEC CICS SEND MAP('MAIN') ERASE END-EXEC
      EXEC CICS RETURN TRANSID('MTRN') COMMAREA(WS-COMM) END-EXEC
    ELSE
      MOVE DFHCOMMAREA TO WS-COMM
      EXEC CICS RECEIVE MAP('MAIN') END-EXEC
      PERFORM PROCESS-INPUT
    END-IF
```

`EIBCALEN = 0` implies no prior state. Non-zero means a continuation.

### Key-Press Dispatch

```cobol
    EVALUATE EIBAID
      WHEN DFHENTER  PERFORM PROCESS-ENTER
      WHEN DFHPF3    EXEC CICS RETURN END-EXEC
      WHEN DFHPF12   EXEC CICS XCTL PROGRAM('MENU') END-EXEC
    END-EVALUATE
```

### Browse Pattern (READNEXT)

```cobol
    EXEC CICS STARTBR FILE('ACCT') RIDFLD(WS-KEY) END-EXEC.
    PERFORM UNTIL WS-RESP = DFHRESP(ENDFILE)
      EXEC CICS READNEXT FILE('ACCT') INTO(WS-REC) RESP(WS-RESP) END-EXEC
      IF WS-RESP = DFHRESP(NORMAL) PERFORM PROCESS-REC
    END-PERFORM.
    EXEC CICS ENDBR FILE('ACCT') END-EXEC.
```

## What Carries Business Logic

**Extract facts from these:**

- `EVALUATE EIBAID` blocks — map function keys to business actions/workflow.
- `EXEC CICS READ/REWRITE/DELETE` with `FILE(...)` — the core data lifecycle.
- `EXEC CICS LINK` and `XCTL` — dependencies on shared business services.
- `EXEC CICS READNEXT` loops — handles subsetting and listing of data.
- COMMAREA mapping before LINK/XCTL — reveals the API contract.
- RESP handlers (`DFHRESP(NOTFND)`, `DFHRESP(DUPREC)`) — encode rules for missing/duplicate data.

**Skip these (boilerplate):**

- `HANDLE CONDITION` / `HANDLE ABEND` global traps.
- DFHEIBLK / DFHCOMMAREA memory layout definitions.
- BMS cursor positioning (`MOVE -1 TO fieldL`).

## Common Misinterpretations

1. **CICS programs are NOT long-running.** They survive for milliseconds. The conversation spans dozens of separate, stateless program executions chained together by the `COMMAREA`.
2. **EIBCALEN = 0 is not an error.** It signals the start of a brand new workflow session.
3. **LINK is a function call; XCTL is a GOTO.** `LINK` returns. `XCTL` does not.
4. **FILE('xyz') is NOT a dataset name.** It's an FCT (File Control Table) mapping to a VSAM file. The same program can target different files via FCT.
5. **TSQ/TDQ are not standard DB tables.** TSQs are temporary scratchpads (often used to hold paginated search results). TDQs are sequential triggers for asynchronous work.
6. **HANDLE CONDITION alters flow invisibly.** A `HANDLE CONDITION NOTFND(X)` at the top of a program means ANY subsequent `READ` that fails implicitly GOTOs paragraph X.
7. **BMS maps have three layers.** Every symbolic field has `L` (length), `F`/`A` (attribute), and `I`/`O` (input/output data). Only the `I`/`O` suffix handles real business data.

## File Naming Conventions

- `.cbl`, `.cob`: Source code.
- `.bms`, `.map`: Screen definitions.
- `.cpy`: Copybooks (COMMAREA layouts).
- PDS Members: Max 8 characters. Transaction IDs max 4 characters (e.g., `TRN1`).
