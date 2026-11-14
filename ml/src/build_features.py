"""Merge the raw CSVs into one modelling table: features for day D, target = PM2.5 on D+1.

Run from the repo root:  .venv/bin/python ml/src/build_features.py
Reads  ml/data/{pm25,weather,cams}_daily.csv   Writes  ml/data/features.csv

No leakage: every feature uses only data from day D or earlier. The target and the CAMS
baseline column come from day D+1 and are never used as inputs. The train/test split is by
time (one cutoff date for every station), never random.
"""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MIN_COVERAGE_PCT = 75   # drop station-days with less data than this (judgement call, tunable)
TEST_START = "2025-11-01"  # rows with date >= this are test. Covers winter smog + spring burning
FEATURES = ["pm25_today", "pm25_yesterday", "pm25_mean3", "temp_c", "humidity_pct",
            "wind_kmh", "precip_mm", "pressure_hpa", "month"]


def build() -> pd.DataFrame:
    pm = pd.read_csv(DATA_DIR / "pm25_daily.csv", parse_dates=["date"])
    pm = pm[pm["coverage_pct"] >= MIN_COVERAGE_PCT]
    weather = pd.read_csv(DATA_DIR / "weather_daily.csv", parse_dates=["date"])
    cams = pd.read_csv(DATA_DIR / "cams_daily.csv", parse_dates=["date"])

    out = []
    for (sid, name), g in pm.groupby(["station_id", "station"]):
        # full daily calendar so shifts mean "exactly one day", with NaN for missing days
        g = g.set_index("date")["pm25"].asfreq("D").to_frame("pm25_today")
        g["pm25_yesterday"] = g["pm25_today"].shift(1)
        g["pm25_mean3"] = g["pm25_today"].rolling(3, min_periods=3).mean()  # D-2..D
        g["target_pm25"] = g["pm25_today"].shift(-1)                          # D+1
        g["station_id"], g["station"] = sid, name
        out.append(g.reset_index())
    df = pd.concat(out, ignore_index=True)

    df = df.merge(weather, on="date", how="left")
    df["month"] = df["date"].dt.month
    # CAMS value for the day we predict (D+1): a baseline to compare against, not an input
    cams_next = cams.assign(date=cams["date"] - pd.Timedelta(days=1)).rename(
        columns={"cams_pm25": "cams_tomorrow"})
    df = df.merge(cams_next, on="date", how="left")

    df = df.dropna(subset=FEATURES + ["target_pm25"])
    df["split"] = (df["date"] >= TEST_START).map({True: "test", False: "train"})
    return df[["station_id", "station", "date", "split"] + FEATURES + ["target_pm25", "cams_tomorrow"]]


def main() -> None:
    df = build()
    df.to_csv(DATA_DIR / "features.csv", index=False)
    print(f"Saved {len(df)} rows to {DATA_DIR / 'features.csv'}\n")
    print(df.pivot_table(index="station", columns="split", values="target_pm25",
                         aggfunc="count", fill_value=0))
    print("\nrows with a CAMS baseline value:", df["cams_tomorrow"].notna().sum())


if __name__ == "__main__":
    main()
