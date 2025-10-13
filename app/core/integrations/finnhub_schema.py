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

    class ConfigDict:
        # Allows Pydantic to map the JSON keys ('c', 'h', etc.) to Python field names (current_price)
        populate_by_name = True

class CompanyProfileOutput(BaseModel):
    """
    Represents the simplified company profile response from Finnhub's /stock/profile2 endpoint.
    """
    country: str
    currency: str
    exchange: str
    finnhubIndustry: Optional[str] = None  # make optional
    ipo: Optional[str] = None
    logo: Optional[str] = None
    marketCapitalization: Optional[float] = None
    name: str
    phone: Optional[str] = None
    shareOutstanding: Optional[float] = None
    ticker: str
    weburl: Optional[str] = None
