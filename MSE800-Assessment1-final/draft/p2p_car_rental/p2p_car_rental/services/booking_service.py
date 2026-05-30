"""
Booking Service
===============
Handles booking-related business logic.

This is where the Use Case "Make booking" implements:
  «include» Check availability   (mandatory subtask)
  «include» Calculate total fee  (mandatory subtask)
  «extend»  Select insurance     (optional)
  «extend»  Apply discount code  (optional)

Optimizations:
  - Single-pass query for availability (uses idx_book_car_dates)
  - Aggregate stats use SQL SUM() instead of Python loops
  - JOINs replace N+1 queries when listing bookings
"""

from typing import List, Optional, Tuple, Dict
from database.db_manager import DatabaseManager
from models.booking import Booking
from models.car import Car
from patterns.insurance_strategy import get_insurance, InsuranceStrategy
from utils.helpers import days_between
from config import PLATFORM_FEE_PERCENT, LONG_TERM_DISCOUNTS


class BookingService:
    """Service for managing bookings."""

    def __init__(self):
        # Singleton — reuses the one connection
        self.db = DatabaseManager()

    # ── «include» Check availability ────────────────────────────────────────

    def check_availability(self, car_id: int, start_date: str,
                            end_date: str) -> Tuple[bool, str]:
        """
        Check if a car is free for the requested date range.

        How the date overlap check works:
            Two date ranges OVERLAP if NEITHER of these is true:
              - End A is before Start B   (A ends before B starts)
              - Start A is after End B    (A starts after B ends)
            So we use the negation: NOT (end_date < ? OR start_date > ?)

        Performance: this query uses idx_book_car_dates (composite index),
        so it's O(log n) instead of scanning every booking.
        """
        # Only check pending/approved bookings — rejected/cancelled don't matter
        rows = self.db.fetch_all("""
            SELECT id FROM bookings
            WHERE car_id = ?
              AND status IN ('pending', 'approved')
              AND NOT (end_date < ? OR start_date > ?)
        """, (car_id, start_date, end_date))

        if rows:
            # There's at least one conflicting booking
            return False, "Car is already booked during this period"
        return True, "Car is available"

    # ── «include» Calculate total fee ───────────────────────────────────────

    def calculate_total(self, car: Car, start_date: str, end_date: str,
                          insurance: InsuranceStrategy,
                          discount_percent: float = 0) -> Dict:
        """
        Calculate the FULL price breakdown for a booking.

        Pricing formula:
            base_price       = daily_rate × days
            long_term_discount → 7+ days = 10% off, 30+ days = 20% off
            discount_code    = additional X% off (e.g. SAVE10 = 10%)
            owner_amount     = base_price after both discounts
            platform_fee     = 15% of owner_amount (our commission)
            insurance_fee    = daily_fee × days  (from Strategy pattern)
            total_amount     = owner_amount + platform_fee + insurance_fee

        Why this design?
            - Owner gets paid the same regardless of how renter pays
            - Platform fee is calculated on top, not deducted from owner
            - Insurance is a separate line item (renter explicitly chose it)
        """
        # Step 1: Calculate base price (delegate to Car class — encapsulation)
        days = days_between(start_date, end_date)
        base_price = car.calculate_base_price(days)

        # Step 2: Apply long-term discount (sorted high-to-low, take first match)
        # Uses config-defined tiers so business can change them easily
        for min_days, discount_fraction in LONG_TERM_DISCOUNTS:
            if days >= min_days:
                base_price *= (1 - discount_fraction)
                break  # Only apply ONE discount tier

        # Step 3: Apply optional discount code (e.g. SAVE10 = 10% off)
        # Division by 100 converts percent to fraction (10 → 0.10)
        discount = base_price * (discount_percent / 100)
        owner_amount = base_price - discount

        # Step 4: Add insurance (delegated to the Strategy object)
        # If renter chose NoInsurance, this returns 0
        insurance_fee = insurance.calculate_fee(days)

        # Step 5: Platform takes its commission on the owner_amount
        platform_fee = owner_amount * PLATFORM_FEE_PERCENT

        # Step 6: Total = what the RENTER pays
        total_amount = owner_amount + platform_fee + insurance_fee

        # Return everything for the UI to display (line-item breakdown)
        return {
            'days': days,
            'base_price':      round(base_price, 2),
            'discount':        round(discount, 2),
            'owner_amount':    round(owner_amount, 2),
            'platform_fee':    round(platform_fee, 2),
            'insurance_fee':   round(insurance_fee, 2),
            'insurance_name':  insurance.name,
            'total_amount':    round(total_amount, 2),
        }

    # ── Make booking (Base UC) ──────────────────────────────────────────────

    def make_booking(self, car: Car, renter_id: int, start_date: str,
                      end_date: str, insurance_name: str = 'none',
                      discount_percent: float = 0) -> Tuple[bool, str, Optional[int]]:
        """Create a new booking (status = pending)."""

        # ── Step 1: «include» Check availability (mandatory) ─────────────────
        ok, msg = self.check_availability(car.id, start_date, end_date)
        if not ok:
            return False, msg, None

        # ── Step 2: Validate rent period against car's policy ────────────────
        days = days_between(start_date, end_date)
        if days < car.min_rent_period:
            return False, f"Minimum rental period is {car.min_rent_period} days", None
        if days > car.max_rent_period:
            return False, f"Maximum rental period is {car.max_rent_period} days", None

        # ── Step 3: Get insurance strategy (may be NoInsurance) ──────────────
        # The factory picks the right Strategy subclass at runtime
        insurance = get_insurance(insurance_name)

        # ── Step 4: «include» Calculate total (mandatory) ────────────────────
        pricing = self.calculate_total(car, start_date, end_date,
                                        insurance, discount_percent)

        # ── Step 5: Insert into DB inside try/except for robust error handling
        try:
            cursor = self.db.execute("""
                INSERT INTO bookings
                  (car_id, renter_id, owner_id, start_date, end_date,
                   insurance_type, insurance_fee, platform_fee,
                   owner_amount, total_amount, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            """, (car.id, renter_id, car.owner_id, start_date, end_date,
                  insurance.name, pricing['insurance_fee'],
                  pricing['platform_fee'], pricing['owner_amount'],
                  pricing['total_amount']))
            # lastrowid is the auto-generated booking ID
            return True, f"Booking #{cursor.lastrowid} created (awaiting owner approval)", cursor.lastrowid
        except Exception as e:
            # Catch any DB error and return it cleanly to the caller
            return False, f"Booking failed: {e}", None

    # ── Owner: approve/reject ───────────────────────────────────────────────

    def approve_booking(self, booking_id: int, owner_id: int) -> Tuple[bool, str]:
        """Owner approves a pending booking they received."""

        # Authorization check: verify this owner actually owns the booking
        # Without this, ANYONE could approve ANYONE's bookings — security hole
        booking = self.db.fetch_one(
            "SELECT * FROM bookings WHERE id = ? AND owner_id = ?",
            (booking_id, owner_id)
        )
        if not booking:
            return False, "Booking not found or you don't own this car"

        # State machine check: only pending bookings can be approved
        if booking['status'] != 'pending':
            return False, f"Cannot approve. Current status: {booking['status']}"

        # All checks passed — update status
        self.db.execute(
            "UPDATE bookings SET status = 'approved' WHERE id = ?",
            (booking_id,)
        )
        return True, f"Booking #{booking_id} approved"

    def reject_booking(self, booking_id: int, owner_id: int) -> Tuple[bool, str]:
        """Owner rejects a pending booking. Same auth pattern as approve."""
        booking = self.db.fetch_one(
            "SELECT * FROM bookings WHERE id = ? AND owner_id = ?",
            (booking_id, owner_id)
        )
        if not booking:
            return False, "Booking not found or you don't own this car"
        if booking['status'] != 'pending':
            return False, f"Cannot reject. Current status: {booking['status']}"

        self.db.execute(
            "UPDATE bookings SET status = 'rejected' WHERE id = ?",
            (booking_id,)
        )
        return True, f"Booking #{booking_id} rejected"

    # ── Renter: cancel ──────────────────────────────────────────────────────

    def cancel_booking(self, booking_id: int, renter_id: int) -> Tuple[bool, str]:
        """Renter cancels their own booking (if not already finalized)."""
        booking = self.db.fetch_one(
            "SELECT * FROM bookings WHERE id = ? AND renter_id = ?",
            (booking_id, renter_id)
        )
        if not booking:
            return False, "Booking not found"

        # Can't cancel something that's already terminal
        if booking['status'] in ('cancelled', 'completed', 'rejected'):
            return False, f"Cannot cancel. Current status: {booking['status']}"

        self.db.execute(
            "UPDATE bookings SET status = 'cancelled' WHERE id = ?",
            (booking_id,)
        )
        return True, f"Booking #{booking_id} cancelled"

    # ── Query methods (all use JOINs for performance) ───────────────────────

    def get_renter_bookings(self, renter_id: int) -> List:
        """
        Get a renter's bookings WITH car details (single query via JOIN).

        Why JOIN here?
            Without it: 1 query for bookings + N queries for each car = SLOW
            With it:    1 query that returns everything in one round-trip
        """
        return self.db.fetch_all("""
            SELECT b.*, c.make, c.model, c.year
            FROM bookings b
            JOIN cars c ON b.car_id = c.id
            WHERE b.renter_id = ?
            ORDER BY b.id DESC
        """, (renter_id,))

    def get_owner_bookings(self, owner_id: int,
                            status: Optional[str] = None) -> List:
        """Get an owner's bookings (optionally filter by status)."""
        if status:
            # Pre-filtered query (uses idx_book_status + idx_book_owner)
            return self.db.fetch_all("""
                SELECT b.*, c.make, c.model, c.year, u.name AS renter_name
                FROM bookings b
                JOIN cars c  ON b.car_id    = c.id
                JOIN users u ON b.renter_id = u.id
                WHERE b.owner_id = ? AND b.status = ?
                ORDER BY b.id DESC
            """, (owner_id, status))

        # No status filter — return all
        return self.db.fetch_all("""
            SELECT b.*, c.make, c.model, c.year, u.name AS renter_name
            FROM bookings b
            JOIN cars c  ON b.car_id    = c.id
            JOIN users u ON b.renter_id = u.id
            WHERE b.owner_id = ?
            ORDER BY b.id DESC
        """, (owner_id,))

    def get_all_bookings(self) -> List:
        """Admin: get all bookings with all related names."""
        # Three JOINs but still one query — SQLite handles this efficiently
        return self.db.fetch_all("""
            SELECT b.*, c.make, c.model, c.year,
                   ur.name AS renter_name, uo.name AS owner_name
            FROM bookings b
            JOIN cars  c  ON b.car_id    = c.id
            JOIN users ur ON b.renter_id = ur.id
            JOIN users uo ON b.owner_id  = uo.id
            ORDER BY b.id DESC
        """)

    def get_owner_earnings(self, owner_id: int) -> float:
        """
        Calculate total earnings for an owner.

        OPTIMIZATION: We use SQL's SUM() and COALESCE() instead of
        fetching all rows and summing in Python. This is much faster
        when there are many bookings (calculation happens on the DB side).
        """
        # COALESCE returns 0 if SUM returns NULL (i.e. no bookings yet)
        row = self.db.fetch_one("""
            SELECT COALESCE(SUM(owner_amount), 0) AS total
            FROM bookings
            WHERE owner_id = ?
              AND status IN ('approved', 'completed')
        """, (owner_id,))
        return row['total'] if row else 0
