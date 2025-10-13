from pydantic import BaseModel, Field
from typing import Optional

class StockQuoteOutput(BaseModel):
    """
    Represents the simplified stock quote response from Finnhub's /quote endpoint.
    """
    current_price: float = Field(..., alias='c')

    high_price: float = Field(..., alias='h')

    low_price: float = Field(..., alias='l')

    open_price: float = Field(..., alias='o')

    previous_close: float = Field(..., alias='pc')

    timestamp: int = Field(..., alias='t')

    class Config:
        # Allows Pydantic to map the JSON keys ('c', 'h', etc.) to Python field names (current_price)
        populate_by_name = True

class CompanyProfileOutput(BaseModel):
    """
    Represents the simplified company profile response from Finnhub's /stock/profile2 endpoint.
    """
    name: str = Field(..., alias='name')
    ticker: str = Field(..., alias='ticker')
    exchange: str = Field(..., alias='exchange')
    ipo: str = Field(..., alias='ipo')
    phone: str = Field(..., alias='phone')
    market_cap: float = Field(..., alias='marketCapitalization')
    share_outstanding: float = Field(..., alias='shareOutstanding')
    logo_url: str = Field(..., alias='logo')
    web_url: str = Field(..., alias='weburl')
    industry: str = Field(..., alias='industry')
    country: str = Field(..., alias='country')
    currency: str = Field(..., alias='currency')

    class Config:
        # Allows Pydantic to map the JSON keys to Python field names
        populate_by_name = True