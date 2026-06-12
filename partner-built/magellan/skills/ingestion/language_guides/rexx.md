# REXX (Restructured Extended Executor) Reference Guide

## Overview

REXX is an interpreted, dynamically-typed scripting language created by IBM, deeply embedded on z/OS (TSO/ISPF). It glues together system services, operates utilities, scripts batch processes, and occasionally implements lightweight calculation routines.

On z/OS, all REXX `.exec` or PDS members must begin with a comment `/* REXX */` to distinguish them from older CLIST formats. REXX evaluates everything as a string. Any standard line not identifiable as a native REXX instruction is immediately relegated to the native OS environment as an executable command.

## Key Constructs

### Program Structure

- `ARG var1 var2`: Implicitly uppercased parameter extraction.
- `PARSE ARG var1 var2`: Case-preserving parameter extraction.
- `EXIT number`: Kills script and passes RC integer back to caller.
- `RETURN var`: Terminates a subroutine/function.

### Data Access & Queues

- **EXECIO**: Primary mechanism for reading disk datasets. `"EXECIO * DISKR infile (STEM LIST. FINIS)"` loads an entire DB table or flat file into `LIST.1` to `LIST.n` with `LIST.0` holding the count.
- **ISPF Storage**: `"ISPEXEC VGET (VAR1) SHARED"` grabs shared variables mapped from online UI screens.
- **Queues**: `QUEUE data` vs `PUSH data` (FIFO vs LIFO). Creates an IPC stack. `PULL val` grabs it. `MAKEBUF` and `DROPBUF` group queue sets natively.

### Control Flow

- `IF / THEN / ELSE`: Supports standard branching.
- `SELECT / WHEN / OTHERWISE`: Switch statement.
- `DO i = 1 TO N`, `DO WHILE x`, `DO FOREVER`.
- `ITERATE` (continue), `LEAVE` (break).

### Parsing (The Core Feature)

```rexx
string = "ACCT190   9050.25 ACTIVE"
PARSE VAR string id 11 amt 19 stat
```

This is a positional parse. `id` = characters 1 to 10. `amt` = characters 11 to 18. `stat` = characters 19+. Absolute parsing is how fixed-width mainframe records are handled instantly.

### Error Trapping

- `SIGNAL ON ERROR`: Acts as a permanent jump table if any OS command returns `RC > 0`. Transfers control definitively to `ERROR:` label.
- `SIGNAL ON NOVALUE`: Catches uninitialized variables across the script. Crucial for tracing literal strings that typo'd into variable evaluations.

## Common Patterns

### Subroutines returning evaluations

```rexx
CALL CheckAcct acctNo
IF RESULT = 'VALID' THEN ...

CheckAcct: PROCEDURE
  PARSE ARG check
  IF length(check) = 10 THEN RETURN 'VALID'
  RETURN 'INVALID'
```

### DB2 Interaction via DSNREXX

```rexx
ADDRESS DSNREXX "EXECSQL PREPARE SQL1 FROM :q"
ADDRESS DSNREXX "EXECSQL OPEN C1"
DO WHILE SQLCODE = 0
  ADDRESS DSNREXX "EXECSQL FETCH C1 INTO :A, :B"
  IF SQLCODE=0 THEN SAY 'Found:' A B
END
```

### Multi-Dimensional Stems

```rexx
grid.1.1 = "TopLeft"
row = 1; col = 1
SAY grid.row.col 
```

Stem variables masquerade as multi-dimensional arrays, using concatenated indices.

## What Carries Business Logic

**Extract facts from these:**

- `PARSE VAR` templates — explicitly decodes the byte-length fields of rigid business datasets.
- `IF / SELECT` conditions containing hard-coded limits or status codes.
- `EXECIO` strings paired with `DISKR/DISKW` indicating input/output data sources.
- `ADDRESS DSNREXX` or `ADDRESS CICS` invocations showing dependencies on native systems.
- Statements that validate input and `EXIT 8` or `SAY "REJECTED"`.

**Skip these (boilerplate):**

- Standard OS allocations `ALLOC FI(X) DA(Y)`.
- Generic ISPF display messages `ISPEXEC SETMSG`.
- `SIGNAL ON` initializations and logging statements `TRACE R`.

## Common Misinterpretations

1. **Unrecognized Text evaluates to OS Execution.** If you type `DELETE DATASET A`, REXX does not throw a syntax error. It assumes `DELETE` is a valid TSO command and attempts to execute it externally on the mainframe.
2. **Variables are all strings.** `x=1` followed by `y='001'` means `x=y` evaluates differently. Using `x == y` is strict string comparison, `x = y` casts to numeric evaluate dynamically.
3. **Parse Variable removes spaces; Parse Positional preserves them.** `PARSE VAR str a b` trims blanks. `PARSE VAR str a 5 b` retains exactly the bytes inside those positions.
4. **Stems are NOT formal arrays.** `Line.1` works, but so does `Line.Name`. `Line.0` storing the count is merely a standard convention adhered to by EXECIO.
5. **SIGNAL destroys DO loops.** `SIGNAL` is a GOTO. Once you signal to `ERROR:`, the script cannot `RETURN` to the inner loop.

## File Naming Conventions

- Extns: PDS members have No extension on zOS. `.rex` `.rexx` `.cmd` locally.
- 1-8 chars, e.g., `FTPPUSH`, `EXTRACTR`.
