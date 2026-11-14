"""Download daily PM2.5 (OpenAQ), weather and CAMS PM2.5 (Open-Meteo) into ml/data/.

Run from the repo root:  .venv/bin/python ml/src/fetch_data.py
Writes (all one row per date, dates in Asia/Kathmandu local time):
  ml/data/pm25_daily.csv   station_id, station, date, pm25, coverage_pct
  ml/data/weather_daily.csv  date, temp_c, humidity_pct, wind_kmh, precip_mm, pressure_hpa
  ml/data/cams_daily.csv   date, cams_pm25   (CAMS model via Open-Meteo, NOT a monitor)
Needs OPENAQ_API_KEY in .env. Open-Meteo needs no key.
Sources to cite: OpenAQ (openaq.org), Open-Meteo (open-meteo.com), CAMS (Copernicus).
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

from check_gaps import get, pm25_sensor_id
from find_stations import KATHMANDU, load_key

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
# Embassy has the long history. Phora Durbar stopped reporting, so it is left out.
STATIONS = {
    3459: "Embassy Kathmandu",
    5509788: "Lagankhel (SC-05)",
    6070692: "Shantichowk (SC-11)",
    2848864: "Dabali, Handigaun",
    4121681: "KIAS",
    5506835: "Gaushala Chowk (SC-01)",
}
FROM = "2017-01-01"
CAMS_START = "2022-08-01"  # Open-Meteo air-quality history starts around mid-2022
TZ = "Asia/Kathmandu"


def fetch_station_days(loc_id: int, name: str, key: str) -> pd.DataFrame:
    sid = pm25_sensor_id(loc_id, key)
    if sid is None:
        print(f"  {name}: no pm25 sensor, skipped")
        return pd.DataFrame()
    rows, page = [], 1
    while True:
        res = get(f"/sensors/{sid}/days", key, datetime_from=FROM,
                  datetime_to=date.today().isoformat(), limit=1000, page=page).get("results", [])
        for r in res:
            cov = r.get("coverage") or {}
            rows.append({
                "station_id": loc_id,
                "station": name,
                "date": r["period"]["datetimeFrom"]["local"][:10],
                "pm25": r["value"],
                "coverage_pct": cov.get("percentCoverage"),
            })
        if len(res) < 1000:
            break
        page += 1
        time.sleep(1)
    return pd.DataFrame(rows)


def open_meteo(url: str, params: dict) -> dict:
    full = f"{url}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(full, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10 * (attempt + 1))
                continue
            raise SystemExit(f"Open-Meteo HTTP {e.code}: {e.read()[:200]!r}")
    raise SystemExit("Open-Meteo still rate limited")


def fetch_weather(start: str, end: str) -> pd.DataFrame:
    data = open_meteo("https://archive-api.open-meteo.com/v1/archive", {
        "latitude": KATHMANDU[0], "longitude": KATHMANDU[1],
        "start_date": start, "end_date": end, "timezone": TZ,
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,wind_speed_10m_mean,"
                 "precipitation_sum,surface_pressure_mean",
    })["daily"]
    return pd.DataFrame({
        "date": data["time"],
        "temp_c": data["temperature_2m_mean"],
        "humidity_pct": data["relative_humidity_2m_mean"],
        "wind_kmh": data["wind_speed_10m_mean"],
        "precip_mm": data["precipitation_sum"],
        "pressure_hpa": data["surface_pressure_mean"],
    })


def fetch_cams(start: str, end: str) -> pd.DataFrame:
    data = open_meteo("https://air-quality-api.open-meteo.com/v1/air-quality", {
        "latitude": KATHMANDU[0], "longitude": KATHMANDU[1],
        "start_date": start, "end_date": end, "timezone": TZ, "hourly": "pm2_5",
    })["hourly"]
    hourly = pd.DataFrame({"time": pd.to_datetime(data["time"]), "pm2_5": data["pm2_5"]})
    hourly["date"] = hourly["time"].dt.strftime("%Y-%m-%d")
    daily = hourly.groupby("date", as_index=False)["pm2_5"].mean()
    return daily.rename(columns={"pm2_5": "cams_pm25"})


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    key = load_key()
    today = date.today().isoformat()

    print("OpenAQ daily PM2.5:")
    frames = []
    for loc_id, name in STATIONS.items():
        df = fetch_station_days(loc_id, name, key)
        print(f"  {name}: {len(df)} days")
        frames.append(df)
        time.sleep(1)
    pm = pd.concat(frames, ignore_index=True)
    pm = pm[pm["pm25"] >= 0]  # sensors sometimes report negative values; those are errors
    pm.to_csv(DATA_DIR / "pm25_daily.csv", index=False)

    first = pm["date"].min()
    print(f"Open-Meteo weather {first} to {today} ...")
    weather = fetch_weather(first, today)
    weather.to_csv(DATA_DIR / "weather_daily.csv", index=False)
    print(f"  {len(weather)} days")

    print(f"Open-Meteo CAMS PM2.5 {CAMS_START} to {today} ...")
    cams = fetch_cams(CAMS_START, today)
    cams.to_csv(DATA_DIR / "cams_daily.csv", index=False)
    print(f"  {len(cams)} days")
    print(f"\nSaved to {DATA_DIR}")


if __name__ == "__main__":
    main()
