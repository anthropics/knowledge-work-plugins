# PL/I Reference Guide

## Overview

PL/I (Programming Language One) is IBM's general-purpose language spanning both business data processing and system programming, primarily on z/OS. It combines the structured nature of COBOL (packed decimals, precise file structures) with the flexibility of C (pointers, recursion, bitwise flags).

PL/I operates in MVS Batch regimes, CICS Online screens, and IMS DB/DC transaction hierarchies. It uses a rigid block-structured scope `BEGIN/END` and Procedure routines `PROC / END`. Data defaults to hardware-efficient forms: it uses standard EBCDIC collating, exact Fixed Decimal math, and pointer overlays.

## Key Constructs

### Program Structure and Data Types

- `procname: PROCEDURE OPTIONS(MAIN)`: Start of execution.
- `DCL` or `DECLARE`: Initializes memory fields.
  - `FIXED DECIMAL(p,q)`: Packed Decimal. The cornerstone of banking math.
  - `FIXED BINARY(15)`: Native standard integer.
  - `BIT(1)`: Boolean switches `1'B` or `0'B`.
  - `CHARACTER(n)`: Fixed length text.
- `BASED`: Pointer-driven memory overlay. `DCL X BASED(P)` maps variable X directly to address P without native allocation.

### Data Access

- **Record I/O**: `READ FILE(InF) INTO(Rec)` or `WRITE FILE(OutF) FROM(Rec)`.
- **Keyed/VSAM**: `READ FILE(idx) INTO(var) KEY(target)`.
- **Relational/DB2**: `EXEC SQL SELECT ... INTO :hostvar`. Standard cursor fetch loops.
- **IMS DL/I**: `CALL PLITDLI(...)`.

### Control Flow

- `IF / THEN / ELSE`: The standard split. The `THEN` executes the ensuing line or DO-group.
- `SELECT; WHEN(A=1)...; WHEN(A=3)...; END;`: Case statement.
- `DO WHILE(x)`, `DO UNTIL(y)`, `DO I=1 TO 10`.
- `DO; ... END;`: Groups statements without iteration.
- `ITERATE` (Next), `LEAVE` (Break), `GOTO` (Jump).

### Program-to-Program Communication

- `CALL prog(a, b)`: Synchronous module connection passing arguments strictly by reference.
- `FETCH prog`: Dynamic/late-binding routine load.
- `EXEC CICS LINK`: Dispatches across the CICS CWA context to external routines.

### Error Handling & Exceptions (ON Blocks)

- `ON ENDFILE(infile) EOF='1'B;`: Sets an async event handler for EOF.
- `ON KEY(idx) GOTO err_rtn;`: Submits a trap for VSAM Record Not Found failures.
- `ON ZERODIVIDE`, `ON CONVERSION`: Math/Casting exception handlers.

## Common Patterns

### Async Event Priming Loop

```pli
OPEN FILE(INFILE) INPUT;
ON ENDFILE(INFILE) EOF_FLAG = '1'B;
EOF_FLAG = '0'B;
READ FILE(INFILE) INTO(REC);

DO WHILE(^EOF_FLAG);
  IF REC.AMT > 0 THEN CALL PROCESS();
  READ FILE(INFILE) INTO(REC);
END;
```

Standard PL/I idiom: declare the trap, prime the read, loop until trap triggers.

### The C-Style Assign into Substrings

```pli
DCL 1 CUST,
      2 ID CHAR(10),
      2 FLG BIT(1);
SUBSTR(CUST.ID, 1, 3) = '100';
```

PL/I permits pseudo-variables on the Left-Hand side of an assignment, dynamically mutating partial strings inline.

### Pointer-Based Dynamic Parsing

```pli
DCL PTR POINTER;
DCL 1 LAYOUT BASED(PTR),
      2 NAME CHAR(20);
PTR = ADDR(BUFFER) + 5;
```

`NAME` now evaluates to the 20 bytes starting at `BUFFER + 5`.

## What Carries Business Logic

**Extract facts from these:**

- `IF` and `SELECT...WHEN`: Encodes strict monetary, date, and status code criteria.
- `READ DIR/KEY` operations map the domain dependencies.
- `ON KEY` or `ON CONVERSION` traps outline edge-cases the business accounts for explicitly.
- `FIXED DECIMAL` size definitions imply business limits (e.g., maximum allowable loan amount).
- `CALL` hierarchies and `ENTRY` declarations outline module responsibility lines.

**Skip these (boilerplate):**

- System-level `%PROCESS` or `OPTIONS` commands.
- Routine `OPEN`/`CLOSE` File definitions without context.
- Buffer math or `ADDR()` / `ALLOCATE` pointer manipulation routines meant solely to handle protocol messages.

## Common Misinterpretations

1. **The I-N Implicit Typing Bug.** If a variable is undeclared, PL/I defaults it to `FIXED BINARY(15)` if it starts with I, J, K, L, M, N. Otherwise it falls back to `FLOAT DECIMAL(6)`. Many silent bugs occur from spelling `DCL AMOUNT` vs `AMUNT` without declaring it.
2. **ON handlers are Event Listeners, not inline conditions.** `ON ENDFILE(F) EOF='1'B` does NOT evaluate immediately. It sets a global hook for that specific block scope.
3. **DO; ... END; is NOT a loop.** It operates like `{ }` in C or Java.
4. **Substrings mutate the source directly.** `SUBSTR(A,1,2) = 'YZ'` rewrites `A`.
5. **BIT math vs Boolean Logic.** `&` is a bitwise AND. `^` is NOT. `|` is OR. Do not mistake them for arithmetic `+` or `-`.

## File Naming Conventions

- Extns: `.pli`, `.pl1`.
- Source Members: 1-8 char PDS.
- Copybooks: Loaded via `%INCLUDE MEMBER;`.
