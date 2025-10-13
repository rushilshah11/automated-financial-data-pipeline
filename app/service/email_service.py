"""
Business logic for periodic data aggregation and email dispatch.

This service orchestrates the fetching of stock data and the sending of 
customized updates to subscribed users. It uses Pydantic models for type safety 
when handling financial data.
"""

from typing import Dict, Any, Union
from sqlalchemy.orm import Session
import asyncio
import logging # New import for logging

from app.db.repository.subscription_repo import SubscriptionRepository
from app.db.repository.user_repo import UserRepository
from app.core.integrations.finnhub_client import FinnhubClient
from app.core.integrations.email_client import EmailClient
from app.db.models.user import User
from app.core.integrations.finnhub_schema import StockQuoteOutput, CompanyProfileOutput


# Initialize logger for this module
logger = logging.getLogger(__name__)
# NOTE: You will need to configure the root logger in main.py or settings to see output.

# Define a type alias for the complex dictionary structure for clarity
FinancialData = Dict[str, Dict[str, Union[StockQuoteOutput, CompanyProfileOutput, None]]]

class EmailService:
    def __init__(self, session: Session):
        self._sub_repo = SubscriptionRepository(session)
        self._user_repo = UserRepository(session)
        self._finnhub_client = FinnhubClient()
        self._email_client = EmailClient()

    async def _fetch_all_stock_data(self) -> FinancialData:
        """
        Step 1: Get all unique tickers and fetch their quote and profile 
        data in parallel using FinnhubClient.
        """
        unique_tickers = self._sub_repo.get_all_unique_tickers()
        if not unique_tickers:
            logger.info("No subscriptions found to fetch data for.")
            return {}

        logger.info("Fetching data for unique tickers: %s", unique_tickers)
        
        async def fetch_ticker_data(ticker: str) -> Dict[str, Union[str, StockQuoteOutput, CompanyProfileOutput, None]]:
            # These calls now return Pydantic models or None
            profile = await self._finnhub_client.get_company_profile(ticker)
            quote = await self._finnhub_client.get_stock_quote(ticker)
            
            return {
                "ticker": ticker,
                "quote": quote,
                "profile": profile,
            }

        tasks = [fetch_ticker_data(ticker) for ticker in unique_tickers]
        
        # Gather results concurrently
        # ARCHITECTURAL DECISION: RESILIENCE VS. CONTRACT
        #
        # FinnhubClient raises exceptions (e.g., HTTPException 404/500) to enforce
        # its contract (get data or fail immediately).
        #
        # Here, we use `return_exceptions=True` to prevent a single ticker failure
        # from stopping the entire job. The exceptions are gathered as values in
        # the 'results' list, allowing the subsequent loop to log the failures
        # gracefully and continue processing the successful tickers.
        # 
        # This behavior allows the EmailService to manage failures at the aggregation level:

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_stock_data: FinancialData = {}
        for res in results:
            if isinstance(res, Exception):
                # Log non-critical errors (we can continue with other tickers)
                error_detail = getattr(res, 'detail', str(res))
                logger.error("Error fetching data for a ticker: %s", error_detail)
            else:
                # Store the Pydantic models or None
                all_stock_data[res["ticker"]] = {
                    "quote": res["quote"],
                    "profile": res["profile"],
                }
        
        return all_stock_data

    def _prepare_user_data(self, user: User, all_stock_data: FinancialData) -> FinancialData:
        """
        Filters the full stock data to include only the tickers the user 
        is subscribed to.
        """
        user_subscribed_data: FinancialData = {}
        # Use a set for efficient lookup
        user_tickers = {sub.ticker for sub in user.subscriptions} 

        for ticker in user_tickers:
            if ticker in all_stock_data:
                user_subscribed_data[ticker] = all_stock_data[ticker]
            # Tickers for which data fetching failed are automatically skipped

        return user_subscribed_data


    async def dispatch_daily_updates(self) -> int:
        """
        Main function to orchestrate the daily update process.
        """
        # 1. Aggregate financial data (contains Pydantic models)
        all_stock_data = await self._fetch_all_stock_data()
        count = 0
        
        if not all_stock_data:
            return

        # 2. Get all users who have subscriptions
        users_with_subscriptions = self._user_repo.get_users_for_email_dispatch()
        
        if not users_with_subscriptions:
            logger.info("No users with active subscriptions found. Dispatch complete.")
            return

        logger.info("Found %d users to send emails to.", len(users_with_subscriptions))

        # 3. Filter data per user and dispatch email
        for user in users_with_subscriptions:
            user_data_to_send = self._prepare_user_data(user, all_stock_data)
            
            if user_data_to_send:
                first_name = user.first_name if user.first_name else "Valued Customer"
                
                # Pass Pydantic models to the email client
                self._email_client.send_stock_update(
                    recipient_email=user.email,
                    first_name=first_name,
                    user_subscribed_data=user_data_to_send
                )
                count += 1
                logger.debug("Successfully dispatched email for user: %s", user.email)
            else:
                logger.warning("Skipping email for user %s: no valid data found for subscribed tickers.", user.email)
                
        logger.info("Daily email dispatch completed.")
        return count
