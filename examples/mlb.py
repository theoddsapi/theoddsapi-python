#!/usr/bin/env python3
"""MLB example: upcoming moneylines + best price per team across books.

Free tier. Get a key at https://bettingdataapi.com/start then:
    pip install theoddsapi-client
    export THEODDSAPI_API_KEY=your_key_here
    python3 examples/mlb.py

Uses GET /odds/?sport_key=baseball_mlb&markets=h2h.
"""
from theoddsapi import TheOddsAPI

client = TheOddsAPI()  # reads THEODDSAPI_API_KEY

events = client.odds("baseball_mlb", markets="h2h", bookmakers="draftkings,fanduel")

if not events:
    print("No upcoming MLB games in the current window.")
    raise SystemExit(0)

print(f"{len(events)} upcoming MLB games\n")

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
