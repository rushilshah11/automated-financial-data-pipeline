"""
Database utilities and SQLAlchemy engine/session setup.

This module creates the SQLAlchemy engine, session factory (`SessionLocal`),
and a declarative `Base` for models to inherit from. It also exposes a
`get_db()` generator suitable for FastAPI's `Depends` to provide a session
per-request and ensure it is closed afterwards.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings
import logging

logger = logging.getLogger(__name__)


# Read the database URL from settings (loaded from environment/.env)
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# Create the engine and a configured session factory. echo=False silences SQL logs.
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base used by model classes (e.g. app.db.models.user.User)
Base = declarative_base()


def get_db():
    """Yield a DB session and ensure it is closed after use.

    Use like: `session: Session = Depends(get_db)` in FastAPI endpoint
    signatures to guarantee proper session lifecycle per request.
    """
    db = SessionLocal()
    logger.debug("Opened new DB session %s", db)
    try:
        yield db
    finally:
        db.close()
        logger.debug("Closed DB session %s", db)