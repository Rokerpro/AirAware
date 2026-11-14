"""Count how many days actually have PM2.5 data for candidate Kathmandu stations.

Run from the repo root:  .venv/bin/python ml/src/check_gaps.py
Uses OpenAQ's daily aggregates (/v3/sensors/{id}/days), so it is cheap.
Prints coverage over each station's span and over the last 365 days.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta

from find_stations import load_key

BASE = "https://api.openaq.org/v3"
# id -> label. Long-history stations first, then a few of the ~1-year GD Labs network.
CANDIDATES = {
    3459: "Embassy Kathmandu",
    3460: "Phora Durbar",
    1236017: "Dhathutole, Handigaun",
    2848864: "Dabali, Handigaun",
    4121681: "KIAS",
    5506835: "Gaushala Chowk (SC-01)",
    5509787: "Baluwatar (SC-02)",
    5509788: "Lagankhel (SC-05)",
    6070692: "Shantichowk (SC-11)",
    6093548: "Tarakeswor (SC-14)",
}
FROM = "2017-01-01"


def get(path: str, key: str, **params) -> dict:
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"X-API-Key": key, "Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:  # rate limited: wait and retry
                time.sleep(5 * (attempt + 1))
                continue
            raise SystemExit(f"HTTP {e.code} for {path}")
    raise SystemExit(f"Still rate limited on {path}")


def pm25_sensor_id(loc_id: int, key: str) -> int | None:
    for s in get(f"/locations/{loc_id}/sensors", key).get("results", []):
        if s.get("parameter", {}).get("name") == "pm25":
            return s["id"]
    return None


def daily_dates(sensor_id: int, key: str) -> set[date]:
    days: set[date] = set()
    page = 1
    while True:
        res = get(f"/sensors/{sensor_id}/days", key, datetime_from=FROM,
                  datetime_to=date.today().isoformat(), limit=1000, page=page).get("results", [])
        for r in res:
            days.add(date.fromisoformat(r["period"]["datetimeFrom"]["local"][:10]))
        if len(res) < 1000:
            return days
        page += 1
        time.sleep(1)


def main() -> None:
    key = load_key()
    print(f"{'id':>8}  {'days':>5}  {'span':>5}  {'cover':>6}  {'last365':>7}  name")
    for loc_id, name in CANDIDATES.items():
        sid = pm25_sensor_id(loc_id, key)
        if sid is None:
            print(f"{loc_id:>8}  no pm25 sensor  {name}")
            continue
        days = daily_dates(sid, key)
        if not days:
            print(f"{loc_id:>8}  no daily data   {name}")
            continue
        span = (max(days) - min(days)).days + 1
        recent = sum(1 for d in days if d >= date.today() - timedelta(days=365))
        print(f"{loc_id:>8}  {len(days):>5}  {span:>5}  {len(days) / span:>6.0%}  {recent:>7}  {name}")
        time.sleep(1)
    print("\ncover = days with data / days between first and last. last365 = days with data in the past year.")


if __name__ == "__main__":
    main()
