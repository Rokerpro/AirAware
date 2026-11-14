"""Tests for the data split, saved models and the inference module.

Run from the repo root:  .venv/bin/python -m unittest discover -s ml/tests -v
Uses only the standard library's unittest, so no extra install is needed.
"""
import json
import sys
import unittest
from pathlib import Path

import pandas as pd

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import predict  # noqa: E402
from build_features import FEATURES, TEST_START  # noqa: E402

DATA = SRC.parent / "data" / "features.csv"
META = SRC.parent / "models" / "meta.json"


class TestNoLeakage(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv(DATA, parse_dates=["date"])

    def test_split_is_by_time(self):
        train, test = self.df[self.df.split == "train"], self.df[self.df.split == "test"]
        self.assertLess(train.date.max(), pd.Timestamp(TEST_START))
        self.assertGreaterEqual(test.date.min(), pd.Timestamp(TEST_START))

    def test_target_and_cams_are_not_features(self):
        self.assertNotIn("target_pm25", FEATURES)
        self.assertNotIn("cams_tomorrow", FEATURES)

    def test_target_is_next_day_value(self):
        # target on day D must equal pm25_today on day D+1 for the same station
        df = self.df.sort_values(["station_id", "date"])
        nxt = df.groupby("station_id").shift(-1)
        consecutive = (nxt.date - df.date) == pd.Timedelta(days=1)
        self.assertTrue(consecutive.any())
        self.assertTrue((df.target_pm25[consecutive] == nxt.pm25_today[consecutive]).all())

    def test_models_trained_before_test_start(self):
        meta = json.loads(META.read_text())
        self.assertLess(pd.Timestamp(meta["train_dates"][1]), pd.Timestamp(meta["test_start"]))


class TestBands(unittest.TestCase):
    def test_aqi_band_edges(self):
        self.assertEqual(predict.aqi_band(9.0), "Good")
        self.assertEqual(predict.aqi_band(35.4), "Moderate")
        self.assertEqual(predict.aqi_band(35.5), "Unhealthy for Sensitive Groups")
        self.assertEqual(predict.aqi_band(55.5), "Unhealthy")
        self.assertEqual(predict.aqi_band(300), "Hazardous")

    def test_alert_levels(self):
        self.assertEqual(predict.alert_level(35.0), "none")   # warn only ABOVE 35
        self.assertEqual(predict.alert_level(35.1), "warning")
        self.assertEqual(predict.alert_level(55.5), "high")


class TestForecast(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stations = predict.list_stations()["stations"]

    def test_health(self):
        self.assertEqual(predict.health(), {"status": "ok", "model_loaded": True})

    def test_six_stations(self):
        self.assertEqual(len(self.stations), 6)

    def test_contract_fields(self):
        s = self.stations[0]
        out = predict.forecast(s["station_id"], s["last_date"])
        for key in ("station_id", "station_name", "forecast_for", "predicted_pm25", "aqi_band",
                    "warning", "baselines", "precaution", "disclaimer", "model_version"):
            self.assertIn(key, out)
        self.assertEqual(out["disclaimer"], "Prototype, not health advice.")
        self.assertIsInstance(out["warning"], bool)
        self.assertGreaterEqual(out["predicted_pm25"], 0)
        json.dumps(out)  # must be JSON-serialisable

    def test_past_date_has_actual(self):
        out = predict.forecast("3459", "2026-01-15")
        self.assertEqual(out["forecast_for"], "2026-01-16")
        self.assertIsNotNone(out["actual_pm25"])

    def test_nepali(self):
        s = self.stations[0]
        out = predict.forecast(s["station_id"], s["last_date"], language="ne")
        self.assertNotEqual(out["disclaimer"], "Prototype, not health advice.")

    def test_errors(self):
        cases = [
            (("999", "2026-01-15"), "unknown_station"),
            (("3459", "2026-13-45"), "invalid_date"),
            (("3459", "2030-01-01"), "date_out_of_range"),
            (("3459", "2026-01-15", "fr"), "invalid_language"),
        ]
        for args, code in cases:
            with self.assertRaises(predict.ForecastError) as ctx:
                predict.forecast(*args)
            self.assertEqual(ctx.exception.code, code)
            self.assertIn("error", ctx.exception.to_dict())


if __name__ == "__main__":
    unittest.main()
