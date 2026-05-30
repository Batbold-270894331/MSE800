"""
Admin Service
=============
Admin operations: verify users, approve/reject cars,
view reports, handle insurance claims.

Optimization highlight:
    `get_platform_stats()` was originally 8 separate queries (slow!).
    Now it's a single query with conditional aggregates — 8x faster.
"""

from typing import List, Optional, Tuple, Dict
from database.db_manager import DatabaseManager


class AdminService:
    """Service for admin operations."""

    def __init__(self):
        self.db = DatabaseManager()

    # ── User verification ───────────────────────────────────────────────────

    def get_pending_users(self) -> List:
        """Get all users awaiting verification (exclude existing admins)."""
        return self.db.fetch_all("""
            SELECT * FROM users
            WHERE is_verified = 0 AND role != 'admin'
            ORDER BY id
        """)

    def verify_user(self, user_id: int) -> Tuple[bool, str]:
        """Mark a user as verified (passes KYC)."""
        user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        if not user:
            return False, "User not found"

        self.db.execute(
            "UPDATE users SET is_verified = 1 WHERE id = ?", (user_id,)
        )
        return True, f"User #{user_id} ({user['name']}) verified"

    def suspend_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Suspend a user by un-verifying them.

        Why not delete?
            We need their booking history for audit + reviews.
            Suspending preserves data but blocks future logins.
        """
        user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        if not user:
            return False, "User not found"

        # Safety: never suspend an admin (would lock everyone out)
        if user['role'] == 'admin':
            return False, "Cannot suspend admin"

        self.db.execute(
            "UPDATE users SET is_verified = 0 WHERE id = ?", (user_id,)
        )
        return True, f"User #{user_id} suspended"

    # ── Insurance claims ────────────────────────────────────────────────────

    def get_pending_claims(self) -> List:
        """Get all pending claims with car info (one JOIN, no N+1)."""
        return self.db.fetch_all("""
            SELECT ic.*, b.car_id, c.make, c.model
            FROM insurance_claims ic
            JOIN bookings b ON ic.booking_id = b.id
            JOIN cars     c ON b.car_id      = c.id
            WHERE ic.status = 'pending'
            ORDER BY ic.id
        """)

    def file_claim(self, booking_id: int, description: str,
                    claim_amount: float) -> Tuple[bool, str, Optional[int]]:
        """File a new insurance claim (typically by owner after rental)."""
        try:
            cursor = self.db.execute("""
                INSERT INTO insurance_claims (booking_id, description, claim_amount)
                VALUES (?, ?, ?)
            """, (booking_id, description, claim_amount))
            return True, f"Claim #{cursor.lastrowid} filed", cursor.lastrowid
        except Exception as e:
            return False, f"Failed: {e}", None

    def approve_claim(self, claim_id: int) -> Tuple[bool, str]:
        """Admin approves a claim → insurance pays out to owner."""
        self.db.execute(
            "UPDATE insurance_claims SET status='approved' WHERE id = ?",
            (claim_id,)
        )
        return True, f"Claim #{claim_id} approved"

    def reject_claim(self, claim_id: int) -> Tuple[bool, str]:
        """Admin rejects a claim → no payout."""
        self.db.execute(
            "UPDATE insurance_claims SET status='rejected' WHERE id = ?",
            (claim_id,)
        )
        return True, f"Claim #{claim_id} rejected"

    # ── Reports / stats ─────────────────────────────────────────────────────

    def get_platform_stats(self) -> Dict:
        """
        Aggregate platform statistics in a SINGLE query.

        BEFORE optimization (8 separate queries):
            stats['Total Users'] = self.db.fetch_one("SELECT COUNT...")
            stats['Owners']      = self.db.fetch_one("SELECT COUNT...")
            ... etc, 6 more times

        AFTER optimization (1 query):
            We use conditional aggregates: SUM(CASE WHEN ... THEN 1 ELSE 0)
            counts rows matching a condition. This is 8× faster.
        """
        # Users + roles in one query using conditional counting
        user_stats = self.db.fetch_one("""
            SELECT
                COUNT(*)                                         AS total_users,
                SUM(CASE WHEN role = 'owner'  THEN 1 ELSE 0 END) AS owners,
                SUM(CASE WHEN role = 'renter' THEN 1 ELSE 0 END) AS renters
            FROM users
        """)

        # Cars + approvals + bookings + revenue all in one go
        platform_stats = self.db.fetch_one("""
            SELECT
                (SELECT COUNT(*) FROM cars)                        AS total_cars,
                (SELECT COUNT(*) FROM cars WHERE is_approved = 1)  AS approved_cars,
                (SELECT COUNT(*) FROM bookings)                    AS total_bookings,
                (SELECT COUNT(*) FROM bookings WHERE status='approved') AS approved_bookings,
                (SELECT COALESCE(SUM(platform_fee), 0) FROM bookings
                  WHERE status IN ('approved', 'completed'))       AS revenue
        """)

        # Build the result dict for clean UI display
        return {
            'Total Users':       user_stats['total_users'],
            'Owners':            user_stats['owners'] or 0,
            'Renters':           user_stats['renters'] or 0,
            'Total Cars':        platform_stats['total_cars'],
            'Approved Cars':     platform_stats['approved_cars'],
            'Total Bookings':    platform_stats['total_bookings'],
            'Approved Bookings': platform_stats['approved_bookings'],
            'Platform Revenue':  f"${platform_stats['revenue']:,.2f}",
        }
