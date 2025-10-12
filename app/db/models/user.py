"""
SQLAlchemy User model.

This model maps to the `users` table. We keep the Python attribute
`password` but map it to the underlying DB column `hashed_password` so
existing application code can continue to access `user.password` while
the database column name remains explicit and descriptive.
"""

from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)

    # Map the attribute `password` to DB column `hashed_password`.
    # This stores the bcrypt hash produced by HashHelper.get_password_hash.
    password = Column('hashed_password', String(250))

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship to other models (example: Subscription)
    subscriptions = relationship("Subscription", back_populates="user")