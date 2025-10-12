"""
Database initialization helpers.

`create_tables` will create any missing tables based on SQLAlchemy models.
We made it async so it can be awaited during FastAPI's async lifespan.
"""

from app.core.database import Base, engine
from app.db.models import user, subscription


# Create all tables defined on SQLAlchemy models. Kept async so it can be
# awaited from FastAPI lifespan handlers without blocking the event loop.
async def create_tables():
    Base.metadata.create_all(bind=engine)


