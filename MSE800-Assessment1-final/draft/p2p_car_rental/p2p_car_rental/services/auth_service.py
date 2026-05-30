"""
Authentication Service
======================
Handles user registration and login.
"""

from database.db_manager import DatabaseManager
from factories.user_factory import UserFactory
from utils.security import hash_password, verify_password
from utils.validators import is_valid_email, is_valid_password


class AuthService:
    """Service for user authentication and registration."""

    def __init__(self):
        self.db = DatabaseManager()

    def register(self, name, email, password, phone, role,
                  license_number=None) -> tuple:
        """
        Register a new user.

        Returns:
            (success: bool, message: str, user: User or None)
        """
        # Validation
        if not is_valid_email(email):
            return False, "Invalid email format", None

        ok, msg = is_valid_password(password)
        if not ok:
            return False, msg, None

        if role not in ('owner', 'renter'):
            return False, "Role must be 'owner' or 'renter'", None

        # Check duplicate email
        existing = self.db.fetch_one(
            "SELECT id FROM users WHERE email = ?", (email,)
        )
        if existing:
            return False, "Email already registered", None

        # Insert
        try:
            cursor = self.db.execute("""
                INSERT INTO users (name, email, password_hash, phone, role,
                                    license_number, is_verified)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            """, (name, email, hash_password(password), phone, role,
                  license_number))
            user_id = cursor.lastrowid

            user = UserFactory.create(
                role=role, user_id=user_id, name=name, email=email,
                password_hash=hash_password(password), phone=phone,
                license_number=license_number, is_verified=False,
            )
            return True, "Registration successful! Awaiting admin verification.", user
        except Exception as e:
            return False, f"Registration failed: {e}", None

    def login(self, email, password) -> tuple:
        """
        Authenticate a user.

        Returns:
            (success: bool, message: str, user: User or None)
        """
        row = self.db.fetch_one(
            "SELECT * FROM users WHERE email = ?", (email,)
        )
        if not row:
            return False, "User not found", None

        if not verify_password(password, row['password_hash']):
            return False, "Incorrect password", None

        user = UserFactory.from_db_row(row)
        return True, f"Welcome back, {user.name}!", user
