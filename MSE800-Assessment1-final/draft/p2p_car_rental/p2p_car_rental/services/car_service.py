"""
Car Service
===========
Handles car-related business logic: add, remove, search, filter.
"""

from database.db_manager import DatabaseManager
from models.car import Car


class CarService:
    """Service for managing cars on the platform."""

    def __init__(self):
        self.db = DatabaseManager()

    # ── Owner operations ─────────────────────────────────────────────────────
    def add_car(self, owner_id, make, model, year, mileage, location,
                 daily_rate, min_rent_period=1, max_rent_period=30) -> tuple:
        """Add a new car listing (status = pending approval)."""
        try:
            cursor = self.db.execute("""
                INSERT INTO cars (owner_id, make, model, year, mileage,
                                   location, daily_rate, min_rent_period,
                                   max_rent_period, is_approved, is_available)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1)
            """, (owner_id, make, model, year, mileage, location,
                  daily_rate, min_rent_period, max_rent_period))
            return True, f"Car added (ID: {cursor.lastrowid}). Awaiting admin approval.", cursor.lastrowid
        except Exception as e:
            return False, f"Failed to add car: {e}", None

    def remove_car(self, owner_id, car_id) -> tuple:
        """Remove a car listing (only if owned by this owner)."""
        car = self.db.fetch_one(
            "SELECT * FROM cars WHERE id = ? AND owner_id = ?",
            (car_id, owner_id)
        )
        if not car:
            return False, "Car not found or you don't own it"

        # Check if there are active bookings
        active = self.db.fetch_one("""
            SELECT id FROM bookings
            WHERE car_id = ? AND status IN ('pending', 'approved')
        """, (car_id,))
        if active:
            return False, "Cannot remove car with active bookings"

        self.db.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        return True, "Car removed successfully"

    def get_owner_cars(self, owner_id):
        """Get all cars owned by a specific owner."""
        rows = self.db.fetch_all(
            "SELECT * FROM cars WHERE owner_id = ? ORDER BY id DESC",
            (owner_id,)
        )
        return [self._row_to_car(r) for r in rows]

    # ── Renter operations ────────────────────────────────────────────────────
    def search_cars(self, location=None, max_price=None) -> list:
        """Search for available, approved cars with optional filters."""
        query = """
            SELECT c.* FROM cars c
            JOIN users u ON c.owner_id = u.id
            WHERE c.is_approved = 1
              AND c.is_available = 1
              AND u.is_verified = 1
        """
        params = []
        if location:
            query += " AND LOWER(c.location) LIKE LOWER(?)"
            params.append(f"%{location}%")
        if max_price is not None:
            query += " AND c.daily_rate <= ?"
            params.append(max_price)
        query += " ORDER BY c.daily_rate ASC"

        rows = self.db.fetch_all(query, params)
        return [self._row_to_car(r) for r in rows]

    def get_car_by_id(self, car_id):
        """Get a single car by ID."""
        row = self.db.fetch_one("SELECT * FROM cars WHERE id = ?", (car_id,))
        return self._row_to_car(row) if row else None

    def get_owner_of_car(self, car_id):
        """Return the owner_id of a car."""
        row = self.db.fetch_one(
            "SELECT owner_id FROM cars WHERE id = ?", (car_id,)
        )
        return row['owner_id'] if row else None

    # ── Admin operations ─────────────────────────────────────────────────────
    def get_pending_cars(self):
        """Get all cars awaiting admin approval."""
        rows = self.db.fetch_all(
            "SELECT * FROM cars WHERE is_approved = 0 ORDER BY id"
        )
        return [self._row_to_car(r) for r in rows]

    def approve_car(self, car_id) -> tuple:
        """Admin: approve a car listing."""
        self.db.execute(
            "UPDATE cars SET is_approved = 1 WHERE id = ?", (car_id,)
        )
        return True, f"Car #{car_id} approved"

    def reject_car(self, car_id) -> tuple:
        """Admin: reject (delete) a car listing."""
        self.db.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        return True, f"Car #{car_id} rejected and removed"

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _row_to_car(self, row) -> Car:
        if not row:
            return None
        return Car(
            car_id=row['id'],
            owner_id=row['owner_id'],
            make=row['make'],
            model=row['model'],
            year=row['year'],
            mileage=row['mileage'],
            location=row['location'],
            daily_rate=row['daily_rate'],
            min_rent_period=row['min_rent_period'],
            max_rent_period=row['max_rent_period'],
            is_approved=row['is_approved'],
            is_available=row['is_available'],
        )
