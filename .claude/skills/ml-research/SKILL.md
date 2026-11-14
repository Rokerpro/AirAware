---
name: ml-research
description: Research and compare ML approaches, models, datasets and existing solutions for a defined problem, then recommend a realistic solution for the time limit. Use after the problem is defined and before committing to a model or dataset.
---

# ML research

Start from the defined problem (run challenge-triage first if there is none). Do not force a technology the brief does not call for.

## Workflow
1. Restate the task: type (classification, regression, forecasting, generation, ...), input, output, metric, time and compute limits.
2. Find existing solutions (papers, repos, competitions, products). Note what they do and their limitations.
3. Find candidate datasets. For each: source URL, licence, size, coverage, access method (key needed?), and whether you have actually verified that it loads.
4. Compare at least three approaches, always considering:
   - a pretrained model used as-is,
   - fine-tuning a pretrained model,
   - classical ML or a rule-based baseline.
   Avoid training from scratch unless there is a strong, stated reason.
5. Estimate effort and compute for each option and say what it would need (GPU? hours? API cost?).
6. Recommend one approach plus a fallback, and the baseline it must beat.
7. Do not install packages or download large models during research; list what would be needed instead.

## Deliverables
- **Task restatement.**
- **Existing solutions**: table of name | what it does | limitation | source link.
- **Datasets**: table of name | licence | size | access | verified? | source link.
- **Approach comparison**: table of approach | data needed | compute | time to working version | risk | explainability.
- **Recommendation and fallback**, with the baseline.
- **Uncertainty**: what is unverified and how to check it.
- **Sources**: every link used.

## Common failure modes
- Quoting benchmark numbers or dataset sizes without a source.
- Assuming a dataset exists or is accessible without checking (licence, API key, region coverage).
- Recommending an approach that needs more compute or time than the team has.
- Ignoring a simple baseline that might already be good enough.
- Licences that forbid the intended use.
