#!/usr/bin/env python3
"""NBA example: upcoming moneylines + best price per team across books.

Free tier. Get a key at https://theoddsapi.com/start then:
    pip install theoddsapi-client
    export THEODDSAPI_API_KEY=your_key_here
    python3 examples/nba.py

Uses GET /odds/?sport_key=basketball_nba&markets=h2h. During the NBA
off-season this may return an empty list -- that's expected, not a bug.
"""
from theoddsapi import TheOddsAPI

client = TheOddsAPI()  # reads THEODDSAPI_API_KEY

events = client.odds("basketball_nba", markets="h2h", bookmakers="draftkings,fanduel")

if not events:
    print("No upcoming NBA games in the current window (likely off-season).")
    raise SystemExit(0)

print(f"{len(events)} upcoming NBA games\n")

for event in events[:5]:
    best = {}  # team name -> (price, book)
    for entry in event.get("books", []):
        if entry.get("market") != "h2h":
            continue
        for outcome in entry.get("outcomes", []):
            team, price = outcome.get("name"), outcome.get("price")
            if team is None or price is None:
                continue
            if team not in best or price > best[team][0]:
                best[team] = (price, entry.get("book"))
    print(f"{event.get('away_team')} at {event.get('home_team')}")
    for team, (price, book) in best.items():
        print(f"  best {team}: {price:+g} at {book}")
