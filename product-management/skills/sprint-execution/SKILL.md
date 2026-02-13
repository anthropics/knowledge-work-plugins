---
name: sprint-execution
description: Run sprint reviews, track velocity, prepare demos, interpret burndown charts, and facilitate retrospectives. Use when running a sprint review, preparing a sprint summary, analyzing sprint metrics, facilitating a retrospective, or communicating sprint progress to stakeholders.
---

# Sprint Execution Skill

You are an expert at sprint execution, review, and continuous improvement for product teams. You help product managers run effective sprint ceremonies, communicate progress clearly, and use sprint data to improve team performance.

## Sprint Review Structure

### Purpose
The sprint review is a working session where the team demonstrates what was built and gets feedback from stakeholders. It is NOT a status meeting. The goal is to inspect the increment and adapt the backlog based on feedback.

### Sprint Review Agenda
1. **Sprint Goal Recap** (2 min): Remind everyone what the team set out to accomplish this sprint
2. **Key Accomplishments** (10 min): Demonstrate completed work — live demos preferred over slide decks
3. **Metrics Dashboard** (5 min): Show sprint-level metrics (velocity, completion rate, bug count)
4. **Blockers and Learnings** (5 min): What got in the way, what the team learned
5. **Customer Feedback** (5 min): Any relevant customer reactions to recent releases
6. **Next Sprint Preview** (5 min): What the team plans to work on next
7. **Q&A and Feedback** (10 min): Stakeholder questions and input

### Sprint Summary Document
A written sprint summary should cover:

- **TL;DR**: 2-3 sentence summary of the sprint's outcome
- **Sprint Goal**: What was the goal and was it met (fully, partially, or missed)
- **Completed Work**: List of stories/tasks completed with point values
- **Carried Over**: Items that did not complete, with brief explanation
- **Metrics**: Velocity, planned vs completed, bug count, quality indicators
- **Demo Highlights**: Key features to showcase, with screenshots or links
- **Blockers**: Issues encountered and how they were resolved (or not)
- **Customer Signal**: Relevant customer feedback received during the sprint
- **Next Sprint**: Preview of planned work

## Sprint Metrics

### Velocity
Velocity measures the amount of work completed per sprint, typically in story points.

**How to use velocity**:
- Track as a 3-5 sprint rolling average, not individual sprint values
- Use for capacity planning, not performance evaluation
- Velocity naturally varies sprint-to-sprint by 15-30%. This is normal.
- Velocity is only meaningful within a single team — never compare velocity across teams

**Velocity anti-patterns**:
- Using velocity as a performance metric (incentivizes point inflation)
- Comparing velocity between teams (different teams estimate differently)
- Expecting velocity to increase continuously (teams reach a natural plateau)
- Reacting to single-sprint velocity drops (look at the trend, not the data point)

### Planned vs Completed
Track the ratio of planned story points to completed story points each sprint.

- **90-100% completion**: Team is estimating well and committing appropriately
- **70-90% completion**: Normal range. Some variation is expected.
- **Below 70%**: Pattern suggests over-commitment, poor estimation, or external disruptions
- **Consistently 100%+**: Team may be under-committing or sandbagging estimates

### Sprint Burndown

**How to read a burndown chart**:
- **Ideal**: Smooth downward line from total points to zero
- **Plateau then cliff**: Work is being completed in big batches, not continuously. May indicate large stories that need breaking down.
- **Flat then drops off**: Late starts or blocked work. Investigate what caused the delay.
- **Scope increase (line goes up)**: Work was added mid-sprint. Track how often this happens and why.
- **Ends above zero**: Sprint goal not fully met. Understand what happened before next planning.

**Burndown vs burnup**:
- Burndown shows remaining work (goes down over time)
- Burnup shows completed work AND total scope (both go up). Burnup makes scope changes visible.
- Use burnup when scope changes are common. It shows both progress AND scope creep.

### Bug Metrics
Track bugs at the sprint level:

- **Bugs opened this sprint**: How many new bugs were reported
- **Bugs closed this sprint**: How many bugs the team fixed
- **Bug escape rate**: Bugs found in production vs found in testing
- **Critical bug count**: Bugs that affect core functionality or block users
- **Bug ratio**: % of sprint capacity spent on bugs vs features

A healthy team spends 10-20% of capacity on bugs. Above 30% suggests quality issues that need a dedicated investment.

### Cycle Time
The time from when work starts on a story to when it is done:

- **Short cycle time** (1-3 days): Team is breaking work into small pieces and shipping continuously
- **Long cycle time** (5+ days): Stories may be too large, or work is getting blocked
- Track median cycle time, not average (outliers skew the average)
- Use cycle time to identify bottlenecks: where do items sit the longest?

## Demo Preparation

### What Makes a Good Demo
- **Tell a story**: Frame the demo as a user scenario, not a feature list. "Here's Sarah, a team lead who needs to..."
- **Show, don't tell**: Live product demos beat screenshots, which beat slide decks
- **Keep it short**: 2-3 minutes per feature. Attention drops sharply after 10 minutes.
- **Show the before and after**: If you improved something, show what it used to be like
- **Include edge cases**: Show that error states, empty states, and edge cases are handled
- **Prepare a backup**: Have screenshots or a recording in case the live demo fails

### Demo Anti-Patterns
- Demoing from a development environment with test data (use staging with realistic data)
- Walking through every field on every screen (focus on the key user flows)
- Apologizing for things that are not done ("ignore this part, it is not finished")
- Skipping the "why" (always explain what user problem this solves before showing the solution)
- Letting the demo run long (strict time-boxing keeps energy high)

### Demo for Different Audiences
- **Engineering team**: Show technical details, architecture decisions, interesting implementation challenges
- **Stakeholders/leadership**: Focus on user value, metrics impact, and strategic alignment
- **Customers**: Emphasize how it solves their specific problem. Use their language, not internal terminology.
- **Design team**: Show interaction details, responsiveness, and how edge cases are handled

## Retrospective Facilitation

### Retrospective Formats

**Start, Stop, Continue**:
- **Start**: Things the team should begin doing
- **Stop**: Things that are not working and should be abandoned
- **Continue**: Things that are working well and should keep going

When to use: Default format. Works well for most teams, most of the time.

**4Ls — Liked, Learned, Lacked, Longed For**:
- **Liked**: What went well this sprint
- **Learned**: New knowledge or insights gained
- **Lacked**: What was missing — resources, information, tools
- **Longed For**: Things the team wishes they had

When to use: When you want to go deeper than Start/Stop/Continue. Good for learning-oriented teams.

**Mad, Sad, Glad**:
- **Mad**: Things that frustrated or angered the team
- **Sad**: Things that were disappointing but not infuriating
- **Glad**: Things that went well and made the team happy

When to use: When you want to surface emotional responses. Good for teams going through a difficult period.

**Sailboat**:
- **Wind** (what propels us forward): Positive forces helping the team
- **Anchor** (what holds us back): Negative forces slowing the team
- **Rocks** (risks ahead): Potential problems on the horizon
- **Island** (destination): The goal the team is working toward

When to use: Strategic retrospectives. Good for quarterly reviews or after major milestones.

### Running an Effective Retro
1. **Set the stage** (2 min): Remind the team of the sprint goal and outcomes
2. **Gather data** (10 min): Individual reflection, then share. Use sticky notes or a digital board.
3. **Generate insights** (10 min): Group similar items. Vote on what to discuss.
4. **Decide what to do** (10 min): Pick 1-3 action items. Assign owners and due dates.
5. **Close** (3 min): Thank the team. Confirm action items.

### Retro Anti-Patterns
- **No action items**: A retro without action items is just venting. Always end with concrete next steps.
- **Same issues every sprint**: If the same problems keep appearing, the team is not actually addressing them. Escalate or dedicate time.
- **Blame-oriented**: Retros should focus on systems and processes, not individuals. "The deploy process is slow" not "Bob broke the deploy."
- **Skipping retros**: Teams that skip retros lose the feedback loop. Even a 15-minute retro is better than none.
- **Only negative**: Celebrate wins. Acknowledging what went well is important for team morale and for understanding what to keep doing.

## Sprint Health Indicators

### Healthy Sprint Patterns
- Team consistently meets 70-90% of sprint commitments
- Stories are small enough to complete in 1-3 days
- No single story takes more than half the sprint
- Blockers are identified and resolved within 1-2 days
- Sprint scope changes less than 10% after planning
- Team has time for code review, testing, and quality work

### Warning Signs
- Velocity trending down over 3+ sprints
- Stories consistently carry over sprint after sprint
- More than 30% of capacity spent on bugs or unplanned work
- Team members regularly working overtime to meet commitments
- Burndown chart is flat for 3+ days mid-sprint
- Sprint goals are missed more often than met
- Retrospective action items are never completed

### When to Intervene
- If velocity drops 3 sprints in a row, investigate root cause (team morale, tech debt, unclear requirements)
- If carry-over is chronic, stories are too big or estimates are too optimistic. Break stories down.
- If unplanned work dominates, the team needs a buffer allocation or the incoming request process needs a gate
- If sprint goals miss consistently, the team may be committing to too much or the goals are too ambitious
