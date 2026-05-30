"""
Renter model — Inherits from User
==================================
Represents a customer who rents cars.
"""

from models.user import User


class Renter(User):
    """Renter — searches and books cars on the platform."""

    def __init__(self, user_id, name, email, password_hash, phone,
                 license_number=None, is_verified=False):
        super().__init__(user_id, name, email, password_hash, phone,
                          'renter', license_number, is_verified)

    def view_dashboard(self):
        """Polymorphism: Renter-specific dashboard."""
        return f"""
        ╔══════════════════════════════════════════╗
        ║   RENTER DASHBOARD — {self._name:<21} ║
        ╚══════════════════════════════════════════╝
        """
