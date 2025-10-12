"""
Base repository class that concrete repositories inherit from.

It simply stores the SQLAlchemy `Session` instance so repository
methods can run queries and commits. Keeping repositories thin helps
unit testing and separates DB concerns from business logic.
"""

from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, session: Session) -> None:
        # session: a SQLAlchemy session provided by FastAPI dependency
        self.session = session