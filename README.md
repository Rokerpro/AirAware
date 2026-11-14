# AirAware

Entry for the Veritas AI International High School Hackathon 2026.

**Status: planning. There is no code yet.** Sections marked **(TBD)** are filled in as the project is built. Nothing below reports real results.

## Project name and description

**AirAware** is a planned next-day air-quality (AQI) forecast for Kathmandu, with an early-warning level per monitored neighbourhood and a plain-language precaution. It is prototype, not health advice.

Planned approach: compare a "tomorrow = today" baseline, linear regression and Random Forest (scikit-learn), and compare against the CAMS forecast from Open-Meteo. Details: [`docs/CHALLENGE_BRIEF.md`](docs/CHALLENGE_BRIEF.md).

## Repository layout

```
backend/    API and inference code (empty)
frontend/   Demo interface (empty)
ml/         Data, training and evaluation code (empty)
tests/      Tests (empty)
docs/       Challenge brief and API contract
```

## Installation instructions

**(TBD)** Planned: Python 3 with a virtual environment locally, or Google Colab with package installs pinned in the first cell. Dependencies will be listed in a requirements file once code exists.

```bash
git clone <repository-url>
cd AirAware
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # (TBD) file does not exist yet
```

## Environment setup

**(TBD)** Planned configuration:

| Variable | Purpose |
|---|---|
| `OPENAQ_API_KEY` | OpenAQ v3 key (free, required; requests return 401 without it) |

- Keep keys in environment variables or Colab secrets. Never commit them.
- Open-Meteo needs no key.

## How to run the frontend

**(TBD)** Planned: a Gradio app.

```bash
# (TBD)
```

## How to run the backend

**(TBD)** Planned: a validated API serving forecasts, following [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md).

```bash
# (TBD)
```

## How to run training

**(TBD)** Planned: baseline first, then linear regression and Random Forest, with a time-based train/test split and saved model and preprocessing artifacts.

```bash
# (TBD)
```

## How to run inference

**(TBD)** Planned: an inference module that loads the saved artifacts and returns a forecast for a station and date.

```bash
# (TBD)
```

## API documentation

See [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md). It is a draft and not implemented yet.

## Team members

**(TBD)** Two team members. Names to be added.

- [Name], data and model
- [Name], demo and write-up

## Model evaluation results

**(TBD)** No models have been trained, so there are no results yet. This section will report actual results only, including failures: MAE against the baselines, warning recall and precision, and error by station and season.

## Data sources and citations

**(TBD)** To be documented with licenses:
- OpenAQ v3 (Kathmandu monitors)
- Open-Meteo weather and air-quality API (CAMS model data)

Every dataset, model, code source and AI tool used will be cited here.
