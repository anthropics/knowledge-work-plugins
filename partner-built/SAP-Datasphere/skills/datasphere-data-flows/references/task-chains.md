# Task Chains Reference Guide

## Overview

Task Chains orchestrate the execution of multiple data integration objects in SAP Datasphere. They provide scheduling, sequencing, and conditional execution capabilities.

## Orchestration Objects

Task Chains can orchestrate:
- **Replication Flows** - Mass data replication
- **Data Flows** - Batch ETL transformations
- **Transformation Flows** - Delta-aware SQL transformations
- **Other Task Chains** - Nested orchestration
- **BW Bridge Data Flows** - Legacy ABAP logic execution

## Execution Modes

### Serial Execution
Objects execute one after another in sequence:
```
Object A → Object B → Object C
```

### Parallel Execution
Multiple objects execute simultaneously with gate logic:

**AND Gate** - All parallel branches must complete before continuing:
```
     ┌─ Object B ─┐
Object A ─┤           ├─ AND ─ Object D
     └─ Object C ─┘
```

**OR Gate** - First completed branch triggers continuation:
```
     ┌─ Object B ─┐
Object A ─┤           ├─ OR ─ Object D
     └─ Object C ─┘
```

## Status Handling

### On Success
Continue to next object or complete chain.

### On Failure
Options:
- Stop chain execution
- Continue with next branch
- Execute error handling branch

## BW Bridge Integration

Task Chains can include BW Bridge Data Flows for:
- Legacy ABAP transformations
- Complex business logic
- InfoProvider updates

## Scheduling Options

| Schedule Type | Use Case |
|--------------|----------|
| Time-based | Regular intervals (hourly, daily, weekly) |
| Event-based | Triggered by external events |
| Manual | On-demand execution |

## Best Practices

1. **Group Related Flows** - Organize flows that load related data together
2. **Use Parallel Execution** - Independent flows should run in parallel
3. **Implement Error Handling** - Define behavior for each failure scenario
4. **Monitor Execution** - Use Data Integration Monitor to track runs
5. **Consider Dependencies** - Ensure upstream data is available before downstream processing

## Navigation

**Access**: Data Builder → Task Chains (or create new)

**Create**: Data Builder → New Task Chain → Drag objects onto canvas → Connect with execution paths

## Common Patterns

### Daily Load Pattern
```
Morning: Source Extracts (Parallel) → AND → Transformations (Serial) → Facts → Aggregates
```

### Real-time + Batch Hybrid
```
Replication Flows (CDC) run continuously
Task Chain (scheduled): Transformation Flows → Analytics Layer

## What's New (2026.05)

### Output Parameters in Task Chains
Task chain objects now support output parameters, enabling more flexible orchestration:
- **Define output parameters** on task objects (Data Flows, Transformation Flows, etc.)
- **Map output parameters** from a task object to the parent task chain
- **Use in nested task chains** — output parameters propagate upward through the chain hierarchy
- This enables conditional logic and dynamic behavior based on task execution results
```
