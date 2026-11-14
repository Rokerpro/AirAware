# frontend/

Development Gradio shell for the forecast contract in
[`docs/API_CONTRACT.md`](../docs/API_CONTRACT.md).

## Run locally

Install Gradio, then run:

```bash
python frontend/app.py
```

The current UI uses an explicitly temporary mock function. It must be
replaced with the real inference call before submission. The four station
choices are development placeholders until the ML time split confirms the
final station list.

The interface supports the contract fields for `/forecast`: station, date,
language, forecast date, PM2.5, warning, baselines, precaution, disclaimer,
and model version. It does not claim that mock values are real predictions.

## B2 precaution text

The development shell includes English and Nepali precaution text for the
school decision about outdoor PE or assembly. Every health-related display
includes:

> This project is a prototype and is not medical advice.

The final UI must keep this disclaimer when the real inference function is
connected.

## B6 credits checklist

Complete these before submission:

- Team members: names, emails, and schools (to be supplied by the team).
- OpenAQ v3: Kathmandu monitor data and API documentation.
- Open-Meteo: historical weather and CAMS air-quality documentation.
- scikit-learn and Gradio documentation.
- Any tutorials, pretrained models, and AI coding tools actually used.

Owner: frontend teammate (branch `frontend-development`).
