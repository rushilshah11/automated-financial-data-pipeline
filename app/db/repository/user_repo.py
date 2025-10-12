"""
Repository for user-related database operations.

This class contains simple CRUD helpers used by the service layer. The
methods accept and return SQLAlchemy model instances (not Pydantic models)
so callers can commit or refresh as needed.
"""

from .base import BaseRepository
from app.db.models.user import User
from app.db.schemas.user_schema import UserInRegister


class UserRepository(BaseRepository):
    """Encapsulate common user DB operations.

    Methods:
    - create_user(user_data) -> User: creates and returns the new user
    - user_exist_by_email(email) -> bool: quick existence check
    - get_user_by_email(email) -> User|None: fetch a user by email
    - get_user_by_id(user_id) -> User|None: fetch a user by id
    """

    def create_user(self, user_data: UserInRegister) -> User:
        # Pydantic -> dict -> SQLAlchemy model
        newUser = User(**user_data.model_dump(exclude_none=True))
        self.session.add(newUser)
        self.session.commit()
        # refresh to populate defaults like autoincremented id
        self.session.refresh(newUser)
        return newUser

    def user_exist_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.session.query(User).filter_by(id=user_id).first()

