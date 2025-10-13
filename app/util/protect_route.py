"""
Dependency used to protect routes by validating the Authorization header.

This function expects an HTTP header named `Authorization` with the
value `Bearer <token>`. It decodes the token using AuthHandler, then
loads the corresponding user and returns a `UserOutput` Pydantic model.
If anything goes wrong the dependency raises HTTP 401 Unauthorized.
"""

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.service.user_service import UserService
from app.core.database import get_db
from app.db.schemas.user_schema import UserOutput


security = HTTPBearer()
AUTH_PREFIX = "Bearer "


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: Session = Depends(get_db),
) -> UserOutput:

    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again.",
    )

    token = credentials.credentials  # automatically extracts token after "Bearer "
    payload = AuthHandler.decode_token(token=token[len(AUTH_PREFIX):])

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




# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozNSwiZXhwIjoxNzYwMzI5ODA3LjQ5NTA2OX0.PYH62KxUVeHUtREmdarwyKa4hoeol6KvdtivZmCDd3w

