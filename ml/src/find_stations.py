"""List OpenAQ stations near Kathmandu that measure PM2.5, with their date range.

Run from the repo root:  .venv/bin/python ml/src/find_stations.py
Reads OPENAQ_API_KEY from .env or the environment. Never prints the key.
Uses only the standard library, so no extra installs are needed.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

KATHMANDU = (27.7172, 85.3240)  # lat, lon
RADIUS_M = 25_000  # OpenAQ v3 maximum
PM25_PARAMETER_ID = 2
URL = "https://api.openaq.org/v3/locations"


def load_key() -> str:
    key = os.environ.get("OPENAQ_API_KEY", "")
    env_file = Path(__file__).resolve().parents[2] / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("OPENAQ_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        raise SystemExit("OPENAQ_API_KEY is empty. Add it to .env first.")
    return key


def fetch_locations(key: str) -> list[dict]:
    params = {
        "coordinates": f"{KATHMANDU[0]},{KATHMANDU[1]}",
        "radius": RADIUS_M,
        "parameters_id": PM25_PARAMETER_ID,
        "limit": 100,
    }
    req = urllib.request.Request(
        f"{URL}?{urllib.parse.urlencode(params)}",
        headers={"X-API-Key": key, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp).get("results", [])
    except urllib.error.HTTPError as e:
        raise SystemExit(f"OpenAQ returned HTTP {e.code} (401 = bad key, 429 = rate limited).")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e.reason}")


def parse(ts: dict | None) -> datetime | None:
    if not ts or not ts.get("utc"):
        return None
    return datetime.fromisoformat(ts["utc"].replace("Z", "+00:00"))


def main() -> None:
    rows = []
    for loc in fetch_locations(load_key()):
        first, last = parse(loc.get("datetimeFirst")), parse(loc.get("datetimeLast"))
        days = (last - first).days if first and last else 0
        rows.append((days, loc["id"], loc.get("name"), first, last))
    rows.sort(key=lambda r: r[0], reverse=True)

    print(f"{len(rows)} PM2.5 locations within {RADIUS_M // 1000} km of Kathmandu\n")
    print(f"{'id':>8}  {'span(days)':>10}  {'first':10}  {'last':10}  name")
    for days, loc_id, name, first, last in rows:
        f = first.date() if first else "?"
        l = last.date() if last else "?"
        print(f"{loc_id:>8}  {days:>10}  {f!s:10}  {l!s:10}  {name}")
    print("\nSpan is first-to-last date only; it does not show gaps. Check gaps next.")


if __name__ == "__main__":
    main()
