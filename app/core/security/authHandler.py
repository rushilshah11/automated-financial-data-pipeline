"""
Utility for encoding and decoding JSON Web Tokens (JWTs).

This small helper centralizes encoding/decoding logic and pulls
secrets/algorithm configuration from the project's settings. Tokens
include a simple `user_id` claim and an expiration (`exp`).
"""

import jwt
from app.settings import settings
import time


# Configuration values come from environment via settings
JWT_SECRET = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM


class AuthHandler(object):
    """Static helpers to encode/decode JWTs used for authentication.

    - encode_token(user_id) -> str: creates a signed JWT containing a user id
      and an expiration timestamp.
    - decode_token(token) -> dict|None: validates and returns the payload or
      None if invalid/expired.
    """

    @staticmethod
    def encode_token(user_id: int) -> str:
        payload = {
            'user_id': user_id,
            # `exp` is a unix timestamp (seconds since epoch)
            'exp': time.time() + 900  # token valid for 15 minutes
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            # Return payload only if not expired (jwt.decode will already
            # raise for expired tokens depending on options; we defensively
            # check exp here too).
            return payload if payload.get('exp', 0) >= time.time() else None
        except Exception:
            # In production you'd probably raise a typed exception and
            # enable structured logging. For the tutorial, we keep it simple.
            print("Token decode error")
            return None