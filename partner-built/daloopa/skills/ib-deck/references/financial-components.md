# Financial Components

Reusable HTML+CSS components for deck slides. All components use design system CSS custom properties.

## KPI Callout Row

4-6 highlighted metrics displayed in boxes across the top of a slide.

```html
<div style="display: flex; gap: 12px; margin-bottom: 20px;">
    <div style="flex: 1; background: var(--light-gray); padding: 14px 12px; border-radius: 4px; text-align: center; border-top: 3px solid var(--navy);">
        <div style="font-size: 9px; color: var(--dark-gray); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Market Cap</div>
        <div style="font-size: 20px; font-weight: 700; color: var(--navy);">$3.4T</div>
    </div>
    <!-- Repeat for each KPI -->
</div>
```

## Dense Financial Table

For income statements, balance sheets, cash flow. Supports row grouping and subtotals.

```html
<table style="width: 100%; border-collapse: collapse; font-size: 10px; font-variant-numeric: tabular-nums;">
    <thead>
        <tr style="background: var(--navy); color: white;">
            <th style="padding: 6px 8px; text-align: left; font-size: 9px; text-transform: uppercase; letter-spacing: 0.5px;">Metric</th>
            <th style="padding: 6px 8px; text-align: right;">Q1 2024</th>
            <th style="padding: 6px 8px; text-align: right;">Q2 2024</th>
            <!-- More columns -->
        </tr>
    </thead>
    <tbody>
        <!-- Regular row -->
        <tr>
            <td style="padding: 4px 8px; border-bottom: 1px solid var(--mid-gray);">Revenue</td>
            <td style="padding: 4px 8px; text-align: right; border-bottom: 1px solid var(--mid-gray);">$94,836</td>
            <!-- More cells -->
        </tr>
        <!-- Sub-row (growth rate, italic) -->
        <tr style="background: var(--light-gray);">
            <td style="padding: 3px 8px 3px 16px; font-style: italic; color: var(--dark-gray); border-bottom: 1px solid var(--mid-gray); font-size: 9px;">YoY Growth</td>
            <td style="padding: 3px 8px; text-align: right; font-style: italic; color: var(--green); border-bottom: 1px solid var(--mid-gray); font-size: 9px;">+5.5%</td>
            <!-- More cells -->
        </tr>
        <!-- Subtotal/bold row -->
        <tr style="border-top: 2px solid var(--navy);">
            <td style="padding: 4px 8px; font-weight: 700; border-bottom: 1px solid var(--mid-gray);">Operating Income</td>
            <td style="padding: 4px 8px; text-align: right; font-weight: 700; border-bottom: 1px solid var(--mid-gray);">$29,412</td>
            <!-- More cells -->
        </tr>
        <!-- Margin row -->
        <tr style="background: var(--light-gray);">
            <td style="padding: 3px 8px 3px 16px; font-style: italic; color: var(--dark-gray); font-size: 9px;">Margin</td>
            <td style="padding: 3px 8px; text-align: right; color: var(--dark-gray); font-size: 9px;">31.0%</td>
            <!-- More cells -->
        </tr>
    </tbody>
</table>
```

## Sensitivity Matrix

Color-coded WACC vs terminal growth. Green = above current price, red = below.

```html
<table style="width: 100%; border-collapse: collapse; font-size: 10px; text-align: center; font-variant-numeric: tabular-nums;">
    <thead>
        <tr style="background: var(--navy); color: white;">
            <th style="padding: 6px;">WACC \ TGR</th>
            <th style="padding: 6px;">1.5%</th>
            <th style="padding: 6px;">2.0%</th>
            <!-- More columns -->
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 6px; font-weight: 700; background: var(--light-gray);">8.0%</td>
            <td style="padding: 6px; background: #D4EDDA; color: var(--near-black);">$245</td>
            <!-- Green bg for above current, red bg for below -->
            <td style="padding: 6px; background: #F8D7DA; color: var(--near-black);">$185</td>
        </tr>
    </tbody>
</table>
```

Use `#D4EDDA` (light green) for upside, `#F8D7DA` (light red) for downside. Bold the base case cell.

## Horizontal Bar Chart (CSS-only)

For peer comparisons, valuation ranges. No JavaScript needed.

```html
<div style="display: flex; flex-direction: column; gap: 8px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 100px; font-size: 11px; text-align: right; color: var(--near-black);">Peer A</div>
        <div style="flex: 1; background: var(--mid-gray); height: 24px; border-radius: 3px; position: relative;">
            <div style="width: 75%; height: 100%; background: var(--navy); border-radius: 3px;"></div>
            <span style="position: absolute; right: 8px; top: 4px; font-size: 10px; font-weight: 600;">18.5x</span>
        </div>
    </div>
    <!-- Repeat for each bar -->
</div>
```

## Vertical Bar Chart (CSS-only)

For time-series financial data.

```html
<div style="display: flex; align-items: flex-end; gap: 8px; height: 200px; border-bottom: 1px solid var(--mid-gray); padding-bottom: 4px;">
    <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;">
        <div style="font-size: 9px; font-weight: 600; margin-bottom: 4px;">$94.8B</div>
        <div style="width: 80%; height: 85%; background: var(--navy); border-radius: 3px 3px 0 0;"></div>
        <div style="font-size: 9px; color: var(--dark-gray); margin-top: 4px;">Q1'24</div>
    </div>
    <!-- Repeat for each bar, adjust height % proportionally -->
</div>
```

## Waterfall Chart (CSS-only)

Bridge from base to target value.

```html
<div style="display: flex; align-items: flex-end; gap: 6px; height: 250px; position: relative;">
    <!-- Base bar (full height from bottom) -->
    <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;">
        <div style="font-size: 9px; font-weight: 600; margin-bottom: 4px;">$100B</div>
        <div style="width: 70%; height: 60%; background: var(--navy); border-radius: 3px 3px 0 0;"></div>
        <div style="font-size: 9px; color: var(--dark-gray); margin-top: 4px;">Base</div>
    </div>
    <!-- Positive increment (floating bar) -->
    <div style="flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; height: 100%;">
        <div style="position: absolute; bottom: 60%; width: 70%; height: 10%; background: var(--green); border-radius: 3px;">
            <span style="position: absolute; top: -16px; left: 50%; transform: translateX(-50%); font-size: 9px; font-weight: 600; color: var(--green);">+$15B</span>
        </div>
        <div style="position: absolute; bottom: 0; font-size: 9px; color: var(--dark-gray);">Organic</div>
    </div>
    <!-- Negative decrement -->
    <div style="flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; height: 100%;">
        <div style="position: absolute; bottom: 67%; width: 70%; height: 5%; background: var(--red); border-radius: 3px;">
            <span style="position: absolute; top: -16px; left: 50%; transform: translateX(-50%); font-size: 9px; font-weight: 600; color: var(--red);">-$3B</span>
        </div>
        <div style="position: absolute; bottom: 0; font-size: 9px; color: var(--dark-gray);">FX</div>
    </div>
</div>
```

Note: For waterfall charts, it's often easier to use the `chart_generator.py waterfall` type and embed the PNG image, rather than building pure CSS waterfalls.

## Pie/Donut Chart (CSS-only)

Simple segment breakdown using CSS conic-gradient.

```html
<div style="display: flex; gap: 30px; align-items: center;">
    <div style="width: 180px; height: 180px; border-radius: 50%; background: conic-gradient(var(--navy) 0% 45%, var(--steel-blue) 45% 70%, var(--gold) 70% 88%, var(--dark-gray) 88% 100%);"></div>
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 12px; height: 12px; background: var(--navy); border-radius: 2px;"></div>
            <span style="font-size: 11px;">iPhone — 45%</span>
        </div>
        <!-- Repeat for each segment -->
    </div>
</div>
```

## Commentary Block

Gray background box with steel-blue left border. Use after every data table or chart.

```html
<div style="background: var(--light-gray); border-left: 4px solid var(--steel-blue); padding: 12px 16px; margin: 12px 0; font-size: 11px; line-height: 1.6;">
    <strong>Key Takeaway:</strong> Revenue accelerated to +6.1% YoY, driven by the iPhone 16 cycle. Operating margins expanded +150bps to 31.0%, suggesting improved cost discipline. Watch for sustainability in Q2 as seasonal tailwinds fade.
</div>
```

## Football Field (CSS-only)

See `ib-advisory-patterns.md` for data format. For best results, use `chart_generator.py football-field` and embed the PNG.
