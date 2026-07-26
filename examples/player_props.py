#!/usr/bin/env python3
"""Player props example: NBA player points across books (Business plan).

    pip install theoddsapi-client
    export THEODDSAPI_API_KEY=your_key_here
    python3 examples/player_props.py

Guide: https://theoddsapi.com/guides/nba-player-props-edge-detection

Note: props responses follow the same events/books/outcomes envelope as
GET /odds/, but the exact market-specific fields can vary by sport. This
script prints defensively (won't crash on an unfamiliar shape) rather
than assume field names it hasn't seen live -- inspect the raw output
for your account before building on top of it.
"""
import json

from theoddsapi import TheOddsAPI, TheOddsAPIError

client = TheOddsAPI()  # reads THEODDSAPI_API_KEY

try:
    events = client.props("basketball_nba", markets="player_points")
except TheOddsAPIError as e:
    if e.status == 403:
        print("Player props require the Business plan:", e.detail)
    else:
        print(f"Request failed ({e.status}): {e.detail}")
    raise SystemExit(1)

if not events:
    print("No player props in the current window (likely off-season).")
    raise SystemExit(0)

print(f"{len(events)} events with player props\n")
print("First event, raw shape:")
print(json.dumps(events[0], indent=2, default=str)[:1000])
