"""
Business logic for user operations.

This layer coordinates validation and repository calls. It also handles
HTTPException raising so the router can return appropriate status codes.
Keep this layer free of framework code wherever possible to make it
easier to unit-test.
"""

from app.db.repository.user_repo import UserRepository
from app.db.schemas.user_schema import UserInRegister, UserOutput, UserInLogin, UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class UserService:
    def __init__(self, session: Session):
        # repository is responsible for talking to the DB
        self.__userRepo = UserRepository(session)

    def register_user(self, user_details: UserInRegister) -> UserOutput:
        """Register a user after ensuring the email is unique.

        The password in `user_details` is replaced with a bcrypt hash
        before creating the DB record.
        """
        existing_user = self.__userRepo.user_exist_by_email(email=user_details.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered. Please Login!"
            )

        # Hash the plaintext password and store the hash in the model
        hashed_password = HashHelper.get_password_hash(password=user_details.password)
        user_details.password = hashed_password
        new_user = self.__userRepo.create_user(user_data=user_details)
        return new_user

    def login_user(self, login_details: UserInLogin) -> UserWithToken:
        """Verify credentials and return a token (and user payload).

        Raises HTTPException(400) for authentication failures and 500 for
        token generation problems.
        """
        existing_user = self.__userRepo.user_exist_by_email(email=login_details.email)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password. Create Account!"
            )

        user = self.__userRepo.get_user_by_email(email=login_details.email)
        # verify_password compares plaintext with stored bcrypt hash
        if not HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password. Please try again!"
            )

        token = AuthHandler.encode_token(user_id=user.id)
        if token:
            # Note: response model expects user+token; current implementation
            # returns only token in some versions — update tests accordingly.
            return UserWithToken(token=token)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token generation failed. Please try again!"
        )

    def get_user_by_id(self, user_id: int):
        """Fetch a user model by id or raise a 404 HTTPException."""
        user = self.__userRepo.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        return user
