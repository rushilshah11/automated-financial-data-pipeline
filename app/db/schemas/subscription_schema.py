from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator


class SubscriptionAdd(BaseModel):
    """
    Schema used when creating a subscription.
    - ticker: required, normalized to uppercase.
    - user_id: optional here because the API/service layer often infers the user
      from the authenticated request context. Provide it only for tests or admin actions.
    """
    ticker: str = Field(..., min_length=1, max_length=10)
    user_id: Optional[int] = Field(None, description="Optional user id (usually inferred from auth)")

class SubscriptionOutput(BaseModel):
    """
    Schema returned from API for subscription resources.
    - orm_mode = True allows Pydantic to read data directly from SQLAlchemy model instances.
    """
    id: int
    user_id: int
    ticker: str
    created_at: datetime
    updated_at: Optional[datetime] = None


