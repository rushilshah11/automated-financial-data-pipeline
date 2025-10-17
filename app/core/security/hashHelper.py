"""
Simple wrapper around bcrypt for hashing and verifying passwords.

Keeping this logic in a helper centralizes hashing algorithm choices and
makes it easy to replace or tweak the hashing policy (e.g. increasing
work factor) in one place.
"""

from bcrypt import checkpw, gensalt, hashpw
import logging

logger = logging.getLogger(__name__)


class HashHelper(object):
    """Helpers for password hashing and verification.

    get_password_hash returns a string suitable for storage in the DB.
    verify_password compares a plaintext password with a stored hash.
    """

    @staticmethod
    def get_password_hash(password: str) -> str:
        # bcrypt returns bytes; decode to store as text in the DB
        hashed = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        # Log only non-sensitive metadata: hash length
        logger.debug("Generated password hash (len=%s)", len(hashed))
        return hashed

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # checkpw expects both args as bytes
        ok = checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        logger.debug("Password verification result: %s", ok)
        return ok