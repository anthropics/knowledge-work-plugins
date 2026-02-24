# Health Data Analysis Track Specification

## Overview

Health data analysis and reporting workflows for epidemiological analyses, population health, and formatted outputs including statistical reports and visualizations.

## Scope

### Analysis Types
- Descriptive epidemiology
- Analytical epidemiology (cohort, case-control)
- Survival analysis
- Trend analysis
- Population health metrics

### Outputs
- Epidemiological reports
- Forest plots
- Survival curves (Kaplan-Meier)
- Population dashboards
- Statistical tables

### Tools Integration
- Statistical analysis (R, Python patterns)
- Visualization (matplotlib, seaborn, plotly)
- Document generation (xlsx, pdf)

## Deliverables

### Skills
- `health-data-report` - Health data analysis and reporting

### Commands
- `/analyze-health-data` - Initiate health data analysis

## Dependencies

- `health-core` (plugin structure)
- `health-coding` (for coded datasets)

## Adapts From

- `data/statistical-analysis` - Statistical methods
- `data/data-visualization` - Visualization patterns
- `document-skills/xlsx` - Spreadsheet outputs
- `document-skills/pdf` - Report generation

## Success Criteria

- [ ] Guides epidemiological analysis selection
- [ ] Supports standard health metrics
- [ ] Generates formatted statistical outputs
- [ ] Creates publication-ready visualizations
- [ ] Produces structured reports
