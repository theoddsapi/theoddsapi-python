#!/usr/bin/env python3
"""Historical odds example: MLB closing-line snapshots (Business plan).

    pip install theoddsapi-client
    export THEODDSAPI_API_KEY=your_key_here
    python3 examples/historical.py

Guide: https://bettingdataapi.com/guides/historical-odds-backtesting

Defaults to the last 7 days if no from/to window is given; max limit
is 1000 rows per call, paginate with offset for more.
"""
import json

from theoddsapi import TheOddsAPI, TheOddsAPIError

client = TheOddsAPI()  # reads THEODDSAPI_API_KEY

try:
    result = client.historical_odds("baseball_mlb", bookmakers="pinnacle", limit=25)
except TheOddsAPIError as e:
    if e.status == 403:
        print("Historical odds require the Business plan:", e.detail)
    else:
        print(f"Request failed ({e.status}): {e.detail}")
    raise SystemExit(1)

rows = result.get("data", result) if isinstance(result, dict) else result
meta = result.get("meta") if isinstance(result, dict) else None

if not rows:
    print("No historical rows in the default 7-day window for this filter.")
    raise SystemExit(0)

print(f"{len(rows)} rows returned" + (f" (meta: {meta})" if meta else ""))
print("First row, raw shape:")
print(json.dumps(rows[0], indent=2, default=str)[:1000])
