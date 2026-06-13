"""Data model module for user and password reset database operations."""

import hashlib
import secrets
from datetime import datetime
from database import get_connection


class UserModel:
    """Handle user-related database operations and password hashing."""
    @staticmethod
    def hash_password(password, salt=None):
        """Hash a password using SHA-256 with a salt."""
        if salt is None:
            salt = secrets.token_hex(16)

        password_with_salt = password + salt
        password_hash = hashlib.sha256(password_with_salt.encode()).hexdigest()

        return password_hash, salt

    @staticmethod
    def verify_password(input_password, stored_hash, stored_salt):
        """Verify an input password against the stored password hash and salt."""
        input_hash, _ = UserModel.hash_password(input_password, stored_salt)
        return input_hash == stored_hash

    @staticmethod
    def create_user(full_name, date_of_birth, email, password):
        """Create a new user in the database."""
        password_hash, salt = UserModel.hash_password(password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users 
            (full_name, date_of_birth, email, password_hash, salt, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            date_of_birth,
            email,
            password_hash,
            salt,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_email(email):
        """Retrieve a user from the database by email."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, date_of_birth, email, password_hash, salt, created_at
            FROM users
            WHERE email = ?
        """, (email,))

        user = cursor.fetchone()
        conn.close()

        return user

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve a user from the database by ID."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, date_of_birth, email, created_at
            FROM users
            WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()
        conn.close()

        return user

    @staticmethod
    def update_profile(user_id, full_name, date_of_birth):
        """Update a user's profile information in the database."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET full_name = ?, date_of_birth = ?
            WHERE id = ?
        """, (full_name, date_of_birth, user_id))

        conn.commit()
        conn.close()

    @staticmethod
    def update_password(user_id, new_password):
        """Update a user's password in the database."""
        password_hash, salt = UserModel.hash_password(new_password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET password_hash = ?, salt = ?
            WHERE id = ?
        """, (password_hash, salt, user_id))

        conn.commit()
        conn.close()


class PasswordResetModel:
    """Handle password reset token database operations."""
    @staticmethod
    def create_reset_token(user_id, reset_token, expires_at):
        """Create a password reset token for a user."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO password_resets
            (user_id, reset_token, expires_at, used, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            reset_token,
            expires_at.isoformat(),
            0,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_reset_token(token):
        """Retrieve a password reset token record from the database."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, user_id, expires_at, used
            FROM password_resets
            WHERE reset_token = ?
        """, (token,))

        reset_record = cursor.fetchone()
        conn.close()

        return reset_record

    @staticmethod
    def mark_token_used(reset_id):
        """Mark a password reset token as used in the database."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE password_resets
            SET used = 1
            WHERE id = ?
        """, (reset_id,))

        conn.commit()
        conn.close()