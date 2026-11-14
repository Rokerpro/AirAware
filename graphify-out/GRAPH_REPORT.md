# Graph Report - AirAware  (2026-11-14)

## Corpus Check
- 2 files · ~4,058 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 37 nodes · 48 edges · 8 communities (5 shown, 3 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Project Scope & Data Sources
- Baselines & Core Principles
- Project Config & Tooling
- Data Quality & Leakage
- Planning & Research
- Hackathon Rules
- Integration & API Serving
- Mission & Priorities

## God Nodes (most connected - your core abstractions)
1. `CLAUDE.md (AirAware project guidance)` - 22 edges
2. `AirAware: Kathmandu air-quality forecast (Climate track)` - 6 edges
3. `dataset-audit skill` - 4 edges
4. `Core principles` - 4 edges
5. `model-training skill` - 3 edges
6. `ml-research skill` - 3 edges
7. `Hackathon rules constraining the work` - 3 edges
8. `Prevent data leakage` - 3 edges
9. `Baselines: tomorrow=today and CAMS forecast` - 3 edges
10. `integration-reviewer subagent` - 2 edges

## Surprising Connections (you probably didn't know these)
- `CLAUDE.md (AirAware project guidance)` --references--> `integration-reviewer subagent`  [EXTRACTED]
  CLAUDE.md → .claude/agents/integration-reviewer.md
- `CLAUDE.md (AirAware project guidance)` --references--> `api-inference skill`  [EXTRACTED]
  CLAUDE.md → .claude/skills/api-inference/SKILL.md
- `CLAUDE.md (AirAware project guidance)` --references--> `model-evaluation skill`  [EXTRACTED]
  CLAUDE.md → .claude/skills/model-evaluation/SKILL.md
- `CLAUDE.md (AirAware project guidance)` --references--> `dataset-auditor subagent`  [EXTRACTED]
  CLAUDE.md → .claude/agents/dataset-auditor.md
- `CLAUDE.md (AirAware project guidance)` --references--> `ml-architect subagent`  [EXTRACTED]
  CLAUDE.md → .claude/agents/ml-architect.md

## Hyperedges (group relationships)
- **Leakage-safe evaluation practices** — claude_md_time_based_split, claude_md_data_leakage, claude_md_baselines, claude_md_baseline_first [INFERRED 0.85]
- **AirAware data sources** — claude_md_open_meteo_cams, claude_md_cams, claude_md_openaq_v3 [EXTRACTED 1.00]

## Communities (8 total, 3 thin omitted)

### Community 0 - "Project Scope & Data Sources"
Cohesion: 0.25
Nodes (7): AirAware: Kathmandu air-quality forecast (Climate track), Collaboration rules, MonsoonRain (backup project), OpenAQ v3 (needs API key; main project risk), Planned stack: Colab, pandas, scikit-learn, Gradio, plans/ (gitignored local planning files), Veritas AI International High School Hackathon 2026

### Community 1 - "Baselines & Core Principles"
Cohesion: 0.29
Nodes (6): Baselines: tomorrow=today and CAMS forecast, CAMS model forecast, Core principles, Open-Meteo air-quality API (CAMS model data), Keep training, evaluation and inference separate, model-evaluation skill

### Community 2 - "Project Config & Tooling"
Cohesion: 0.29
Nodes (7): Development standards, graphify usage rules, AirAware Notion page (notion MCP), CLAUDE.md (AirAware project guidance), Skills pipeline: triage, research, audit, training, evaluation, inference, Subagents: ml-architect, dataset-auditor, integration-reviewer, Workflow (inspect, plan, implement, test, report)

### Community 3 - "Data Quality & Leakage"
Cohesion: 0.50
Nodes (3): dataset-auditor subagent, dataset-audit skill, model-training skill

### Community 4 - "Planning & Research"
Cohesion: 0.67
Nodes (3): ml-architect subagent, challenge-triage skill, ml-research skill

## Knowledge Gaps
- **10 isolated node(s):** `MonsoonRain (backup project)`, `Planned stack: Colab, pandas, scikit-learn, Gradio`, `Submission requirements`, `Keep training, evaluation and inference separate`, `Workflow (inspect, plan, implement, test, report)` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 11 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md (AirAware project guidance)` connect `Project Config & Tooling` to `Project Scope & Data Sources`, `Baselines & Core Principles`, `Data Quality & Leakage`, `Planning & Research`, `Hackathon Rules`, `Integration & API Serving`, `Mission & Priorities`?**
  _High betweenness centrality (0.862) - this node is a cross-community bridge._
- **What connects `MonsoonRain (backup project)`, `Planned stack: Colab, pandas, scikit-learn, Gradio`, `Submission requirements` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `AirAware: Kathmandu air-quality forecast (Climate track)` connect `Project Scope & Data Sources` to `Baselines & Core Principles`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Why does `Core principles` connect `Baselines & Core Principles` to `Project Config & Tooling`, `Data Quality & Leakage`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._