"""Score the saved models against both baselines on the unseen TEST split.

Run from the repo root (after train.py):  .venv/bin/python ml/src/evaluate.py

Every forecast is scored on exactly the same test rows. Writes to ml/experiments/:
  test_mae_overall.csv      MAE, bias and median error per forecast
  test_mae_by_station.csv   MAE per station (checks performance across groups)
  test_mae_by_month.csv     MAE per month (season: winter smog, spring burning, monsoon)
  test_warnings.csv         warning counts at each threshold, as raw counts
  test_worst_misses.csv     the 15 biggest errors of the demo model ("where it fails")
  test_bootstrap_vs_persistence.csv  MAE gain over persistence with a 95% interval
  test_predictions.csv      every test row with every forecast, for the demo and write-up
"""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR, MODEL_DIR, OUT_DIR = ROOT / "data", ROOT / "models", ROOT / "experiments"
# 35.0: US EPA 24-hour standard, suggested by the brief.
# 55.5: start of the AQI "Unhealthy" band (unhealthy for everyone, not just sensitive groups).
THRESHOLDS = (35.0, 55.5)
FORECASTS = ["persistence", "cams", "linear_regression", "random_forest", "random_forest_change"]
DEMO = "random_forest_change"  # the improved model (v2) used in the demo
N_BOOT, SEED = 2000, 42


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


def bootstrap_vs_persistence(test: pd.DataFrame) -> pd.DataFrame:
    """MAE gain over persistence with a 95% interval.

    Neighbouring days (and stations on the same day) have similar errors, so we resample
    whole calendar weeks rather than single rows. If the interval is entirely above 0,
    the model beats persistence by more than chance.
    """
    rng = np.random.default_rng(SEED)
    week = test["date"].dt.to_period("W").astype(str)
    groups = {w: idx.to_numpy() for w, idx in test.groupby(week).groups.items()}
    keys = list(groups)
    err_p = (test["persistence"] - test["target_pm25"]).abs().to_numpy()
    rows = []
    for f in FORECASTS:
        if f == "persistence":
            continue
        gain = err_p - (test[f] - test["target_pm25"]).abs().to_numpy()
        pos = {w: test.index.get_indexer(groups[w]) for w in keys}
        samples = []
        for _ in range(N_BOOT):
            pick = rng.choice(len(keys), size=len(keys), replace=True)
            samples.append(np.concatenate([gain[pos[keys[i]]] for i in pick]).mean())
        lo, hi = np.percentile(samples, [2.5, 97.5])
        rows.append({"forecast": f, "mae_gain": round(float(gain.mean()), 2),
                     "ci_low": round(float(lo), 2), "ci_high": round(float(hi), 2),
                     "days_closer_than_persistence": f"{int((gain > 0).sum())} of {len(gain)}"})
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
    for name in ("linear_regression", "random_forest", "random_forest_change"):
        pred = joblib.load(MODEL_DIR / f"{name}.joblib").predict(test[feats])
        test[name] = test["pm25_today"] + pred if name in meta["predicts_change"] else pred
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
    boot = bootstrap_vs_persistence(test)
    test["model_error"] = test[DEMO] - test["target_pm25"]
    worst = test.reindex(test.model_error.abs().sort_values(ascending=False).index).head(15)
    num = ["pm25_today", "target_pm25", DEMO, "persistence", "cams", "model_error"]
    worst = worst[["station", "date"] + num + ["precip_mm", "wind_kmh"]].round({c: 1 for c in num})

    OUT_DIR.mkdir(exist_ok=True)
    overall.to_csv(OUT_DIR / "test_mae_overall.csv", index=False)
    st.to_csv(OUT_DIR / "test_mae_by_station.csv", index=False)
    mo.to_csv(OUT_DIR / "test_mae_by_month.csv", index=False)
    warn.to_csv(OUT_DIR / "test_warnings.csv", index=False)
    boot.to_csv(OUT_DIR / "test_bootstrap_vs_persistence.csv", index=False)
    worst.to_csv(OUT_DIR / "test_worst_misses.csv", index=False)
    cols = ["station_id", "station", "date", "pm25_today", "target_pm25"] + FORECASTS
    test[cols].round({f: 2 for f in FORECASTS}).to_csv(OUT_DIR / "test_predictions.csv", index=False)

    pd.set_option("display.width", 200)
    print(f"TEST {test.date.min().date()}..{test.date.max().date()}, {len(test)} station-days\n")
    print(overall.to_string(index=False), "\n")
    print(st.to_string(index=False), "\n")
    print(mo.to_string(index=False), "\n")
    print(warn.drop(columns=["recall", "precision"]).to_string(index=False), "\n")
    print("Is the gain over persistence more than luck? (weekly block bootstrap, 95% interval)")
    print(boot.to_string(index=False), "\n")
    print(f"Biggest {DEMO} misses:")
    print(worst.to_string(index=False))


if __name__ == "__main__":
    main()
