"""
Business logic for subscription management.

Provides functions to create, list, and delete user subscriptions while
encapsulating repository calls and raising appropriate HTTP errors for the
router layer.
"""

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.repository.subscription_repo import SubscriptionRepository
from app.db.schemas.subscription_schema import SubscriptionAdd, SubscriptionOutput
from app.db.models.subscription import Subscription


class SubscriptionService:
    def __init__(self, session: Session):
        self._repo = SubscriptionRepository(session)

    def subscribe(self, user_id: int, payload: SubscriptionAdd) -> Subscription:
        """Create a subscription for the user.

        Raises HTTPException(400) when subscription already exists.
        Returns the SQLAlchemy Subscription model instance on success.
        """
        # normalize ticker and check for existing
        ticker = payload.ticker.upper()
        if self._repo.check_ticker_by_user(user_id=user_id, ticker=ticker):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Already subscribed to {ticker}."
            )

        sub = self._repo.create_subscription(ticker=ticker, user_id=user_id)
        return sub

    def list_user_subscriptions(self, user_id: int) -> List[Subscription]:
        """Return a list of Subscription model instances for the user."""
        return self._repo.list_by_user(user_id=user_id)

    def unsubscribe(self, user_id: int, ticker: str) -> int:
        """Delete subscription(s) for a given user and ticker.

        Returns the number of deleted rows (0 if none existed). If nothing was
        deleted, raises 404 to signal resource not found.
        """
        count = self._repo.delete_by_user_and_ticker(user_id=user_id, ticker=ticker)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subscription for {ticker.upper()} not found."
            )
        return count
