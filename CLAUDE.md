# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mission

Build a reliable, working AI product within a 48-hour hackathon.

## What this folder is

Planning folder for a two-person team of high-school students entering the Veritas AI International High School Hackathon 2026. It is a virtual 48-hour AI build: hacking starts Nov 14, 12:00 AM ET; submission deadline Sun Nov 15, 11:59 PM ET. There is no code yet. Planned stack: Google Colab, pandas, scikit-learn, Gradio. The user is a beginner in ML, so keep models and code at that level and explain them.

`plans/` is gitignored, so these files exist only locally:

- `plans/AirAware Plan.md`: the chosen project, a Kathmandu air-quality forecast for the Climate track (suggested project 4.3.2, next-day PM2.5 forecast). Covers what makes it different, roles, timeline and checklists. Backup: MonsoonRain.
- `plans/1 AI Health Project 1.txt`: the user's original 12 ideas.
- `plans/Plan 2 - New Project Ideas.txt`: 12 further ideas. Dataset names in it are unverified.

## Hackathon rules that constrain the work

- All project work happens between the start (Nov 14, 12:00 AM ET) and the deadline; earlier, only learning tools, starter notebooks and browsing datasets were allowed. AI/ML must do the project's main job.
- Public or synthetic data only; cite every dataset, model, code source and AI tool.
- Check model performance across groups (e.g. stations or seasons) and report real results, including failures.
- Health or finance outputs must be labelled "prototype, not advice".
- Teammates must be able to explain everything, so prefer simple, explainable code.
- Submission (one person submits for the team; resubmit any time, the latest is judged): public code link (Colab or GitHub, notebook saved with outputs), one-page write-up from the official template (Google Doc, README or PDF/Word), track, each member's name, email and school, credits with links, optional demo video of at most 2 minutes (unlisted YouTube or Drive). Teams have 1-3 students. Test every link in a private window and submit a first version a few hours early.
- Write-up and demo must answer: who is it for, what goes in/out, does it beat a baseline, where does it fail. Results only from unseen test data. Say what we added beyond the suggested project (own user, data or question).
- Judging (PDF section 6, same four criteria for every track): technical quality, impact, creativity, clarity. Climate judges look for a fair comparison with a simple forecast, a clear link between the prediction and a decision, and an unseen test period. Honest, modest results score higher than unexplained high ones.
- The official brief is the PDF in `docs/` (that copy is truncated at page 8); `docs/CHALLENGE_BRIEF.md` holds the summary for the pages we have. It overrides anything in `plans/`.

## Hackathon priorities

In order:

1. Correctness
2. Working end-to-end product
3. Measurable AI performance
4. User experience
5. Presentation quality

## Core principles

- Prioritize a working solution over unnecessary complexity.
- Inspect the challenge brief before choosing technologies.
- Compare pretrained models, fine-tuning and classical ML.
- Never train from scratch without a strong reason.
- Never fabricate dataset statistics or evaluation results.
- Establish a baseline before improving a model.
- Prevent data leakage.
- Keep training, evaluation and inference separate.

## Workflow

1. Inspect before modifying.
2. Understand the problem before coding.
3. Propose an implementation plan.
4. Implement incrementally.
5. Run tests after changes.
6. Report actual results and remaining limitations.

## Development standards

- Use Python virtual environments for local work. In Colab, pin package installs in the first cell instead.
- Write modular, readable and tested code.
- Use type hints where useful.
- Handle errors explicitly.
- Avoid unnecessary dependencies.
- Document datasets and licenses.

## Collaboration

- Respect ownership of files between teammates.
- Agree on API contracts before integration.
- Never overwrite uncommitted teammate work.
- Use Git branches and small commits.
- Never commit API keys, credentials or sensitive data (e.g. the OpenAQ key). Keep keys in environment variables or Colab secrets.

## Data notes (AirAware)

- The Open-Meteo air-quality API works without a key, but its values come from a model (CAMS), not monitors. Use it as a baseline to compare against, not as ground truth.
- OpenAQ v3 needs a free API key (it returns 401 without one). Kathmandu monitor history has not been verified yet. It is the main project risk.
- Always split by time (train on older dates, test on newer). Random splits leak future data. Target: tomorrow's daily-average PM2.5 (μg/m3). Baselines to beat: "tomorrow = today" (required by the brief) and the CAMS forecast. Warn above 35 μg/m3 (US EPA 24-hour standard, suggested by the brief). Prototype line for the write-up: "This project is a prototype and is not medical advice."

## Project tooling

- Notion: the team's notes live on the "AirAware" Notion page (https://app.notion.com/p/417018756a4280ee907feb2ddd0d5b1f). It is reached through the `notion` MCP server (local config; sign in with `/mcp`). Only write to Notion when asked, and never put API keys or credentials there.
- Subagents in `.claude/agents/` (read-only): `ml-architect`, `dataset-auditor`, `integration-reviewer`.
- Skills in `.claude/skills/`: `challenge-triage`, `ml-research`, `dataset-audit`, `model-training`, `model-evaluation`, `api-inference`. Intended order: triage, research, audit, training, evaluation, inference.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
