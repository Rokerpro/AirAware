# AirAware

Entry for the Veritas AI International High School Hackathon 2026 (AI + Climate track). Official brief: `docs/` and [`docs/CHALLENGE_BRIEF.md`](docs/CHALLENGE_BRIEF.md). Submission deadline: Sun Nov 15, 11:59 PM ET.

**Status: planning. There is no code yet.** Sections marked **(TBD)** are filled in as the project is built. Nothing below reports real results.

## Project name and description

**AirAware** is a planned next-day air-quality forecast for Kathmandu (tomorrow's daily-average PM2.5), built for the AI + Climate track (suggested project 4.3.2), with an early-warning level per monitored neighbourhood (warn above 35 μg/m3) and a plain-language precaution for school staff deciding on outdoor activity. This project is a prototype and is not medical advice.

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

**(TBD)** Two team members. Names, emails and schools to be added (the submission form needs all three for every member).

- [Name], data and model
- [Name], demo and write-up

## Model evaluation results

Initial results for Phora Durbar, Kathmandu, use a chronological split and
142 aligned final test samples. The final Linear Regression model uses
today's PM2.5, a three-day PM2.5 mean, and month.

| Metric | Persistence baseline | Linear Regression |
|---|---:|---:|
| Final test MAE (μg/m³) | 3.92 | 3.29 |
| Final test RMSE (μg/m³) | 4.92 | 4.15 |

The final model improves test MAE by 0.63 μg/m³. These are held-out results,
not training scores. At the 35 μg/m³ warning threshold, the model caught 117
of 122 high-pollution test days, missed 5, and produced 1 false alarm.
Persistence caught 118, missed 4, and produced 3 false alarms. The model
therefore reduced false alarms but had slightly lower recall.

The largest listed error was 2023-09-26: actual 68.38 μg/m³ versus predicted
52.95 μg/m³. CAMS comparison, station/season breakdowns, and additional
failure analysis remain to be added from the evaluation notebook.

## Data sources and citations

**(TBD)** To be documented with licenses:
- OpenAQ v3 (Kathmandu monitors)
- Open-Meteo weather and air-quality API (CAMS model data)

Every dataset, model, code source and AI tool used will be cited here.
