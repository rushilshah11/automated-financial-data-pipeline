"""
Pydantic schemas for user input/output validation and serialization.

Use these in FastAPI request bodies (`UserInRegister`, `UserInLogin`) and
response models (`UserOutput`, `UserWithToken`). Pydantic ensures payload
shape and performs basic validation (e.g. `EmailStr`).
"""

from pydantic import EmailStr, BaseModel


class UserInRegister(BaseModel):
    # Request body expected when creating a new user
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    # Response payload for user objects returned by the API
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserInUpdate(BaseModel):
    # Optional fields for an update endpoint (not used in the tutorial)
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserInLogin(BaseModel):
    # Request body for login
    email: EmailStr
    password: str


class UserWithToken(BaseModel):
    # Response model that bundles a user object and a JWT token
    token: str