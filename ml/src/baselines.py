"""Baseline errors on the TEST period: "tomorrow = today" and the CAMS forecast.

Run from the repo root:  .venv/bin/python ml/src/baselines.py
Any model we train later has to beat these numbers on the same rows.

Writes to ml/experiments/:
  baseline_mae_by_station.csv  MAE per station (and ALL)
  baseline_mae_by_month.csv    MAE per calendar month of the test period
  baseline_warnings.csv        warning counts at 35 ug/m3 (caught / missed / false alarms)

Two kinds of comparison:
  persist      scored on every test row
  persist_c / cams   scored only on rows that have a CAMS value, so the two are comparable
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "experiments"
WARN_AT = 35.0  # ug/m3, US EPA 24-hour PM2.5 standard (suggested by the brief)


def mae(actual: pd.Series, pred: pd.Series) -> float:
    return float((actual - pred).abs().mean())


def mae_table(test: pd.DataFrame, by: str) -> pd.DataFrame:
    """One row per group: n rows, persistence MAE, and persistence vs CAMS on CAMS rows."""
    rows = []
    groups = list(test.groupby(by)) + [("ALL", test)]
    for name, g in groups:
        c = g.dropna(subset=["cams_tomorrow"])
        rows.append({
            by: name,
            "n": len(g),
            "mae_persist": round(mae(g.target_pm25, g.persist), 1),
            "n_cams": len(c),
            "mae_persist_c": round(mae(c.target_pm25, c.persist), 1) if len(c) else None,
            "mae_cams": round(mae(c.target_pm25, c.cams_tomorrow), 1) if len(c) else None,
        })
    return pd.DataFrame(rows)


def warning_counts(actual: pd.Series, pred: pd.Series, name: str) -> dict:
    """Raw counts for a warning rule 'warn if predicted > WARN_AT'."""
    bad = actual > WARN_AT
    warn = pred > WARN_AT
    caught = int((bad & warn).sum())
    return {
        "forecast": name,
        "n_days": len(actual),
        "unhealthy_days": int(bad.sum()),
        "caught": caught,
        "missed": int((bad & ~warn).sum()),
        "false_alarms": int((~bad & warn).sum()),
        "warnings_issued": int(warn.sum()),
        "recall": f"{caught} of {int(bad.sum())}",
        "precision": f"{caught} of {int(warn.sum())}",
    }


def main() -> None:
    df = pd.read_csv(DATA_DIR / "features.csv", parse_dates=["date"])
    test = df[df["split"] == "test"].copy()
    test["persist"] = test["pm25_today"]
    test["month"] = test["date"].dt.to_period("M").astype(str)

    by_station = mae_table(test, "station")
    by_month = mae_table(test, "month")
    c = test.dropna(subset=["cams_tomorrow"])
    warnings = pd.DataFrame([
        warning_counts(test.target_pm25, test.persist, "persist (all rows)"),
        warning_counts(c.target_pm25, c.persist, "persist (CAMS rows)"),
        warning_counts(c.target_pm25, c.cams_tomorrow, "CAMS (CAMS rows)"),
    ])

    OUT_DIR.mkdir(exist_ok=True)
    by_station.to_csv(OUT_DIR / "baseline_mae_by_station.csv", index=False)
    by_month.to_csv(OUT_DIR / "baseline_mae_by_month.csv", index=False)
    warnings.to_csv(OUT_DIR / "baseline_warnings.csv", index=False)

    print(f"Test period {test.date.min().date()} to {test.date.max().date()}, {len(test)} station-days")
    print("MAE in ug/m3, lower is better\n")
    print(by_station.to_string(index=False), "\n")
    print(by_month.to_string(index=False), "\n")
    print(f"Warnings at > {WARN_AT} ug/m3\n")
    print(warnings.to_string(index=False))
    print(f"\nSaved to {OUT_DIR}")


if __name__ == "__main__":
    main()
