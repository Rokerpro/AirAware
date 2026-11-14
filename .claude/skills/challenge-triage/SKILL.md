---
name: challenge-triage
description: Turn a hackathon challenge brief into a scoped plan. Use when a brief, track description or judging rubric arrives, to extract the problem, users, requirements, judging criteria, constraints and prohibited approaches, define the MVP and success metrics, and produce a 48-hour plan.
---

# Challenge triage

Read the brief before choosing any technology. Do not assume a track, domain or stack the brief does not state.

## Workflow
1. Read the whole brief, rubric and rules (and CLAUDE.md). Quote the brief for every requirement you extract.
2. Extract: problem statement, target users, required features, required deliverables, judging criteria and their weights, deadlines.
3. List constraints (time, data, compute, team skills) and prohibited or restricted approaches (e.g. data rules, pre-built work, disclosure rules).
4. Mark anything ambiguous as an open question for the user; do not guess the answer.
5. Define the MVP: the smallest end-to-end product that meets every hard requirement.
6. Define measurable success criteria: one primary metric, the baseline it must beat, and a demo-able user flow.
7. Write a 48-hour plan in time blocks, with an owner per task, a "working end-to-end" checkpoint by the halfway mark, and a feature freeze well before the deadline.
8. List the top risks, each with a fallback.

## Deliverables
- **Brief summary**: problem, users, requirements, judging criteria (with quotes).
- **Constraints and prohibited approaches.**
- **Open questions.**
- **MVP scope**: in scope / stretch / out of scope.
- **Success criteria**: metric, baseline, demo flow.
- **48-hour plan**: table of time block | task | owner | done-when.
- **Risks and fallbacks.**

## Common failure modes
- Picking a model or framework before reading the judging criteria.
- Missing a required deliverable (video, write-up, citations, team names).
- An MVP that cannot be finished in half the time.
- Success criteria with no number or no baseline.
- No buffer for submission, recording and write-up.
