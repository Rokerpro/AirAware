"""Inference: tomorrow's PM2.5 forecast for one station, as described in docs/API_CONTRACT.md.

The Gradio demo imports this module and calls three plain functions (no web server needed):
    list_stations()                          -> {"stations": [...]}
    health()                                 -> {"status": "ok", "model_loaded": True}
    forecast(station_id, date, language="en")-> forecast dict (see the contract)
Bad input raises ForecastError(code, message); err.to_dict() gives the contract's error JSON.

It only LOADS saved artifacts (ml/models/) and stored data (ml/data/). It never trains.
Features use data up to the end of `date` only, so there is no leakage.
"""
from __future__ import annotations

import json
from datetime import date as Date, timedelta
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from build_features import FEATURES, daily_table

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"

WARN_AT = 35.0        # ug/m3, US EPA 24-hour standard (suggested by the brief) -> warning = True
HIGH_AT = 55.5        # ug/m3, start of the AQI "Unhealthy" band -> alert_level = "high"
# PM2.5 AQI bands, US EPA 2024 revision (upper edge of each band, ug/m3, 24-hour average)
AQI_BANDS = [(9.0, "Good"), (35.4, "Moderate"), (55.4, "Unhealthy for Sensitive Groups"),
             (125.4, "Unhealthy"), (225.4, "Very Unhealthy"), (float("inf"), "Hazardous")]

# Precaution text for the school decision. The Nepali is a DRAFT: needs a native-speaker check.
PRECAUTIONS = {
    "none": {
        "en": "Air is forecast to be below the 35 ug/m3 warning level. Outdoor PE and "
              "assembly can go ahead as normal tomorrow.",
        "ne": "भोलि हावा ३५ माइक्रोग्राम/घनमिटरको चेतावनी तहभन्दा तल रहने अनुमान छ। बाहिरी "
              "खेलकुद र प्रार्थना सभा सामान्य रूपमा गर्न सकिन्छ।",
    },
    "warning": {
        "en": "Air may be unhealthy for sensitive groups tomorrow. Keep outdoor PE short and "
              "light, and let students with asthma or heart or lung conditions stay indoors.",
        "ne": "भोलि हावा संवेदनशील समूहका लागि अस्वस्थ हुन सक्छ। बाहिरी खेलकुद छोटो र हल्का "
              "राख्नुहोस्, र दम वा मुटु/फोक्सोको समस्या भएका विद्यार्थीलाई भित्रै राख्नुहोस्।",
    },
    "high": {
        "en": "Air is forecast to be unhealthy for everyone tomorrow. Move PE and assembly "
              "indoors.",
        "ne": "भोलि हावा सबैका लागि अस्वस्थ हुने अनुमान छ। खेलकुद र प्रार्थना सभा भित्र "
              "सार्नुहोस्।",
    },
}
DISCLAIMER = {"en": "Prototype, not health advice.",
              "ne": "प्रोटोटाइप मात्र, स्वास्थ्य सल्लाह होइन।"}


class ForecastError(ValueError):
    """Bad request. `code` matches the contract's error codes."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code, self.message = code, message

    def to_dict(self) -> dict:
        return {"error": {"code": self.code, "message": self.message}}


@lru_cache(maxsize=1)
def _load() -> tuple[dict, object, pd.DataFrame]:
    """Load metadata, the demo model and the feature table once."""
    meta = json.loads((MODEL_DIR / "meta.json").read_text())
    model = joblib.load(MODEL_DIR / f"{meta['demo_model']}.joblib")
    table = daily_table()
    table["station_id"] = table["station_id"].astype(str)
    return meta, model, table


def aqi_band(pm25: float) -> str:
    for upper, name in AQI_BANDS:
        if pm25 <= upper:
            return name
    return AQI_BANDS[-1][1]


def alert_level(pm25: float) -> str:
    if pm25 >= HIGH_AT:
        return "high"
    if pm25 > WARN_AT:
        return "warning"
    return "none"


def health() -> dict:
    try:
        _load()
    except Exception as e:  # report, don't crash the UI
        return {"status": "error", "model_loaded": False, "message": str(e)}
    return {"status": "ok", "model_loaded": True}


def list_stations() -> dict:
    _, _, table = _load()
    usable = table.dropna(subset=FEATURES)
    out = []
    for (sid, name), g in usable.groupby(["station_id", "station"]):
        out.append({"station_id": sid, "station_name": name,
                    "first_date": str(g.date.min().date()), "last_date": str(g.date.max().date())})
    return {"stations": out}


def forecast(station_id: str, date: str, language: str = "en") -> dict:
    """Forecast daily-average PM2.5 for date + 1 at one station."""
    meta, model, table = _load()
    station_id = str(station_id).strip()
    if language not in ("en", "ne"):
        raise ForecastError("invalid_language", "language must be 'en' or 'ne'.")
    try:
        day = Date.fromisoformat(str(date).strip())
    except ValueError:
        raise ForecastError("invalid_date", f"'{date}' is not a valid YYYY-MM-DD date.") from None

    st = table[table.station_id == station_id]
    if st.empty:
        raise ForecastError("unknown_station", f"Station '{station_id}' is not available.")
    row = st[st.date == pd.Timestamp(day)]
    if row.empty or row[FEATURES].isna().any(axis=None):
        usable = st.dropna(subset=FEATURES)
        raise ForecastError(
            "date_out_of_range",
            f"No complete data for station '{station_id}' on {day}. This station has usable "
            f"days between {usable.date.min().date()} and {usable.date.max().date()} "
            "(some days in between are missing).")
    row = row.iloc[0]

    raw = float(model.predict(row[FEATURES].to_frame().T.astype(float))[0])
    pred = row.pm25_today + raw if meta["demo_model"] in meta["predicts_change"] else raw
    pred = round(max(float(pred), 0.0), 1)  # PM2.5 can't be negative
    level = alert_level(pred)
    cams = row.get("cams_tomorrow")
    actual = row.get("target_pm25")
    return {
        "station_id": station_id,
        "station_name": str(row.station),
        "forecast_for": str(day + timedelta(days=1)),
        "predicted_pm25": pred,
        "aqi_band": aqi_band(pred),
        "warning": bool(pred > WARN_AT),
        "alert_level": level,  # extra field (not yet in the contract): none / warning / high
        "baselines": {
            "persistence_pm25": round(float(row.pm25_today), 1),
            "cams_pm25": None if pd.isna(cams) else round(float(cams), 1),
        },
        # extra field: the measured value for date + 1 if we have it (past dates only)
        "actual_pm25": None if pd.isna(actual) else round(float(actual), 1),
        "precaution": PRECAUTIONS[level][language],
        "disclaimer": DISCLAIMER[language],
        "model_version": meta["model_versions"][meta["demo_model"]],
    }


if __name__ == "__main__":
    stations = list_stations()["stations"]
    print(json.dumps(health()))
    for s in stations:
        print(json.dumps(forecast(s["station_id"], s["last_date"]), ensure_ascii=False))
