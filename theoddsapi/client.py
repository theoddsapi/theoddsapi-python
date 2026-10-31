"""HTTP client for Betting Data API. Standard library only, retries on 5xx."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.bettingdataapi.com"
ENV_KEY = "THEODDSAPI_API_KEY"
RETRY_STATUSES = {502, 503, 504}


class TheOddsAPIError(Exception):
    """Raised for any non-2xx API response. Carries .status and .detail."""

    def __init__(self, status, detail):
        self.status = status
        self.detail = detail
        super().__init__(f"HTTP {status}: {detail}")


class TheOddsAPI:
    """Thin client for Betting Data API. Docs: https://bettingdataapi.com/docs/"""

    def __init__(self, api_key=None, base_url=BASE_URL, timeout=15, max_retries=3):
        self.api_key = api_key or os.environ.get(ENV_KEY)
        if not self.api_key:
            raise TheOddsAPIError(
                0, f"no API key: pass TheOddsAPI(\"key\") or set {ENV_KEY}. "
                   "Free key in minutes at https://bettingdataapi.com/start")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    # ------------------------------------------------------------- core ----
    def _get(self, path, params=None):
        query = urllib.parse.urlencode(
            {k: v for k, v in (params or {}).items() if v is not None})
        url = f"{self.base_url}{path}" + (f"?{query}" if query else "")
        req = urllib.request.Request(url, headers={
            "x-api-key": self.api_key,
            "User-Agent": "theoddsapi-python/1.0.3",
        })
        delay = 1.0
        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code in RETRY_STATUSES and attempt < self.max_retries:
                    time.sleep(delay)
                    delay = min(delay * 2, 30)
                    continue
                try:
                    detail = json.loads(e.read().decode("utf-8")).get("detail", e.reason)
                except Exception:
                    detail = e.reason
                raise TheOddsAPIError(e.code, detail) from None
            except urllib.error.URLError as e:
                if attempt < self.max_retries:
                    time.sleep(delay)
                    delay = min(delay * 2, 30)
                    continue
                raise TheOddsAPIError(0, f"connection failed: {e.reason}") from None

    # -------------------------------------------------------- core data ----
    def sports(self):
        """List the sports available on your plan."""
        return self._get("/sports/")

    def odds(self, sport_key, **params):
        """Current multi-book odds for a sport. Params: markets, regions,
        bookmakers, event_id, commenceTimeFrom, commenceTimeTo, oddsFormat."""
        return self._get("/odds/", {"sport_key": sport_key, **params})

    def events(self, sport_key, **params):
        """Upcoming events for a sport."""
        return self._get("/events/", {"sport_key": sport_key, **params})

    def best_lines(self, sport_key, **params):
        """Best available price per outcome across all tracked books."""
        return self._get("/best-lines/", {"sport_key": sport_key, **params})

    # ---------------------------------------------- business endpoints ----
    def props(self, sport_key, **params):
        """Player props (Business plan)."""
        return self._get("/props/", {"sport_key": sport_key, **params})

    def edges(self, sport_key, **params):
        """Pinnacle-anchored cross-book edges (Business plan)."""
        return self._get("/edges/", {"sport_key": sport_key, **params})

    def fair_odds(self, sport_key, **params):
        """Vig-removed fair odds from sharp-anchored consensus (Business)."""
        return self._get("/intelligence/fair-odds", {"sport_key": sport_key, **params})

    def consensus(self, sport_key, **params):
        """Median/mean market center per outcome (Business)."""
        return self._get("/intelligence/consensus", {"sport_key": sport_key, **params})

    def arbitrage(self, sport_key, **params):
        """Precomputed cross-book arbitrage opportunities (Business)."""
        return self._get("/intelligence/arbitrage", {"sport_key": sport_key, **params})

    def value_bets(self, sport_key, **params):
        """Value bets vs vig-removed consensus (Business)."""
        return self._get("/intelligence/value", {"sport_key": sport_key, **params})

    def historical_odds(self, sport_key, **params):
        """Historical odds snapshots (Business). Params: from/to (use
        from_/to_ or pass via dict), event_id, bookmakers, market,
        limit, offset, oddsFormat."""
        clean = {k.rstrip("_"): v for k, v in params.items()}
        return self._get("/historical/odds", {"sport_key": sport_key, **clean})

    def historical_settlements(self, sport_key, **params):
        """Graded edge settlements joined with final scores (Business)."""
        return self._get("/historical/settlements", {"sport_key": sport_key, **params})

    # ------------------------------------------------------------ account --
    def me(self):
        """Your key's tier and usage."""
        return self._get("/me/")
