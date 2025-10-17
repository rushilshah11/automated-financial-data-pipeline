from sqlalchemy.orm import Session
from app.db.repository.base import BaseRepository
from app.db.models.subscription import Subscription
from app.db.schemas.subscription_schema import SubscriptionAdd
from typing import List
from sqlalchemy import distinct
import logging

logger = logging.getLogger(__name__)


class SubscriptionRepository(BaseRepository):
	"""Repository for subscription-related DB operations.

	Provides helpers used by the service layer. Methods return SQLAlchemy
	model instances so callers can commit/refresh or convert to Pydantic.
	"""

	def create_subscription(self, ticker: str, user_id: int) -> Subscription:
		"""Create and return a new Subscription."""
		sub = Subscription(ticker=ticker.upper(), user_id=user_id)
		self.session.add(sub)
		self.session.commit()
		self.session.refresh(sub)
		# logging: created
		logger.info("Created subscription id=%s user_id=%s ticker=%s", sub.id, user_id, sub.ticker)
		return sub

	def get_subscription_by_id(self, sub_id: int) -> Subscription | None:
		return self.session.query(Subscription).filter_by(id=sub_id).first()

	def get_by_user_and_ticker(self, user_id: int, ticker: str) -> Subscription | None:
		return (
			self.session.query(Subscription)
			.filter_by(user_id=user_id, ticker=ticker.upper())
			.first()
		)

	def list_by_user(self, user_id: int) -> List[Subscription]:
		return self.session.query(Subscription).filter_by(user_id=user_id).all()

	def list_all(self) -> List[Subscription]:
		return self.session.query(Subscription).all()

	def delete_subscription(self, sub: Subscription) -> None:
		self.session.delete(sub)
		self.session.commit()
		logger.info("Deleted subscription id=%s", sub.id)

	def delete_by_user_and_ticker(self, user_id: int, ticker: str) -> int:
		"""Delete subscriptions for user/ticker and return number deleted."""
		q = self.session.query(Subscription).filter_by(user_id=user_id, ticker=ticker.upper())
		count = q.delete()
		self.session.commit()
		logger.info("Deleted %s rows for user_id=%s ticker=%s", count, user_id, ticker.upper())
		return count

	def check_ticker_by_user(self, user_id: int, ticker: str) -> bool:
		"""Return True if a subscription for the (user_id, ticker) exists."""
		exists = (
			self.session.query(Subscription)
			.filter_by(user_id=user_id, ticker=ticker.upper())
			.first()
		)
		return bool(exists)

	def get_all_unique_tickers(self) -> List[str]:
		"""Return a list of all unique ticker symbols subscribed to."""
		tickers = (
			self.session.query(distinct(Subscription.ticker))
			.all()
		)
		# Flatten the list of single-item tuples: [('AAPL',), ('GOOG',)] -> ['AAPL', 'GOOG']
		return [t[0] for t in tickers]