---
name: api-inference
description: Serve a trained model through a separate inference module and a validated FastAPI endpoint that loads saved model and preprocessing artifacts, with error handling and tests. Use when the model needs to be called from an app or API.
---

# API inference

FastAPI is the default for an HTTP API. If the brief or the team's chosen stack uses something else (e.g. a Gradio or Streamlit app), keep steps 1-3 and 6-7 and call the inference module from that app instead. Do not install dependencies without asking.

Never retrain, refit or tune anything during a prediction request.

## Workflow
1. Create a separate inference module (e.g. `inference.py`) with no training code. It loads the saved model, preprocessing and feature list once at startup.
2. Expose one function such as `predict(input) -> output` that applies the same preprocessing as training, then the model.
3. Define request and response schemas (e.g. Pydantic models) with types, ranges, required fields and units. Agree them with the teammate building the front end before integration.
4. Add the FastAPI app (e.g. `api.py`): a `/health` endpoint and a `/predict` endpoint that validates input, calls the inference module and returns the response schema.
5. Handle errors explicitly: missing artifacts at startup, invalid input (422 with a clear message), model or external-service failures (5xx with a safe message, no stack traces to users).
6. Add any required labels to the response (e.g. "prototype, not advice" for health or finance outputs).
7. Write tests: inference on a known input, a valid API request, an invalid request, and missing-artifact handling. Run them and report the actual results.
8. Keep secrets in environment variables, never in code.

## Deliverables
- `inference.py` (load + predict), API app, request/response schemas.
- Tests and their actual run output.
- A short usage example (e.g. a curl command) that was actually run.

## Common failure modes
- Different preprocessing at inference than at training.
- Loading the model on every request.
- Retraining or fitting a scaler inside the request handler.
- Feature order or units that differ between the app and the model.
- Claiming the API works without having called it.
- Hardcoded API keys or file paths.
