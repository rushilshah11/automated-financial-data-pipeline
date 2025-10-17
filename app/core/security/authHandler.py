"""
Utility for encoding and decoding JSON Web Tokens (JWTs).

This small helper centralizes encoding/decoding logic and pulls
secrets/algorithm configuration from the project's settings. Tokens
include a simple `user_id` claim and an expiration (`exp`).
"""

import jwt
from app.settings import settings
import time
import logging

logger = logging.getLogger(__name__)


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
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        logger.info("Generated token for user_id=%s (expires in %s minutes)", user_id, 15)
        return token

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            # If the token lacks an exp claim or is expired, treat as invalid
            if "exp" not in payload:
                logger.warning("Token missing exp claim")
                return None
            if payload["exp"] < time.time():
                logger.warning("Token expired for user_id=%s", payload.get("user_id"))
                return None
            logger.debug("Decoded token payload for user_id=%s", payload.get("user_id"))
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired (ExpiredSignatureError)")
            return None
        except Exception as e:
            logger.exception("Failed to decode token: %s", e)
            return None
