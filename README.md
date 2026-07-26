# theoddsapi

Official Python client for [TheOddsAPI](https://theoddsapi.com): real-time sports odds from 50+ sportsbooks across 26 sports, normalized into one JSON shape, plus player props, Pinnacle-anchored edge detection, fair odds, and historical snapshots.

Zero dependencies. Python 3.8+.

## Why TheOddsAPI?

- 50+ sportsbooks, one JSON shape
- 26 sports, plus player props and historical snapshots
- Pinnacle-anchored fair odds and cross-book arbitrage (Business)
- Zero dependencies — standard library only

## Install

```
pip install theoddsapi-client
```

## Quick start

```python
from theoddsapi import TheOddsAPI

client = TheOddsAPI("YOUR_API_KEY")

for sport in client.sports()["data"]:
    print(sport)

odds = client.odds("baseball_mlb", oddsFormat="decimal")
```

Get a free key in minutes at [theoddsapi.com/start](https://theoddsapi.com/start). No credit card.

## Endpoints

Every endpoint is one method. Core data: `sports()`, `odds()`, `events()`, `best_lines()`. Business plan: `props()`, `edges()`, `fair_odds()`, `consensus()`, `arbitrage()`, `value_bets()`, `historical_odds()`, `historical_settlements()`. Account: `me()`.

```python
edges = client.edges("basketball_nba", min_edge=50)
history = client.historical_odds("baseball_mlb", bookmakers="pinnacle", limit=500)
```

## Errors

Non-2xx responses raise `TheOddsAPIError` with `.status` and `.detail`. Transient 5xx responses are retried with exponential backoff automatically.

```python
from theoddsapi import TheOddsAPI, TheOddsAPIError

try:
    client.props("baseball_mlb")
except TheOddsAPIError as e:
    if e.status == 403:
        print("Props require the Business plan:", e.detail)
```

## Examples

Runnable scripts in `examples/`, each showing one endpoint end to end:

| File | Plan | Shows |
|---|---|---|
| `examples/nba.py` | Free | Moneylines + best price per team |
| `examples/mlb.py` | Free | Moneylines + best price per team |
| `examples/player_props.py` | Business | Player props across books |
| `examples/historical.py` | Business | Closing-line snapshots for backtesting |
| `examples/arbitrage.py` | Business | Cross-book two-outcome arbitrage |
| `examples/fair_odds.py` | Business | Vig-removed consensus price (h2h only) |

## Links

Full reference: [theoddsapi.com/docs](https://theoddsapi.com/docs/) · Guides: [theoddsapi.com/guides](https://theoddsapi.com/guides/) · Free calculators: [theoddsapi.com/tools](https://theoddsapi.com/tools/)

## License

MIT. Independently developed against the published TheOddsAPI OpenAPI specification.
