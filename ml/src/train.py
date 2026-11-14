"""Train the next-day PM2.5 models on the TRAIN split only and save them to ml/models/.

Run from the repo root:  .venv/bin/python ml/src/train.py

Steps
1. Split the train rows by time again: older rows "fit", the last 12 months "val".
   The val rows choose Random Forest settings. The test split is never touched here.
2. Refit the chosen models on ALL train rows and save them with joblib.

Models (one model shared by all stations, because most stations have < 150 train rows):
  linear_regression  ordinary least squares, easy to explain via its coefficients
  random_forest      many decision trees averaged, can learn non-linear effects (e.g. month)
"""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from build_features import FEATURES, TEST_START

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR, MODEL_DIR, OUT_DIR = ROOT / "data", ROOT / "models", ROOT / "experiments"
VAL_START = "2024-11-01"  # last 12 months of the train period, used only to pick RF settings
SEED = 42
RF_GRID = [  # small grid: deeper trees fit more detail, bigger leaves are smoother
    {"max_depth": d, "min_samples_leaf": leaf}
    for d in (6, 10, None) for leaf in (5, 20)
]


def mae(a: pd.Series, b) -> float:
    return float((a - b).abs().mean())


def make_rf(params: dict) -> RandomForestRegressor:
    return RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=-1, **params)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "features.csv", parse_dates=["date"])
    train = df[df["split"] == "train"]
    assert train["date"].max() < pd.Timestamp(TEST_START), "test rows leaked into train"
    fit, val = train[train["date"] < VAL_START], train[train["date"] >= VAL_START]
    print(f"fit rows {len(fit)} ({fit.date.min().date()}..{fit.date.max().date()}), "
          f"val rows {len(val)} ({val.date.min().date()}..{val.date.max().date()})\n")

    # Validation scores (MAE, ug/m3) for the baseline and every candidate
    val_rows = [{"model": "persistence", "params": "", "val_mae": mae(val.target_pm25, val.pm25_today)}]
    lr = LinearRegression().fit(fit[FEATURES], fit.target_pm25)
    val_rows.append({"model": "linear_regression", "params": "",
                     "val_mae": mae(val.target_pm25, lr.predict(val[FEATURES]))})
    for p in RF_GRID:
        rf = make_rf(p).fit(fit[FEATURES], fit.target_pm25)
        val_rows.append({"model": "random_forest", "params": json.dumps(p),
                         "val_mae": mae(val.target_pm25, rf.predict(val[FEATURES]))})
    val_table = pd.DataFrame(val_rows).round({"val_mae": 2})
    print(val_table.to_string(index=False), "\n")

    best = val_table[val_table.model == "random_forest"].sort_values("val_mae").iloc[0]
    best_params = json.loads(best.params)
    print(f"chosen RF settings: {best_params} (val MAE {best.val_mae})")

    # Refit on all train rows and save
    MODEL_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)
    final = {
        "linear_regression": LinearRegression().fit(train[FEATURES], train.target_pm25),
        "random_forest": make_rf(best_params).fit(train[FEATURES], train.target_pm25),
    }
    for name, model in final.items():
        joblib.dump(model, MODEL_DIR / f"{name}.joblib")
    meta = {
        "features": FEATURES,
        "target": "target_pm25 (next-day daily-average PM2.5, ug/m3)",
        "train_rows": len(train),
        "train_dates": [str(train.date.min().date()), str(train.date.max().date())],
        "test_start": TEST_START,
        "val_start": VAL_START,
        "rf_params": best_params,
        "seed": SEED,
        "model_versions": {"linear_regression": "linear_regression_v1",
                           "random_forest": "random_forest_v1"},
    }
    (MODEL_DIR / "meta.json").write_text(json.dumps(meta, indent=2))
    val_table.to_csv(OUT_DIR / "validation_scores.csv", index=False)

    coefs = pd.Series(final["linear_regression"].coef_, index=FEATURES).round(3)
    print("\nlinear regression coefficients (ug/m3 change per unit of each feature):")
    print(coefs.to_string())
    imp = pd.Series(final["random_forest"].feature_importances_, index=FEATURES)
    print("\nrandom forest feature importance (share of error reduction):")
    print(imp.sort_values(ascending=False).round(3).to_string())
    print(f"\nSaved models to {MODEL_DIR}")


if __name__ == "__main__":
    main()
