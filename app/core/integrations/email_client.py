"""
Mock client for sending emails. 

This client uses Pydantic schemas for data access, ensuring that only the
expected fields from the financial data are used and are strongly typed.
"""

from typing import Dict, Any, Union
import logging # New import for logging
from pydantic import EmailStr
from app.settings import settings
from app.core.integrations.finnhub_schema import StockQuoteOutput, CompanyProfileOutput 


# Initialize logger for this module
logger = logging.getLogger(__name__)

# Define a type alias for the complex dictionary structure for clarity
# This structure maps a ticker to a dictionary containing the two Pydantic models (which can be None if fetching failed)
FinancialData = Dict[str, Dict[str, Union[StockQuoteOutput, CompanyProfileOutput, None]]]

class EmailClient:
    def __init__(self):
        self.sender_email = settings.EMAIL_FROM_ADDRESS

    def _format_message(self, first_name: str, stock_data: FinancialData) -> str:
        """Helper to format the email body content with stock and company info."""
        message = f"Hello {first_name},\n\nHere is your financial data update for your subscribed tickers:\n\n"
        
        for ticker, data in stock_data.items():
            # Data values are Pydantic models (or None)
            company_profile: CompanyProfileOutput | None = data.get("profile")
            stock_quote: StockQuoteOutput | None = data.get("quote")
            
            # Use direct attribute access for Pydantic models, falling back gracefully
            
            # --- Company Profile Data ---
            name = company_profile.name if company_profile else "N/A"
            exchange = company_profile.exchange if company_profile else "N/A"
            industry = company_profile.finnhubIndustry if company_profile else "N/A"
            web_url = company_profile.weburl if company_profile else "#"

            # --- Stock Quote Data ---
            current_price = stock_quote.current_price if stock_quote else "N/A"
            high = stock_quote.high_price if stock_quote else "N/A"
            low = stock_quote.low_price if stock_quote else "N/A"
            
            message += f"--- {ticker} ({name}) ---\n"
            message += f"Current Price: {current_price}\n"
            message += f"Daily High: {high}\n"
            message += f"Daily Low: {low}\n"
            message += f"Exchange: {exchange}\n"
            message += f"Industry: {industry}\n"
            message += f"Website: {web_url}\n"
            message += "--------------------------\n\n"

        message += "To manage your subscriptions, please log into the app.\n\nBest regards,\nThe Financial Pipeline Team"
        return message

    def send_stock_update(self, recipient_email: EmailStr, first_name: str, user_subscribed_data: FinancialData) -> bool:
        """
        MOCK: Simulates sending the email using logging instead of print.
        """
        subject = "Your Daily Financial Data Update"
        body = self._format_message(first_name, user_subscribed_data)

        # Log the mock email contents using INFO level
        logger.info("="*50)
        logger.info("MOCK EMAIL DISPATCH")
        logger.info("Sending to: %s", recipient_email)
        logger.info("From: %s", self.sender_email)
        logger.info("Subject: %s", subject)
        # Logging the full body at DEBUG level is often preferred, but INFO is kept for visibility in mock environment
        logger.info("\n%s", body) 
        logger.info("="*50)

        return True
