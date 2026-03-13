# IDMS (Integrated Database Management System) Reference Guide

## Overview

IDMS is a network-model (CODASYL) database management system running on IBM mainframes since the 1970s. It is distinctly **NOT relational**. There are no tables, no foreign keys, and no SQL JOINs.

IDMS structures data via **Records** connected by **Sets** (physical linked lists representing one-to-many relationships). Programs interact with IDMS navigationally, moving a "Currency Pointer" precisely through the network graph.

Logic is typically written in **COBOL-DML** (COBOL with embedded native DB traversal commands) or **ADS/Online** (a native 4GL dialog system).

## Key Constructs

### Program Structure

- **SCHEMA**: The global database map.
- **SUBSCHEMA**: The subset map bound to this specific program. `MOVE 'SS-NAME' TO SUBSCHEMA-ID` authorizes access.
- **IDMS COMMUNICATIONS BLOCK**: Global error and status array. `ERROR-STATUS` dictates the result of every step.

### Data Access (Navigating the Network)

Because there are no JOINs, you must "walk" the database graph physically using DML (Data Manipulation Language).

- `OBTAIN CALC record`: The fastest entry point. Looks up a root record via a hashing algorithm on its primary key.
- `OBTAIN NEXT record WITHIN set`: Walks forward through the linked list of children owned by the current parent.
- `OBTAIN OWNER WITHIN set`: Navigates backwards from a child to its parent record.
- `FIND`: Moves the currency pointer through the network without actually fetching the data into COBOL memory (highly optimized check).
- `STORE`: Inserts a new record *and automatically connects it* to all mandatory Sets.
- `MODIFY`: Updates the record under the current currency pointer.
- `ERASE`: Deletes the current record (`ERASE PERMANENT` physically cascades down to delete all child members in owned sets).

### Control Flow and Error Handling

- `ERROR-STATUS`: Evaluated after *every* DML verb.
  - `0000` = Success
  - `0326` = End of Set (No more children to loop through)
  - `0306` = CALC Not Found (Primary key doesn't exist)
  - `0069` = Deadlock
- Standard `PERFORM IDMS-STATUS` paragraphs wrap global abort logic.

### ADS/Online Dialogs

A unique 4GL environment specifically for IDMS terminal screens.

- **Premap Process**: Code executed before drawing the UI.
- **Response Process**: Code executed after the user hits Enter.
- Commands: `LINK TO DIALOG 'Menu'`, `DISPLAY AND WAIT`, `IF ... LEAVE`.

## Common Patterns

### The Root Entry Lookup (CALC)

```cobol
MOVE '12345' TO CUST-ID.
OBTAIN CALC CUSTOMER.
IF DB-STAT-OK
   PERFORM EXISTING-CUST-LOGIC
ELSE
   IF DB-REC-NOT-FOUND
      PERFORM NEW-CUST-LOGIC
   END-IF
END-IF.
```

### Walking the Graph (Parent to Children Iteration)

```cobol
OBTAIN CALC CUSTOMER.
PERFORM UNTIL DB-END-OF-SET
   OBTAIN NEXT ORDER WITHIN CUST-ORDER-SET
   IF DB-STAT-OK
      ADD ORDER-TOTAL TO WS-CUST-GRAND-TOTAL
   END-IF
END-PERFORM.
```

This replaces a `SELECT * FROM ORDERS WHERE CUSTID = 12345`. Instead of a query, the program physically traverses the `CUST-ORDER-SET` linked list until it hits the end (`0326`).

### Walking Upwards (Child to Parent)

```cobol
OBTAIN CALC ORDER.
OBTAIN OWNER WITHIN CUST-ORDER-SET.
DISPLAY CUST-NAME.
```

There is no Foreign Key on the `ORDER` record holding the Customer ID. The program navigates the internal `OWNER` pointer backwards up the hierarchy to find out who owns the order.

## What Carries Business Logic

**Extract facts from these:**

- `OBTAIN CALC` targets — what are the primary entry entities into the business workflow?
- `OBTAIN NEXT WITHIN` loops — how does the logic aggregate or evaluate children datasets?
- `IF ERROR-STATUS =` checks — specifically handling `0306` (Missing) vs `0326` (End of line) maps to explicit business pathways.
- `STORE / ERASE` execution blocks — where does data mutate, and does it use `ERASE PERMANENT` (cascading business deletion)?
- ADS `Response` processes — these house the strict validation rules applied against human input.

**Skip these (boilerplate):**

- Generic `PERFORM IDMS-STATUS` abort evaluations.
- `BIND RUN-UNIT` / `READY` / `FINISH` transaction lifecycle setup.

## Common Misinterpretations

1. **IDMS is not relational SQL.** Do not frame analysis around "Tables" or "Foreign Keys". `CUST-ORDER-SET` is a physical linked list traversal.
2. **Currency is implicit global state.** `MODIFY` updates whatever the database currently points at. If an intervening paragraph does a `FIND` on a different record, currency shifts invisibly.
3. **OBTAIN is not a bulk SELECT.** `OBTAIN CALC CUSTOMER` fetches exactly 1 record. Loops are mandatory to fetch sets.
4. **0326 and 0306 are standard flow, not fatal errors.** Trapping `0326` (End of Set) is the correct way to terminate a `WHILE` loop in IDMS. It is not an exception.
5. **STORE auto-wires relationships.** A `STORE ORDER` command implicitly wires the Order into the `CUST-ORDER-SET` if currency was already established on the Customer.
6. **FIND vs OBTAIN.** `FIND` locates the record in the DB engine but leaves COBOL's memory empty. `OBTAIN` locates it and moves the bytes into Working Storage.

## File Naming Conventions

- Extns: `.cbl`, `.cob`.
- Dialogs: Often stored internally in the Integrated Data Dictionary (IDD) rather than raw text files. Mapped as `dialog.PREMAP` or `dialog.RESPONSE`.
