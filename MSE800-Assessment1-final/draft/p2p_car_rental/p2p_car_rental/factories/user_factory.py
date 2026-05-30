"""
User Factory — Factory Method Pattern
=====================================
Creates the right User subclass based on role.
"""

from models.owner import Owner
from models.renter import Renter
from models.admin import Admin


class UserFactory:
    """Factory class to create User instances based on role."""

    @staticmethod
    def create(role: str, user_id, name, email, password_hash,
                phone, license_number=None, is_verified=False):
        """
        Create a User instance based on the role parameter.

        Args:
            role: 'owner', 'renter', or 'admin'
            ... other user fields

        Returns:
            An Owner, Renter, or Admin instance.

        Raises:
            ValueError if role is unknown.
        """
        role = role.lower()
        if role == 'owner':
            return Owner(user_id, name, email, password_hash, phone,
                          license_number, is_verified)
        elif role == 'renter':
            return Renter(user_id, name, email, password_hash, phone,
                           license_number, is_verified)
        elif role == 'admin':
            return Admin(user_id, name, email, password_hash, phone,
                          is_verified)
        else:
            raise ValueError(f"Unknown role: {role}")

    @staticmethod
    def from_db_row(row):
        """Create a User instance from a database row (sqlite3.Row)."""
        return UserFactory.create(
            role=row['role'],
            user_id=row['id'],
            name=row['name'],
            email=row['email'],
            password_hash=row['password_hash'],
            phone=row['phone'],
            license_number=row['license_number'] if 'license_number' in row.keys() else None,
            is_verified=row['is_verified'],
        )
