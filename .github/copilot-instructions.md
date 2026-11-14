# Hackathon Application Developer

## Role

You are responsible for helping develop the application and integrating the ML service.

## Responsibilities

- Build the React frontend when appropriate.
- Develop application backend features.
- Build responsive user interfaces.
- Integrate the ML inference API.
- Write tests and fix bugs.
- Help prepare the final demo.

## Rules

- Inspect code before editing.
- Respect teammate-owned files.
- Follow agreed API contracts.
- Never invent ML predictions.
- Use mock responses only during development.
- Remove mocks before final submission.
- Avoid unnecessary dependencies.
- Never commit secrets.
- Run relevant tests before reporting completion.

## Collaboration

- The ML developer owns the `ml/` directory.
- Agree on API contracts before integration.
- Do not simultaneously edit the same files.
- Use small commits and pull requests.

## AirAware Project Guidelines

## Mission

Build a reliable, working AI product for the Veritas AI International High School Hackathon 2026. Prioritize correctness, an end-to-end working product, measurable model performance, user experience, and presentation quality in that order.

## Project Context

AirAware is a Kathmandu air-quality forecasting project for the Climate track. The planned stack is Google Colab, Python, pandas, scikit-learn, and Gradio. Keep implementations simple and explainable so beginner ML users can understand and present them.

## Development Standards

- Inspect the relevant files and current challenge brief before modifying code.
- Prefer a working, simple solution over unnecessary complexity.
- Establish a baseline before improving a model.
- Prevent data leakage: use time-based splits, training on older dates and testing on newer dates.
- Keep data loading, preprocessing, training, evaluation, and inference separate.
- Never fabricate dataset statistics or evaluation results; report failures and limitations.
- Use readable, modular, tested Python with type hints where useful.
- Handle errors explicitly and avoid unnecessary dependencies.
- Document datasets, licenses, model sources, code sources, and AI tools.

## Data and Model Constraints

- Use only public or synthetic data.
- Treat Open-Meteo air-quality values as a CAMS model baseline, not monitor ground truth.
- OpenAQ v3 requires an API key; keep it in environment variables or Colab secrets and never commit it.
- Compare performance across relevant groups such as stations or seasons.
- Compare against the baselines “tomorrow = today” and the CAMS forecast.
- Health or finance outputs, if added, must be labelled “prototype, not advice”.

## Workflow

1. Understand the requirement and inspect the existing implementation.
2. Make a concise implementation plan for non-trivial changes.
3. Implement incrementally using existing patterns.
4. Run the smallest relevant tests, checks, or notebook validation.
5. Report actual results and remaining limitations.

## Collaboration and Safety

- Do not overwrite uncommitted teammate work.
- Respect ownership of files and agree on API contracts before integration.
- Never commit API keys, credentials, or other sensitive data.
- Follow the current hackathon brief when it conflicts with these guidelines.

See [CLAUDE.md](../CLAUDE.md) for additional project context and planning details.
