#!/usr/bin/env python3
"""Arbitrage example: cross-book two-outcome opportunities (Business plan).

    pip install theoddsapi-client
    export THEODDSAPI_API_KEY=your_key_here
    python3 examples/arbitrage.py

Guide: https://theoddsapi.com/guides/arbitrage-detection

Today this covers two-outcome h2h markets only. Every opportunity
carries detected_at / age_seconds (server-side precompute age) and a
latency_warning, since arb windows can close in seconds while odds
refresh on a slower cycle -- always check age_seconds before acting.
Opportunities over ~5% profit are flagged likely_stale rather than
trusted at face value.
"""
from theoddsapi import TheOddsAPI, TheOddsAPIError

client = TheOddsAPI()  # reads THEODDSAPI_API_KEY

try:
    opportunities = client.arbitrage("basketball_nba")
except TheOddsAPIError as e:
    if e.status == 403:
        print("Arbitrage detection requires the Business plan:", e.detail)
    else:
        print(f"Request failed ({e.status}): {e.detail}")
    raise SystemExit(1)

if not opportunities:
    print("No arbitrage opportunities detected right now.")
    raise SystemExit(0)

print(f"{len(opportunities)} opportunities\n")

for opp in opportunities[:5]:
    profit = opp.get("profit_pct")
    age = opp.get("age_seconds")
    flag = " (likely_stale)" if opp.get("likely_stale") else ""
    print(f"profit={profit}%  age={age}s{flag}  {opp.get('event_id', opp)}")
