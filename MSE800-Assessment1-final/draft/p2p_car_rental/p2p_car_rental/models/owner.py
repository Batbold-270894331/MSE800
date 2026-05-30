"""
Owner model — Inherits from User
=================================
Represents a car owner who can list cars and approve bookings.
"""

from models.user import User


class Owner(User):
    """Car owner — lists cars on the platform and earns rental income."""

    def __init__(self, user_id, name, email, password_hash, phone,
                 license_number=None, is_verified=False):
        super().__init__(user_id, name, email, password_hash, phone,
                          'owner', license_number, is_verified)

    def view_dashboard(self):
        """Polymorphism: Owner-specific dashboard."""
        return f"""
        ╔══════════════════════════════════════════╗
        ║   OWNER DASHBOARD — {self._name:<22} ║
        ╚══════════════════════════════════════════╝
        """
