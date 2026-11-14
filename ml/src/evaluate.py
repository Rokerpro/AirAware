"""Score the saved models against both baselines on the unseen TEST split.

Run from the repo root (after train.py):  .venv/bin/python ml/src/evaluate.py

Every forecast is scored on exactly the same test rows. Writes to ml/experiments/:
  test_mae_overall.csv      MAE, bias and median error per forecast
  test_mae_by_station.csv   MAE per station (checks performance across groups)
  test_mae_by_month.csv     MAE per month (season: winter smog, spring burning, monsoon)
  test_warnings.csv         warning counts at each threshold, as raw counts
  test_worst_misses.csv     the 15 biggest model errors ("where it fails")
  test_predictions.csv      every test row with every forecast, for the demo and write-up
"""
import json
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR, MODEL_DIR, OUT_DIR = ROOT / "data", ROOT / "models", ROOT / "experiments"
# 35.0: US EPA 24-hour standard, suggested by the brief.
# 55.5: start of the AQI "Unhealthy" band (unhealthy for everyone, not just sensitive groups).
THRESHOLDS = (35.0, 55.5)
FORECASTS = ["persistence", "cams", "linear_regression", "random_forest"]


def mae(actual: pd.Series, pred: pd.Series) -> float:
    return round(float((actual - pred).abs().mean()), 2)


def by_group(test: pd.DataFrame, col: str) -> pd.DataFrame:
    rows = []
    for name, g in list(test.groupby(col)) + [("ALL", test)]:
        row = {col: name, "n": len(g), "mean_pm25": round(g.target_pm25.mean(), 1)}
        row.update({f: mae(g.target_pm25, g[f]) for f in FORECASTS})
        rows.append(row)
    return pd.DataFrame(rows)


def warnings(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for t in THRESHOLDS:
        bad = test.target_pm25 > t
        for f in FORECASTS:
            warn = test[f] > t
            caught = int((bad & warn).sum())
            rows.append({
                "threshold": t, "forecast": f, "bad_days": int(bad.sum()),
                "caught": caught, "missed": int((bad & ~warn).sum()),
                "false_alarms": int((~bad & warn).sum()), "warnings_issued": int(warn.sum()),
                "recall": f"{caught} of {int(bad.sum())}",
                "precision": f"{caught} of {int(warn.sum())}",
            })
    return pd.DataFrame(rows)


def main() -> None:
    meta = json.loads((MODEL_DIR / "meta.json").read_text())
    feats = meta["features"]
    df = pd.read_csv(DATA_DIR / "features.csv", parse_dates=["date"])
    test = df[df["split"] == "test"].copy()
    assert test["date"].min() >= pd.Timestamp(meta["test_start"])
    # CAMS is missing for no test rows today; drop any that are so all forecasts share rows
    n_before = len(test)
    test = test.dropna(subset=["cams_tomorrow"])
    if len(test) < n_before:
        print(f"note: dropped {n_before - len(test)} test rows with no CAMS value")

    test["persistence"] = test["pm25_today"]
    test["cams"] = test["cams_tomorrow"]
    for name in ("linear_regression", "random_forest"):
        test[name] = joblib.load(MODEL_DIR / f"{name}.joblib").predict(test[feats])
    test["month_str"] = test["date"].dt.to_period("M").astype(str)

    overall = pd.DataFrame([{
        "forecast": f,
        "mae": mae(test.target_pm25, test[f]),
        "bias_pred_minus_actual": round(float((test[f] - test.target_pm25).mean()), 2),
        "median_abs_error": round(float((test[f] - test.target_pm25).abs().median()), 2),
    } for f in FORECASTS])
    st = by_group(test, "station")
    mo = by_group(test, "month_str").rename(columns={"month_str": "month"})
    warn = warnings(test)
    test["rf_error"] = test["random_forest"] - test["target_pm25"]
    worst = test.reindex(test.rf_error.abs().sort_values(ascending=False).index).head(15)
    worst = worst[["station", "date", "pm25_today", "target_pm25", "random_forest",
                   "persistence", "cams", "rf_error", "precip_mm", "wind_kmh"]].round({c: 1 for c in ["pm25_today", "target_pm25", "random_forest", "persistence", "cams", "rf_error"]})

    OUT_DIR.mkdir(exist_ok=True)
    overall.to_csv(OUT_DIR / "test_mae_overall.csv", index=False)
    st.to_csv(OUT_DIR / "test_mae_by_station.csv", index=False)
    mo.to_csv(OUT_DIR / "test_mae_by_month.csv", index=False)
    warn.to_csv(OUT_DIR / "test_warnings.csv", index=False)
    worst.to_csv(OUT_DIR / "test_worst_misses.csv", index=False)
    cols = ["station_id", "station", "date", "pm25_today", "target_pm25"] + FORECASTS
    test[cols].round({f: 2 for f in FORECASTS}).to_csv(OUT_DIR / "test_predictions.csv", index=False)

    pd.set_option("display.width", 200)
    print(f"TEST {test.date.min().date()}..{test.date.max().date()}, {len(test)} station-days\n")
    print(overall.to_string(index=False), "\n")
    print(st.to_string(index=False), "\n")
    print(mo.to_string(index=False), "\n")
    print(warn.drop(columns=["recall", "precision"]).to_string(index=False), "\n")
    print("Biggest Random Forest misses:")
    print(worst.to_string(index=False))


if __name__ == "__main__":
    main()
