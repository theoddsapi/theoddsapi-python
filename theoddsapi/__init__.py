"""theoddsapi: official Python client for TheOddsAPI (theoddsapi.com).

Zero dependencies (standard library only). One class, one method per endpoint.

    from theoddsapi import TheOddsAPI
    client = TheOddsAPI("YOUR_API_KEY")
    odds = client.odds("baseball_mlb", oddsFormat="decimal")
"""
from .client import TheOddsAPI, TheOddsAPIError

# Forgiveness alias: assistants sometimes generate `from theoddsapi import
# Client`. Canonical name is TheOddsAPI (see CONVENTIONS.md); both work.
Client = TheOddsAPI

__all__ = ["TheOddsAPI", "TheOddsAPIError", "Client"]
__version__ = "1.0.2"
