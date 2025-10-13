from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.util.protect_route import get_current_user
from app.db.schemas.user_schema import UserOutput
from app.db.schemas.subscription_schema import SubscriptionAdd, SubscriptionOutput
from app.service.subscription_service import SubscriptionService


subscription_router = APIRouter()


@subscription_router.post("/", response_model=SubscriptionOutput, status_code=status.HTTP_201_CREATED)
def create_subscription(
    payload: SubscriptionAdd,
    current_user: UserOutput = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Create a subscription for the authenticated user.

    The `user_id` field on the `SubscriptionAdd` schema is optional and is
    ignored in favor of the authenticated user's id.
    """
    service = SubscriptionService(session=session)
    sub = service.subscribe(user_id=current_user.id, payload=payload)
    # Pydantic's orm_mode allows returning the SQLAlchemy model directly
    return sub


@subscription_router.get("/", response_model=List[SubscriptionOutput])
def list_subscriptions(
    current_user: UserOutput = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """List subscriptions belonging to the authenticated user."""
    service = SubscriptionService(session=session)
    subs = service.list_user_subscriptions(user_id=current_user.id)
    return subs


@subscription_router.delete("/{ticker}", status_code=status.HTTP_200_OK)
def delete_subscription(
    ticker: str,
    current_user: UserOutput = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Unsubscribe the authenticated user from `ticker`.

    Returns a simple dict with `deleted` key indicating how many records
    were removed.
    """
    service = SubscriptionService(session=session)
    count = service.unsubscribe(user_id=current_user.id, ticker=ticker)
    return {"deleted": count}
