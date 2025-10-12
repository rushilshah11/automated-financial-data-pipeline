"""
Authentication routes (register/login).

This router delegates business logic to the `UserService` and uses
Pydantic response models to validate outgoing payloads.
"""

from fastapi import APIRouter, Depends
from app.db.schemas.user_schema import UserInRegister, UserInLogin, UserWithToken, UserOutput
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.service.user_service import UserService


auth_router = APIRouter()


@auth_router.post("/login", status_code=200, response_model=UserWithToken)
async def login(loginDetails: UserInLogin, session: Session = Depends(get_db)):
    """Authenticate a user and return a token (and user payload).

    The heavy lifting lives in `UserService.login_user` which handles
    validation, password verification and token creation.
    """
    try:
        user_service = UserService(session)
        return user_service.login_user(login_details=loginDetails)
    except Exception as e:
        # For development we print errors; in production use structured logging
        print(f"Error during login: {e}")
        raise e


@auth_router.post("/register", status_code=201, response_model=UserOutput)
async def register(registerDetails: UserInRegister, session: Session = Depends(get_db)):
    """Create a new user.

    Returns the created user (without password). Duplicate emails raise 400.
    """
    try:
        user_service = UserService(session)
        return user_service.register_user(user_details=registerDetails)
    except Exception as e:
        print(f"Error during registration: {e}")
        raise e

# Typical call flow: router -> service -> repository -> DB