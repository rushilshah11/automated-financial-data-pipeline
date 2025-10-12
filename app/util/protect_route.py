"""
Dependency used to protect routes by validating the Authorization header.

This function expects an HTTP header named `Authorization` with the
value `Bearer <token>`. It decodes the token using AuthHandler, then
loads the corresponding user and returns a `UserOutput` Pydantic model.
If anything goes wrong the dependency raises HTTP 401 Unauthorized.
"""

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.service.user_service import UserService
from app.core.database import get_db
from app.db.schemas.user_schema import UserOutput


AUTH_PREFIX = "Bearer "


def get_current_user(
        authorization: Annotated[Union[str, None], Header()] = None, session: Session = Depends(get_db)
) -> UserOutput:
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Basic header checks
    if not authorization:
        raise auth_exception
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    # Decode the token and ensure it contains a user_id
    payload = AuthHandler.decode_token(authorization[len(AUTH_PREFIX):])

    if payload and payload.get("user_id"):
        try:
            user = UserService(session=session).get_user_by_id(payload["user_id"])
            # Return a Pydantic object (safe for JSON serialization)
            return UserOutput(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
        except Exception as e:
            print(f"Error fetching user: {e}")
            raise e

    # Token invalid or missing required claims
    raise auth_exception