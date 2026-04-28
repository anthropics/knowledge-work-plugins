# Consulting PPTX Generation Guide

Reference for generating consulting-grade .pptx files with pptxgenjs. Principles and adaptable code patterns — not fixed styles. Choose colors, fonts, and density based on client, firm, and purpose.

---

## Layout

Default to widescreen for consulting leave-behinds:

```js
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // 13.33" x 7.5"
```

Every content slide has three zones:

| Zone | Height | Purpose |
|------|--------|---------|
| Action title | ~1.0" | Sentence stating the slide's takeaway |
| Body | ~5.0" | Exhibit(s) — charts, tables, frameworks |
| Footer | ~0.5" | Source attribution + page number |

Choose margins and density based on purpose: dense analytical slides get tighter margins, big-idea slides get generous white space.

---

## Slide Anatomy (Non-Negotiable)

The pattern that distinguishes consulting slides from everything else:

1. **Action title** — A complete sentence stating the takeaway. "Revenue declined 12% driven by customer churn" not "Revenue Overview." This is the most important rule.

2. **Exhibit-driven body** — Visual exhibits (charts, tables, frameworks) dominate, not paragraphs or bullets. One focused exhibit is ideal. Two related exhibits side-by-side (e.g. market size + growth rate) works when they jointly support the action title. The exhibit tells the story; text annotates it.

3. **Source line** — Bottom of slide, small font. Data source, date, caveats.

Apply this to every content slide. Title slides, section dividers, and appendix slides are exceptions.

---

## Slide Masters

Three masters as factory functions. `palette` and `fonts` are parameters — the agent picks values per engagement.

### TITLE_SLIDE

```js
function addTitleSlide(pptx, { title, subtitle, date, presenter, palette, fonts }) {
  const slide = pptx.addSlide({ masterName: "TITLE_SLIDE" });
  slide.background = { color: palette.dark };

  slide.addText(title, {
    x: 0.8, y: 2.0, w: 11.7, h: 1.5,
    fontSize: 36, fontFace: fonts.heading,
    color: palette.light, bold: true,
    align: "left",
  });

  slide.addText(subtitle, {
    x: 0.8, y: 3.6, w: 11.7, h: 0.8,
    fontSize: 18, fontFace: fonts.body,
    color: palette.lightMuted,
    align: "left",
  });

  slide.addText(`${presenter}  |  ${date}`, {
    x: 0.8, y: 6.2, w: 11.7, h: 0.4,
    fontSize: 12, fontFace: fonts.body,
    color: palette.lightMuted,
    align: "left",
  });

  return slide;
}
```

### CONTENT_SLIDE

```js
function addContentSlide(pptx, { actionTitle, source, pageNum, palette, fonts }) {
  const slide = pptx.addSlide({ masterName: "CONTENT_SLIDE" });
  slide.background = { color: palette.light };

  // Action title zone
  slide.addText(actionTitle, {
    x: 0.6, y: 0.3, w: 12.1, h: 0.7,
    fontSize: 18, fontFace: fonts.heading,
    color: palette.dark, bold: true,
    align: "left", valign: "top",
  });

  // Thin divider line
  slide.addShape(pptx.ShapeType.line, {
    x: 0.6, y: 1.05, w: 12.1, h: 0,
    line: { color: palette.accent, width: 1.0 },
  });

  // Footer: source + page number
  slide.addText(source, {
    x: 0.6, y: 7.0, w: 10.0, h: 0.3,
    fontSize: 8, fontFace: fonts.body,
    color: palette.muted, italic: true,
    align: "left",
  });
  slide.addText(String(pageNum), {
    x: 11.5, y: 7.0, w: 1.2, h: 0.3,
    fontSize: 8, fontFace: fonts.body,
    color: palette.muted,
    align: "right",
  });

  return slide; // caller adds exhibit(s) to the body zone (y: 1.2, h: ~5.7)
}
```

### SECTION_DIVIDER

```js
function addSectionDivider(pptx, { sectionNumber, sectionTitle, palette, fonts }) {
  const slide = pptx.addSlide({ masterName: "SECTION_DIVIDER" });
  slide.background = { color: palette.dark };

  if (sectionNumber) {
    slide.addText(String(sectionNumber).padStart(2, "0"), {
      x: 0.8, y: 2.0, w: 2.0, h: 1.0,
      fontSize: 48, fontFace: fonts.heading,
      color: palette.accent, bold: true,
      align: "left",
    });
  }

  slide.addText(sectionTitle, {
    x: 0.8, y: 3.2, w: 11.7, h: 1.0,
    fontSize: 28, fontFace: fonts.heading,
    color: palette.light, bold: true,
    align: "left",
  });

  return slide;
}
```

---

## Common Consulting Slide Patterns

Each function accepts content + style parameters. No hardcoded colors. All follow the action-title + exhibit anatomy — call `addContentSlide()` first, then add the exhibit to the returned slide.

### Executive Summary

```js
function addExecSummary(slide, { findings, bottomLine, palette, fonts }) {
  // 4-5 bullet findings
  const bulletText = findings.map((f) => ({
    text: f,
    options: {
      fontSize: 14, fontFace: fonts.body, color: palette.dark,
      bullet: { type: "number" },
      paraSpaceAfter: 8,
    },
  }));

  slide.addText(bulletText, {
    x: 0.6, y: 1.3, w: 12.1, h: 3.5,
    valign: "top",
  });

  // Bottom-line callout box
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.6, y: 5.2, w: 12.1, h: 1.2,
    fill: { color: palette.accentLight },
    rectRadius: 0.1,
  });
  slide.addText(bottomLine, {
    x: 0.9, y: 5.3, w: 11.5, h: 1.0,
    fontSize: 14, fontFace: fonts.body, color: palette.dark,
    bold: true, valign: "middle",
  });
}
```

### Framework / Matrix (2x2)

```js
function addFrameworkMatrix(slide, { quadrants, axisLabels, palette, fonts }) {
  // quadrants: [{ label, items, position: "tl"|"tr"|"bl"|"br" }]
  const positions = {
    tl: { x: 0.8, y: 1.3 }, tr: { x: 7.0, y: 1.3 },
    bl: { x: 0.8, y: 4.0 }, br: { x: 7.0, y: 4.0 },
  };
  const cellW = 5.8, cellH = 2.5;

  quadrants.forEach((q) => {
    const pos = positions[q.position];
    slide.addShape(pptx.ShapeType.rect, {
      x: pos.x, y: pos.y, w: cellW, h: cellH,
      fill: { color: palette.light },
      line: { color: palette.muted, width: 0.5 },
    });
    slide.addText(q.label, {
      x: pos.x + 0.2, y: pos.y + 0.15, w: cellW - 0.4, h: 0.4,
      fontSize: 13, fontFace: fonts.heading,
      color: palette.accent, bold: true,
    });
    const items = q.items.map((item) => ({
      text: item,
      options: { fontSize: 11, fontFace: fonts.body, color: palette.dark, bullet: true },
    }));
    slide.addText(items, {
      x: pos.x + 0.2, y: pos.y + 0.6, w: cellW - 0.4, h: cellH - 0.8,
      valign: "top",
    });
  });

  // Axis labels
  if (axisLabels) {
    slide.addText(axisLabels.x, {
      x: 5.0, y: 6.6, w: 3.3, h: 0.3,
      fontSize: 10, fontFace: fonts.body, color: palette.muted,
      align: "center", italic: true,
    });
    slide.addText(axisLabels.y, {
      x: 0.1, y: 3.5, w: 0.5, h: 2.0,
      fontSize: 10, fontFace: fonts.body, color: palette.muted,
      align: "center", italic: true, rotate: 270,
    });
  }
}
```

### Waterfall / Bridge Chart

Reach for this whenever showing "what drove the change."

```js
function addWaterfallChart(slide, { categories, values, palette }) {
  // values: array of numbers. First = starting total, last = ending total.
  // Middle values are increments/decrements.
  const chartColors = values.map((v, i) =>
    i === 0 || i === values.length - 1
      ? palette.dark
      : v >= 0 ? palette.positive : palette.negative
  );

  slide.addChart(pptx.ChartType.bar, [
    { name: "Change", labels: categories, values: values },
  ], {
    x: 0.8, y: 1.3, w: 11.7, h: 5.2,
    showValue: true,
    valueFontSize: 10,
    catAxisOrientation: "minMax",
    valAxisHidden: false,
    valAxisMajorGridlines: { color: "E0E0E0", width: 0.5 },
    valAxisMinorGridlines: false,
    chartColors: chartColors,
    showLegend: false,
  });
}
```

### Comparison Table

```js
function addComparisonTable(slide, { headers, rows, palette, fonts }) {
  const tableRows = [
    headers.map((h) => ({
      text: h,
      options: {
        fontSize: 11, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "center",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    })),
    ...rows.map((row, i) =>
      row.map((cell) => ({
        text: cell,
        options: {
          fontSize: 10, fontFace: fonts.body, color: palette.dark,
          fill: { color: i % 2 === 0 ? palette.light : palette.altRow },
          border: { type: "solid", color: "E0E0E0", pt: 0.5 },
          align: "left", valign: "middle",
        },
      }))
    ),
  ];

  slide.addTable(tableRows, {
    x: 0.6, y: 1.3, w: 12.1,
    colW: Array(headers.length).fill(12.1 / headers.length),
    rowH: [0.45, ...Array(rows.length).fill(0.4)],
    autoPage: true,
    autoPageRepeatHeader: true,
  });
}
```

### Roadmap / Timeline

```js
function addRoadmap(slide, { phases, palette, fonts }) {
  // phases: [{ label, duration, milestones: string[] }]
  const phaseW = 11.7 / phases.length;
  const startX = 0.8;

  phases.forEach((phase, i) => {
    const x = startX + i * phaseW;

    // Phase bar
    slide.addShape(pptx.ShapeType.rect, {
      x: x + 0.05, y: 1.5, w: phaseW - 0.1, h: 0.7,
      fill: { color: i % 2 === 0 ? palette.accent : palette.accentLight },
      rectRadius: 0.05,
    });
    slide.addText(phase.label, {
      x: x + 0.1, y: 1.55, w: phaseW - 0.2, h: 0.6,
      fontSize: 12, fontFace: fonts.heading, color: palette.light,
      bold: true, align: "center", valign: "middle",
    });

    // Duration
    slide.addText(phase.duration, {
      x: x + 0.1, y: 2.3, w: phaseW - 0.2, h: 0.3,
      fontSize: 9, fontFace: fonts.body, color: palette.muted,
      align: "center",
    });

    // Milestones
    const msText = phase.milestones.map((m) => ({
      text: m,
      options: {
        fontSize: 10, fontFace: fonts.body, color: palette.dark,
        bullet: { code: "2022" }, paraSpaceAfter: 4,
      },
    }));
    slide.addText(msText, {
      x: x + 0.1, y: 2.7, w: phaseW - 0.2, h: 3.5,
      valign: "top",
    });
  });
}
```

### Big Number Callout

```js
function addBigNumber(slide, { metrics, palette, fonts }) {
  // metrics: [{ value, label, sublabel? }] — 1 to 3 items
  const count = metrics.length;
  const cellW = 11.7 / count;
  const startX = 0.8;

  metrics.forEach((m, i) => {
    const x = startX + i * cellW;

    slide.addText(m.value, {
      x, y: 2.0, w: cellW, h: 1.8,
      fontSize: 54, fontFace: fonts.heading,
      color: palette.accent, bold: true,
      align: "center", valign: "bottom",
    });
    slide.addText(m.label, {
      x, y: 3.9, w: cellW, h: 0.6,
      fontSize: 16, fontFace: fonts.body,
      color: palette.dark, bold: true,
      align: "center", valign: "top",
    });
    if (m.sublabel) {
      slide.addText(m.sublabel, {
        x, y: 4.5, w: cellW, h: 0.5,
        fontSize: 11, fontFace: fonts.body,
        color: palette.muted,
        align: "center",
      });
    }
  });
}
```

### Before / After Split

```js
function addBeforeAfter(slide, { before, after, palette, fonts }) {
  // before/after: { title, points: string[] }
  const colW = 5.7;

  [
    { data: before, x: 0.6, headerColor: palette.muted },
    { data: after, x: 6.8, headerColor: palette.accent },
  ].forEach(({ data, x, headerColor }) => {
    slide.addShape(pptx.ShapeType.rect, {
      x, y: 1.3, w: colW, h: 0.6,
      fill: { color: headerColor },
    });
    slide.addText(data.title, {
      x: x + 0.2, y: 1.35, w: colW - 0.4, h: 0.5,
      fontSize: 14, fontFace: fonts.heading,
      color: palette.light, bold: true,
      align: "center", valign: "middle",
    });

    const points = data.points.map((p) => ({
      text: p,
      options: {
        fontSize: 12, fontFace: fonts.body, color: palette.dark,
        bullet: true, paraSpaceAfter: 6,
      },
    }));
    slide.addText(points, {
      x: x + 0.2, y: 2.1, w: colW - 0.4, h: 4.3,
      valign: "top",
    });
  });

  // Vertical divider
  slide.addShape(pptx.ShapeType.line, {
    x: 6.65, y: 1.3, w: 0, h: 5.2,
    line: { color: palette.muted, width: 0.5, dashType: "dash" },
  });
}
```

### Harvey Ball Assessment

Capability or maturity assessment using filled circles. Common for "current state vs target state" or vendor/option scoring across multiple dimensions.

```js
function addHarveyBallAssessment(slide, { dimensions, entities, ratings, palette, fonts }) {
  // dimensions: string[] — row labels (e.g. ["Data Quality", "Governance", "Analytics"])
  // entities: string[] — column headers (e.g. ["Current", "Target"] or ["Vendor A", "Vendor B"])
  // ratings: number[][] — values 0-4 per dimension per entity (0=empty, 1=quarter, 2=half, 3=three-quarter, 4=full)
  const harveyBalls = ["○", "◔", "◐", "◕", "●"];
  const colCount = 1 + entities.length;
  const dimColW = 3.5;
  const entityColW = (12.1 - dimColW) / entities.length;
  const colWidths = [dimColW, ...Array(entities.length).fill(entityColW)];

  // Header row
  const headerRow = [
    {
      text: "Dimension",
      options: {
        fontSize: 11, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "left",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    },
    ...entities.map((e) => ({
      text: e,
      options: {
        fontSize: 11, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "center",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    })),
  ];

  // Data rows
  const dataRows = dimensions.map((dim, i) => [
    {
      text: dim,
      options: {
        fontSize: 10, fontFace: fonts.body, color: palette.dark,
        fill: { color: i % 2 === 0 ? palette.light : palette.altRow },
        border: { type: "solid", color: "E0E0E0", pt: 0.5 },
        align: "left", valign: "middle",
      },
    },
    ...ratings[i].map((r) => ({
      text: harveyBalls[r],
      options: {
        fontSize: 18, fontFace: fonts.body, color: palette.accent,
        fill: { color: i % 2 === 0 ? palette.light : palette.altRow },
        border: { type: "solid", color: "E0E0E0", pt: 0.5 },
        align: "center", valign: "middle",
      },
    })),
  ]);

  slide.addTable([headerRow, ...dataRows], {
    x: 0.6, y: 1.3, w: 12.1,
    colW: colWidths,
    rowH: [0.45, ...Array(dimensions.length).fill(0.45)],
    autoPage: true,
    autoPageRepeatHeader: true,
  });

  // Legend
  const legendText = harveyBalls.map((b, i) => `${b} ${["None", "Low", "Moderate", "High", "Full"][i]}`).join("    ");
  slide.addText(legendText, {
    x: 0.6, y: 6.5, w: 12.1, h: 0.3,
    fontSize: 9, fontFace: fonts.body, color: palette.muted,
    align: "left",
  });
}
```

### RACI Matrix

Responsibility assignment matrix. Bold "A" (Accountable) draws the eye to single-point accountability. Common in operating model and org design work.

```js
function addRACIMatrix(slide, { activities, roles, assignments, palette, fonts }) {
  // activities: string[] — row labels (e.g. ["Budget approval", "Vendor selection"])
  // roles: string[] — column headers (e.g. ["CFO", "VP Ops", "PM", "Legal"])
  // assignments: string[][] — "R", "A", "C", "I", or "" per activity per role
  const raciColors = {
    A: palette.accent,
    R: palette.dark,
    C: palette.muted,
    I: palette.muted,
  };
  const raciBold = { A: true, R: false, C: false, I: false };

  const actColW = 3.2;
  const roleColW = (12.1 - actColW) / roles.length;
  const colWidths = [actColW, ...Array(roles.length).fill(roleColW)];

  // Header row
  const headerRow = [
    {
      text: "Activity",
      options: {
        fontSize: 11, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "left",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    },
    ...roles.map((r) => ({
      text: r,
      options: {
        fontSize: 10, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "center",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    })),
  ];

  // Data rows
  const dataRows = activities.map((act, i) => [
    {
      text: act,
      options: {
        fontSize: 10, fontFace: fonts.body, color: palette.dark,
        fill: { color: i % 2 === 0 ? palette.light : palette.altRow },
        border: { type: "solid", color: "E0E0E0", pt: 0.5 },
        align: "left", valign: "middle",
      },
    },
    ...assignments[i].map((val) => ({
      text: val || "",
      options: {
        fontSize: 13, fontFace: fonts.heading,
        color: raciColors[val] || palette.muted,
        bold: raciBold[val] || false,
        fill: { color: val === "A" ? palette.accentLight : (i % 2 === 0 ? palette.light : palette.altRow) },
        border: { type: "solid", color: "E0E0E0", pt: 0.5 },
        align: "center", valign: "middle",
      },
    })),
  ]);

  slide.addTable([headerRow, ...dataRows], {
    x: 0.6, y: 1.3, w: 12.1,
    colW: colWidths,
    rowH: [0.45, ...Array(activities.length).fill(0.4)],
    autoPage: true,
    autoPageRepeatHeader: true,
  });

  // Legend
  slide.addText(
    "R = Responsible  |  A = Accountable  |  C = Consulted  |  I = Informed",
    {
      x: 0.6, y: 6.5, w: 12.1, h: 0.3,
      fontSize: 9, fontFace: fonts.body, color: palette.muted,
      align: "left",
    }
  );
}
```

### RAG Status Dashboard

Red/Amber/Green traffic light dashboard for steering committee decks. Shows status across multiple workstreams or dimensions (schedule, budget, scope, quality, resources).

```js
function addRAGDashboard(slide, { workstreams, dimensions, statuses, comments, palette, fonts }) {
  // workstreams: string[] — row labels (e.g. ["Data Migration", "Integration", "Testing"])
  // dimensions: string[] — status dimensions (e.g. ["Schedule", "Budget", "Scope", "Quality"])
  // statuses: string[][] — "R", "A", "G" per workstream per dimension
  // comments: string[] — one comment per workstream (optional, pass [] to omit)
  const ragFills = {
    R: "CC3333",
    A: "F5A623",
    G: "4CAF50",
  };
  const ragLabels = { R: "●", A: "●", G: "●" };

  const hasComments = comments && comments.length > 0;
  const wsColW = 2.8;
  const dimColW = 1.4;
  const commentColW = hasComments ? 12.1 - wsColW - (dimColW * dimensions.length) : 0;
  const colWidths = [wsColW, ...Array(dimensions.length).fill(dimColW), ...(hasComments ? [commentColW] : [])];

  // Header row
  const headerRow = [
    {
      text: "Workstream",
      options: {
        fontSize: 10, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "left",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    },
    ...dimensions.map((d) => ({
      text: d,
      options: {
        fontSize: 9, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "center",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    })),
    ...(hasComments ? [{
      text: "Commentary",
      options: {
        fontSize: 10, fontFace: fonts.heading, color: palette.light,
        bold: true, fill: { color: palette.dark }, align: "left",
        border: { type: "solid", color: palette.dark, pt: 0.5 },
      },
    }] : []),
  ];

  // Data rows
  const dataRows = workstreams.map((ws, i) => {
    const rowBg = i % 2 === 0 ? palette.light : palette.altRow;
    return [
      {
        text: ws,
        options: {
          fontSize: 10, fontFace: fonts.body, color: palette.dark, bold: true,
          fill: { color: rowBg },
          border: { type: "solid", color: "E0E0E0", pt: 0.5 },
          align: "left", valign: "middle",
        },
      },
      ...statuses[i].map((s) => ({
        text: ragLabels[s] || "",
        options: {
          fontSize: 16, color: ragFills[s] || palette.muted,
          fill: { color: rowBg },
          border: { type: "solid", color: "E0E0E0", pt: 0.5 },
          align: "center", valign: "middle",
        },
      })),
      ...(hasComments ? [{
        text: comments[i] || "",
        options: {
          fontSize: 9, fontFace: fonts.body, color: palette.dark,
          fill: { color: rowBg },
          border: { type: "solid", color: "E0E0E0", pt: 0.5 },
          align: "left", valign: "middle",
        },
      }] : []),
    ];
  });

  slide.addTable([headerRow, ...dataRows], {
    x: 0.6, y: 1.3, w: 12.1,
    colW: colWidths,
    rowH: [0.45, ...Array(workstreams.length).fill(0.45)],
    autoPage: true,
    autoPageRepeatHeader: true,
  });

  // Legend
  slide.addText([
    { text: "●", options: { fontSize: 12, color: ragFills.G } },
    { text: " On Track    ", options: { fontSize: 9, fontFace: fonts.body, color: palette.muted } },
    { text: "●", options: { fontSize: 12, color: ragFills.A } },
    { text: " At Risk    ", options: { fontSize: 9, fontFace: fonts.body, color: palette.muted } },
    { text: "●", options: { fontSize: 12, color: ragFills.R } },
    { text: " Off Track", options: { fontSize: 9, fontFace: fonts.body, color: palette.muted } },
  ], {
    x: 0.6, y: 6.5, w: 12.1, h: 0.3,
    align: "left",
  });
}
```

### Gantt Timeline

Phased implementation timeline with workstreams, bars, milestones, and dependency arrows. The standard planning slide in consulting. Builds a grid-based Gantt using shapes — no chart API needed.

```js
function addGanttTimeline(slide, { periods, workstreams, milestones, palette, fonts }) {
  // periods: string[] — column headers (e.g. ["Q1 '25", "Q2 '25", "Q3 '25", "Q4 '25", "Q1 '26"])
  // workstreams: [{ label, startIdx, endIdx, color? }] — bar spans across period indices (0-based)
  // milestones: [{ label, periodIdx, y? }] — diamond markers at specific periods
  const gridX = 3.0;
  const gridY = 1.5;
  const gridW = 9.5;
  const gridH = 4.8;
  const labelW = 2.2;
  const periodW = gridW / periods.length;
  const rowH = gridH / Math.max(workstreams.length, 1);

  // Period headers
  periods.forEach((p, i) => {
    slide.addText(p, {
      x: gridX + i * periodW, y: 1.15, w: periodW, h: 0.35,
      fontSize: 9, fontFace: fonts.heading, color: palette.dark,
      bold: true, align: "center", valign: "middle",
    });
  });

  // Header underline
  slide.addShape(pptx.ShapeType.line, {
    x: gridX, y: gridY, w: gridW, h: 0,
    line: { color: palette.dark, width: 1.0 },
  });

  // Vertical period dividers (light)
  periods.forEach((_, i) => {
    if (i > 0) {
      slide.addShape(pptx.ShapeType.line, {
        x: gridX + i * periodW, y: gridY, w: 0, h: gridH,
        line: { color: "E0E0E0", width: 0.5, dashType: "dash" },
      });
    }
  });

  // Workstream rows
  workstreams.forEach((ws, i) => {
    const rowY = gridY + i * rowH;
    const barY = rowY + rowH * 0.3;
    const barH = rowH * 0.4;

    // Alternating row background
    if (i % 2 === 1) {
      slide.addShape(pptx.ShapeType.rect, {
        x: gridX, y: rowY, w: gridW, h: rowH,
        fill: { color: palette.altRow },
        line: { width: 0 },
      });
    }

    // Workstream label
    slide.addText(ws.label, {
      x: 0.6, y: rowY, w: labelW, h: rowH,
      fontSize: 10, fontFace: fonts.body, color: palette.dark,
      bold: true, align: "left", valign: "middle",
    });

    // Gantt bar
    const barStartX = gridX + ws.startIdx * periodW;
    const barW = (ws.endIdx - ws.startIdx + 1) * periodW - 0.1;
    slide.addShape(pptx.ShapeType.rect, {
      x: barStartX + 0.05, y: barY, w: barW, h: barH,
      fill: { color: ws.color || palette.accent },
      rectRadius: 0.05,
    });

    // Bar label (inside bar if wide enough, otherwise skip)
    if (ws.endIdx - ws.startIdx >= 1) {
      slide.addText(ws.label, {
        x: barStartX + 0.1, y: barY, w: barW - 0.1, h: barH,
        fontSize: 8, fontFace: fonts.body, color: palette.light,
        align: "left", valign: "middle",
      });
    }
  });

  // Milestones (diamond markers)
  milestones.forEach((ms) => {
    const msX = gridX + (ms.periodIdx + 0.5) * periodW;
    const msY = ms.y || (gridY + gridH + 0.15);

    slide.addText("◆", {
      x: msX - 0.15, y: msY - 0.15, w: 0.3, h: 0.3,
      fontSize: 14, color: palette.accent,
      align: "center", valign: "middle",
    });
    slide.addText(ms.label, {
      x: msX + 0.2, y: msY - 0.12, w: 2.5, h: 0.25,
      fontSize: 8, fontFace: fonts.body, color: palette.dark,
      align: "left", valign: "middle",
    });
  });
}
```

---

## Chart Styling Principles

Not specific colors — principles for professional appearance:

- **Clean backgrounds**: Remove default chart borders and backgrounds. White or transparent.
- **Subtle gridlines**: Horizontal only (`valAxisMajorGridlines: { color: "E0E0E0" }`). Hide vertical gridlines.
- **Muted axis labels**: Use the palette's secondary text color, not black. Keep font size small (8-9pt).
- **Data labels on bars/columns**: More readable than forcing people to trace to the axis. `showValue: true, valueFontSize: 10`.
- **Limited palette**: 2-3 colors from the chosen palette per chart. More dilutes the message.
- **No legend for single-series**: `showLegend: false` when there's only one data series.
- **Number formatting**: Use abbreviated formats for large numbers (e.g. "$1.2M" not "$1,200,000"). Apply `valAxisNumFmt` or format data labels.

---

## Adapting to Context

Choose styling based on the situation:

| Context | Approach |
|---------|----------|
| **Client-branded deck** | Ask for or infer brand colors; use as the palette. Match the client's font if known. |
| **Firm-branded deck** | Use the consulting firm's visual identity if known. |
| **Neutral / independent** | Pick a palette that fits the topic. |
| **Projected presentation** | Larger fonts (min 18pt body), fewer elements per slide, high contrast. |
| **Leave-behind document** | Denser layout allowed, smaller fonts (12-14pt body), more detail per slide. |
| **Analytical deep-dive** | Dense exhibits, detailed tables, tighter margins. |
| **Recommendation / big idea** | Generous white space, large type, one message per slide. |

Slide density varies by purpose. An analytical slide can pack data. A recommendation slide should breathe. Don't apply one density everywhere.
