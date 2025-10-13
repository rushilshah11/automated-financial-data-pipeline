"""
Client for interacting with the external Finnhub API.
Wraps the synchronous Finnhub library to make it safely callable within 
FastAPI's asynchronous context using asyncio.to_thread.
"""

import finnhub
from app.settings import settings
from fastapi import HTTPException
import asyncio
from typing import Any, Optional, Dict
from app.core.integrations.finnhub_schema import StockQuoteOutput, CompanyProfileOutput

class FinnhubClient:
    """
    Thin wrapper around the synchronous finnhub.Client.

    Purpose:
    - Instantiate the finnhub client correctly with the API key.
    - Expose async methods (get_stock_quote, get_company_profile) that
      run the blocking finnhub calls off the event loop so they don't
      block other async tasks.
    """
        
    def __init__(self):
        api_key = settings.FINNHUB_API_KEY
        self.client = finnhub.Client(api_key=api_key)
    
    async def run_sync_call(self, func, *args, **kwargs):
        """
        Run a synchronous function in a separate thread and await its result.

        Why:
        - finnhub.Client methods are blocking (perform network I/O).
        - In an async FastAPI endpoint, calling a blocking function directly
          would block the event loop and halt concurrency.
        - asyncio.to_thread schedules the blocking call on a thread from the
          default thread pool and returns a coroutine you can await.

        How it works (high level):
        - asyncio.to_thread(func, *args, **kwargs) submits func to a thread
          and returns a coroutine. Awaiting that coroutine yields the return
          value of func once it finishes.
        """
        return await asyncio.to_thread(func, *args, **kwargs)

    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Response Attributes:
            c: Current price, d: Change, dp: Percent change, h: High price of the day, l: Low price of the day, o: Open price of the day, pc: Previous close price, pc: Previous close price
        """
        try:
            # call the blocking library off the event loop
            quote = await self.run_sync_call(self.client.quote, symbol.upper())
            if not quote or quote.get('c') == 0:
                raise HTTPException(status_code=404, detail=f"Quote for symbol '{symbol}' not found.")
            # Convert to a Pydantic model for structured typing and validation.
            # Using model_validate for Pydantic v2 compatibility.
            try:
                return StockQuoteOutput.model_validate(quote)
            except Exception:
                # If validation fails, fall back to returning the raw dict
                return quote
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Finnhub quote fetch failed: {e}")


    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Response Attributes:
            country: Country of company's headquarter.
            currency: Currency used in company filings.
            exchange: Listed exchange.
            finnhubIndustry: Finnhub industry classification.
            ipo: IPO date.
            logo: Logo image.
            marketCapitalization: Market Capitalization.
            name: Company name.
            phone: Company phone number.
            shareOutstanding: Number of oustanding shares.
            ticker: Company symbol/ticker as used on the listed exchange.
            weburl: Company website.
        """

        try:
            profile = await self.run_sync_call(self.client.company_profile2, symbol=symbol.upper())
            if not profile or profile.get('name') is None:
                raise HTTPException(status_code=404, detail=f"Profile for symbol '{symbol}' not found.")
            try:
                return CompanyProfileOutput.model_validate(profile)
            except Exception:
                return profile
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Finnhub profile fetch failed: {e}")



