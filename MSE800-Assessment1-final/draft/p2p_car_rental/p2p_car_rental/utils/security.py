"""
Security utilities — Password hashing
======================================
Uses SHA-256 with salt for password hashing.

Why hash passwords?
    Storing raw passwords is a CRITICAL security vulnerability.
    If the DB is leaked, attackers get every user's password directly.
    Hashing makes the stored value useless even if leaked.

Why salt?
    Same password → same hash. Without salt, two users with password
    "abc123" produce IDENTICAL hashes. With salt, hashes are unique.
    The salt also defeats rainbow-table attacks.

NOTE: SHA-256 is fast — fine for an academic project, but for production
      use bcrypt or argon2 (intentionally slow algorithms designed for passwords).
"""

import hashlib
from config import PASSWORD_SALT


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with the configured salt.

    Args:
        password: Plain-text password from user input

    Returns:
        Hex string of the SHA-256 hash (64 chars)
    """
    # Concatenate password + salt before hashing
    salted = (password + PASSWORD_SALT).encode('utf-8')
    # hashlib expects bytes; .hexdigest() converts the result to a readable string
    return hashlib.sha256(salted).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a plain-text password against a stored hash.

    We hash the input and compare to the stored hash — never decrypt
    (you CAN'T un-hash; that's the whole point).
    """
    return hash_password(password) == hashed
