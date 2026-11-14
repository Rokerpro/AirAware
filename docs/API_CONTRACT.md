# Frontend / Backend / ML API Contract

**Status: DRAFT.** Updated to match the official Climate brief 4.3.2 (see `docs/CHALLENGE_BRIEF.md`), which asks for a forecast of tomorrow's daily-average PM2.5 and suggests a 35 μg/m3 warning threshold. Items marked **(TBD)** depend on what the data turns out to contain (e.g. how many OpenAQ stations have usable history).

The interface is a single forecast call: given a monitoring station and a date, return tomorrow's predicted daily-average PM2.5, whether to warn, its AQI band (context), and a plain-language precaution. The Gradio demo (frontend) calls the inference module (backend), which loads the saved model and preprocessing artifacts (ML).

## Endpoint
`/forecast`: tomorrow's PM2.5 forecast and early-warning level for one station.

Supporting endpoints:
- `/stations`: lists the stations the model can forecast (the frontend builds one alert card per station; the number is capped by working OpenAQ stations, no interpolation between them).
- `/health`: confirms the service and model are loaded.

(The brief does not require an HTTP API; in the Colab-only demo the same contract can be a Python function call with these inputs/outputs.)

## Implementation
`ml/src/predict.py` implements this contract as Python functions: `health()`, `list_stations()` (also returns each station's `first_date` and `last_date`) and `forecast(station_id, date, language)`. Errors raise `predict.ForecastError`; `.to_dict()` returns the error JSON below.

## HTTP method
- `POST /forecast`
- `GET /stations`
- `GET /health`

## Input schema
`POST /forecast` body (JSON):

| Field | Type | Required | Description |
|---|---|---|---|
| `station_id` | string | yes | A station id returned by `GET /stations`. |
| `date` | string, `YYYY-MM-DD` | yes | The "today" the forecast starts from. The forecast is for `date + 1 day`. |
| `language` | string, `"en"` or `"ne"` | no, default `"en"` | Language of the precaution text (English or Nepali). |

The backend builds the model features itself from stored data for that station and date: today's PM2.5, 3-day average PM2.5, temperature, wind speed, rainfall, humidity, and month. The user does not enter these. Features use only data available up to the end of `date`, to prevent leakage.

## Output schema
`POST /forecast` 200 response (JSON):

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Echo of the request. |
| `station_name` | string | Neighbourhood/area label shown on the alert card. |
| `forecast_for` | string, `YYYY-MM-DD` | `date + 1 day`. |
| `predicted_pm25` | number | Model forecast of tomorrow's daily-average PM2.5, in μg/m3. |
| `aqi_band` | string | Standard AQI band for `predicted_pm25` (context only): `Good`, `Moderate`, `Unhealthy for Sensitive Groups`, `Unhealthy`, `Very Unhealthy`, `Hazardous`. |
| `warning` | boolean | `true` when `predicted_pm25` is above the warning threshold (35 μg/m3, the US EPA 24-hour standard suggested by the brief). The threshold is a documented constant and may be tuned, with the choice explained. |
| `baselines` | object | `persistence_pm25` (tomorrow = today) and `cams_pm25` (CAMS forecast via Open-Meteo, may be `null` if unavailable), so the UI can show model vs. baselines. |
| `precaution` | string | Plain-language advice in the requested language, including the school decision ("hold outdoor PE/assembly tomorrow?"). |
| `disclaimer` | string | Always `"Prototype, not health advice."` (and its Nepali version when `language` is `ne`). |
| `alert_level` | string | `none` (≤ 35 μg/m3), `warning` (> 35, unhealthy for sensitive groups) or `high` (≥ 55.5, AQI "Unhealthy" for everyone: move PE and assembly indoors). The second level exists because 35 μg/m3 is exceeded on 68% of test days, so `warning` alone is on almost all winter. |
| `actual_pm25` | number or null | Measured PM2.5 for `forecast_for` when the backend has it (past dates), else `null`. Lets the demo show whether the forecast was right. |
| `model_version` | string | Which saved model produced the result (currently `random_forest_v2`). |

`GET /stations` 200 response: `{"stations": [{"station_id": "...", "station_name": "..."}]}`.

`GET /health` 200 response: `{"status": "ok", "model_loaded": true}`.

## Validation
- `station_id` and `date` are required; missing fields return 422.
- `station_id` must be in the station list.
- `date` must be a valid `YYYY-MM-DD` and fall within the range of data the backend holds for that station (so the features can be built). Future dates beyond the latest data are rejected.
- `language` must be `en` or `ne` if provided.
- Unknown extra fields are ignored or rejected (pick one when implementing; reject is safer).
- Values are checked server-side even though the Gradio UI restricts choices.

## Error handling
Errors return JSON: `{"error": {"code": "<code>", "message": "<human-readable>"}}`.

| Case | HTTP status | Code |
|---|---|---|
| Missing or malformed field, bad date format, bad language | 422 | `invalid_input` |
| Unknown `station_id` | 404 | `unknown_station` |
| Date outside available data range for that station | 400 | `date_out_of_range` |
| Not enough recent readings to build features (gaps in PM2.5/weather) | 422 | `insufficient_data` |
| Model or preprocessing artifact missing or failed to load | 503 | `model_unavailable` |
| Model raised an error during prediction | 500 | `prediction_failed` |
| CAMS baseline unreachable | 200, with `baselines.cams_pm25: null` (not an error) | n/a |

The frontend shows a clear message and no forecast on any error. It never displays a guessed number. Stack traces and API keys are never returned to the client.

## Model behavior
- Task: regression for next-day daily-average PM2.5 per station, then a 35 μg/m3 threshold for the warning.
- Models, in order: baseline "tomorrow = today", linear regression, Random Forest (scikit-learn). The saved model is whichever is best on the time-based test set.
- Split by time (train on older dates, test on the most recent months). No random splits.
- Required baseline: "tomorrow = today". Second baseline: the CAMS forecast via Open-Meteo. It is model output, not monitor data, so it is a comparison, not ground truth.
- Warning evaluation: recall (of days truly above 35 μg/m3, how many we warned about) and precision (of our warnings, how many were right), reported as raw counts and compared against both baselines. The warning threshold may be tuned to favour recall, since a missed warning is worse than a false one.
- Known weak spots, to be reported honestly: smog spikes, burning season, high-pollution months, and per-station differences.
- Station count: 6 OpenAQ stations (Embassy Kathmandu, Dabali Handigaun, KIAS, Lagankhel SC-05, Shantichowk SC-11, Gaushala Chowk SC-01). Embassy stopped reporting in June 2026.
- Pollutant: PM2.5, hourly readings averaged to daily means. The brief wants at least a year of mostly complete readings per station. Open-Meteo air-quality values are model estimates, so label them as such.

## Example requests
Illustrative only, with a placeholder station id. Replace after implementation.

```http
POST /forecast
Content-Type: application/json

{
  "station_id": "<station_id>",
  "date": "<YYYY-MM-DD>",
  "language": "en"
}
```

```http
GET /stations
```

## Example responses
Shape only. The numbers are placeholders, not real results. Replace with real output after implementation.

```json
{
  "station_id": "<station_id>",
  "station_name": "<area name>",
  "forecast_for": "<YYYY-MM-DD>",
  "predicted_pm25": "<number>",
  "aqi_band": "<band>",
  "warning": "<true|false>",
  "baselines": { "persistence_pm25": "<number>", "cams_pm25": "<number|null>" },
  "precaution": "<plain-language advice>",
  "disclaimer": "Prototype, not health advice.",
  "model_version": "<model_version>"
}
```

Error example:

```json
{ "error": { "code": "unknown_station", "message": "Station '<id>' is not available." } }
```
