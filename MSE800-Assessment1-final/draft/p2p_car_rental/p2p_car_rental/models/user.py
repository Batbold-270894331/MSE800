"""
User model — Abstract base class
=================================
Demonstrates OOP principles:
  - Abstraction (abstract methods)
  - Encapsulation (private fields with _ prefix)
  - Inheritance (Owner, Renter, Admin extend User)
  - Polymorphism (view_dashboard differs per role)
"""

from abc import ABC, abstractmethod


class User(ABC):
    """Abstract base class for all users (Owner, Renter, Admin)."""

    def __init__(self, user_id, name, email, password_hash, phone,
                 role, license_number=None, is_verified=False):
        # Encapsulation: protected attributes (prefix with _)
        self._id = user_id
        self._name = name
        self._email = email
        self._password_hash = password_hash
        self._phone = phone
        self._role = role
        self._license_number = license_number
        self._is_verified = bool(is_verified)

    # ── Properties (getters) ─────────────────────────────────────────────────
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def role(self):
        return self._role

    @property
    def license_number(self):
        return self._license_number

    @property
    def is_verified(self):
        return self._is_verified

    @property
    def password_hash(self):
        """Read-only access to password hash (used for auth)."""
        return self._password_hash

    # ── Abstract method: must be implemented by subclasses ──────────────────
    @abstractmethod
    def view_dashboard(self):
        """Each role displays a different dashboard (Polymorphism)."""
        pass

    # ── Common method ───────────────────────────────────────────────────────
    def view_profile(self):
        """Display user profile info."""
        verified = "Yes" if self._is_verified else "No (pending admin verification)"
        return {
            'ID': self._id,
            'Name': self._name,
            'Email': self._email,
            'Phone': self._phone,
            'Role': self._role.capitalize(),
            'Verified': verified,
        }

    def __str__(self):
        return f"{self._role.capitalize()}({self._name}, {self._email})"
