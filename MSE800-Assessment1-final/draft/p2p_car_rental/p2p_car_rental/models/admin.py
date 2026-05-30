"""
Admin model — Inherits from User
=================================
Platform administrator with elevated permissions.
"""

from models.user import User


class Admin(User):
    """Admin — manages platform users, listings, and disputes."""

    def __init__(self, user_id, name, email, password_hash, phone,
                 is_verified=True):
        super().__init__(user_id, name, email, password_hash, phone,
                          'admin', None, is_verified)

    def view_dashboard(self):
        """Polymorphism: Admin-specific dashboard."""
        return f"""
        ╔══════════════════════════════════════════╗
        ║   ADMIN PANEL — {self._name:<26} ║
        ╚══════════════════════════════════════════╝
        """
