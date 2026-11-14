# Frontend / Backend / ML API Contract

**Status: DRAFT.** Filled in from `plans/AirAware Plan.md`. The official challenge brief (`docs/CHALLENGE_BRIEF.md`) is still blank, and the brief overrides this plan. Items marked **(TBD)** depend on what the data turns out to contain (e.g. how many OpenAQ stations have usable history).

The interface is a single forecast call: given a monitoring station and a date, return tomorrow's predicted AQI, its AQI band, whether to warn, and a plain-language precaution. The Gradio demo (frontend) calls the inference module (backend), which loads the saved model and preprocessing artifacts (ML).

## Endpoint
`/forecast`: tomorrow's AQI forecast and early-warning level for one station.

Supporting endpoints:
- `/stations`: lists the stations the model can forecast (the frontend builds one alert card per station; the number is capped by working OpenAQ stations, no interpolation between them).
- `/health`: confirms the service and model are loaded.

(Final paths **TBD** after the brief; in the Colab-only demo the same contract can be a Python function call with these inputs/outputs.)

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

The backend builds the model features itself from stored data for that station and date: yesterday's AQI, 3-day average AQI, temperature, wind, humidity, and month. The user does not enter these. Features use only data available up to the end of `date`, to prevent leakage.

## Output schema
`POST /forecast` 200 response (JSON):

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Echo of the request. |
| `station_name` | string | Neighbourhood/area label shown on the alert card. |
| `forecast_for` | string, `YYYY-MM-DD` | `date + 1 day`. |
| `predicted_aqi` | number | Model forecast of tomorrow's AQI. |
| `aqi_band` | string | Standard AQI band for `predicted_aqi`: `Good`, `Moderate`, `Unhealthy for Sensitive Groups`, `Unhealthy`, `Very Unhealthy`, `Hazardous`. |
| `warning` | boolean | `true` when the predicted band is "Unhealthy for Sensitive Groups" or worse. |
| `baselines` | object | `persistence_aqi` (tomorrow = today) and `cams_aqi` (CAMS forecast via Open-Meteo, may be `null` if unavailable), so the UI can show model vs. baselines. |
| `precaution` | string | Plain-language advice in the requested language, including the school decision ("hold outdoor PE/assembly tomorrow?"). |
| `disclaimer` | string | Always `"Prototype, not health advice."` (and its Nepali version when `language` is `ne`). |
| `model_version` | string | Which saved model produced the result (e.g. `random_forest_v1`). |

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
| Not enough recent readings to build features (gaps in AQI/weather) | 422 | `insufficient_data` |
| Model or preprocessing artifact missing or failed to load | 503 | `model_unavailable` |
| Model raised an error during prediction | 500 | `prediction_failed` |
| CAMS baseline unreachable | 200, with `baselines.cams_aqi: null` (not an error) | n/a |

The frontend shows a clear message and no forecast on any error. It never displays a guessed number. Stack traces and API keys are never returned to the client.

## Model behavior
- Task: regression for next-day AQI per station, then threshold into AQI bands for the warning.
- Models, in order: baseline "tomorrow = today", linear regression, Random Forest (scikit-learn). The saved model is whichever is best on the time-based test set.
- Split by time (train on older dates, test on the newest). No random splits.
- Second baseline: the CAMS forecast via Open-Meteo. It is model output, not monitor data, so it is a comparison, not ground truth.
- Warning evaluation: recall (of truly unhealthy days, how many we warned about) and precision (of our warnings, how many were right), reported as raw counts and compared against both baselines. The warning threshold may be tuned to favour recall, since a missed warning is worse than a false one.
- Known weak spots, to be reported honestly: smog spikes, burning season, high-pollution months, and per-station differences.
- Station count: **(TBD)**. If only 1-2 stations have usable history, fall back to a single city-level warning.
- Pollutant/AQI definition (e.g. PM2.5-based AQI): **(TBD)** once the OpenAQ data is inspected.

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
  "predicted_aqi": "<number>",
  "aqi_band": "<band>",
  "warning": "<true|false>",
  "baselines": { "persistence_aqi": "<number>", "cams_aqi": "<number|null>" },
  "precaution": "<plain-language advice>",
  "disclaimer": "Prototype, not health advice.",
  "model_version": "<model_version>"
}
```

Error example:

```json
{ "error": { "code": "unknown_station", "message": "Station '<id>' is not available." } }
```
