#!/usr/bin/env python3
"""Fair odds example: vig-removed consensus price, moneyline (Business plan).

    pip install theoddsapi-client
    export THEODDSAPI_API_KEY=your_key_here
    python3 examples/fair_odds.py

Covers the h2h (moneyline) market only today -- that's the endpoint's
current scope, not a bug in this script. Passing any other market
(spreads, totals, player props) returns an HTTP 400 with a roadmap
message; don't build on those until the API says they're supported.

The response includes a method_note disclosing that "fair" here means
consensus across the tracked retail/offshore books, not a sharp-anchored
price -- there's no Pinnacle or Circa in this feed.
"""
from theoddsapi import TheOddsAPI, TheOddsAPIError

client = TheOddsAPI()  # reads THEODDSAPI_API_KEY

try:
    fair = client.fair_odds("baseball_mlb", market="h2h")
except TheOddsAPIError as e:
    if e.status == 403:
        print("Fair odds require the Business plan:", e.detail)
    else:
        print(f"Request failed ({e.status}): {e.detail}")
    raise SystemExit(1)

if not fair:
    print("No fair-odds data in the current window.")
    raise SystemExit(0)

for entry in (fair if isinstance(fair, list) else [fair])[:5]:
    note = entry.get("method_note") if isinstance(entry, dict) else None
    print(entry)
    if note:
        print(f"  note: {note}")
